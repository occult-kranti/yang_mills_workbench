#!/usr/bin/env python3
"""Local-only static server and arXiv metadata refresh endpoint."""
from __future__ import annotations

import argparse
import datetime as _dt
import html
import json
import mimetypes
import os
import re
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
import webbrowser
import xml.etree.ElementTree as ET
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Callable

ALLOWED_CATEGORIES = frozenset({
    "quant-ph", "cond-mat.str-el", "cond-mat.mtrl-sci", "cond-mat.stat-mech",
    "cond-mat.mes-hall", "cond-mat.soft", "hep-ex", "hep-th", "hep-ph",
    "nucl-ex", "nucl-th", "gr-qc", "astro-ph.CO", "astro-ph.HE", "astro-ph.IM",
    "astro-ph.EP", "astro-ph.GA", "astro-ph.SR", "physics.atom-ph", "physics.optics",
    "physics.plasm-ph", "physics.flu-dyn", "nlin.CD", "physics.bio-ph", "physics.ao-ph",
    "physics.geo-ph", "physics.comp-ph", "physics.ins-det",
    "physics.class-ph", "eess.AS", "math.MG", "math.DG", "math.HO",
})
ARXIV_API = "https://export.arxiv.org/api/query"
CACHE_TTL = 15 * 60
RATE_INTERVAL = 3.0
REQUEST_TIMEOUT = 12.0
MAX_BODY = 2 * 1024 * 1024
_ID_RE = re.compile(r"^(?:[a-z-]+(?:\.[A-Z-]+)?/\d{7}|\d{4}\.\d{4,5})(?:v\d+)?$", re.I)
_DATE_RE = re.compile(r"^(\d{4})-(\d{2})-(\d{2})")
_DOI_RE = re.compile(r"^10\.\d{4,9}/[-._;()/:A-Z0-9]+$", re.I)


def _text(parent: ET.Element, name: str) -> str:
    node = parent.find("{*}" + name)
    return (node.text or "").strip() if node is not None else ""


def normalize_date(value: str) -> str:
    match = _DATE_RE.match(value.strip())
    if not match:
        raise ValueError("invalid arXiv date")
    try:
        return _dt.date(int(match.group(1)), int(match.group(2)), int(match.group(3))).isoformat()
    except ValueError as exc:
        raise ValueError("invalid arXiv date") from exc


def normalize_arxiv_id(raw: str) -> tuple[str, str]:
    """Return (id, canonical abs URL), rejecting arbitrary URLs."""
    value = raw.strip()
    if value.startswith("http://") or value.startswith("https://"):
        parsed = urllib.parse.urlsplit(value)
        if parsed.scheme not in {"http", "https"} or parsed.netloc.lower() not in {"arxiv.org", "www.arxiv.org"}:
            raise ValueError("untrusted arXiv URL")
        path = parsed.path
        if not path.startswith("/abs/") or parsed.query or parsed.fragment:
            raise ValueError("invalid arXiv URL")
        value = path[5:]
    value = value.strip("/")
    if not _ID_RE.fullmatch(value):
        raise ValueError("invalid arXiv id")
    return value, "https://arxiv.org/abs/" + value


def normalize_doi(raw: str) -> str | None:
    value = raw.strip()
    if not value:
        return None
    if value.lower().startswith("https://doi.org/"):
        value = value[len("https://doi.org/"):]
    elif value.lower().startswith("http://doi.org/"):
        return None
    value = value.removeprefix("doi:").strip()
    if not _DOI_RE.fullmatch(value) or any(c in value for c in "<>\"' "):
        return None
    return value


def parse_arxiv_feed(body: bytes | str, category: str) -> list[dict[str, Any]]:
    if len(body.encode() if isinstance(body, str) else body) > MAX_BODY:
        raise ValueError("arXiv response too large")
    try:
        root = ET.fromstring(body)
    except ET.ParseError as exc:
        raise ValueError("malformed arXiv feed") from exc
    if root.tag != '{http://www.w3.org/2005/Atom}feed':
        raise ValueError('response is not an Atom feed')
    entries = root.findall("{*}entry")
    if len(entries) == 1 and (_text(entries[0], "error") or _text(entries[0], "title").strip().lower() == "error"):
        raise ValueError("arXiv returned an error")
    papers: list[dict[str, Any]] = []
    for entry in entries:
        title = " ".join(_text(entry, "title").split())
        raw_id = _text(entry, "id")
        if not title or not raw_id:
            raise ValueError("malformed arXiv entry")
        paper_id, url = normalize_arxiv_id(raw_id)
        date = normalize_date(_text(entry, "published"))
        updated = normalize_date(_text(entry, "updated"))
        authors = []
        for author in entry.findall("{*}author"):
            name = _text(author, "name")
            if name:
                authors.append(name)
        if not authors:
            raise ValueError("arXiv entry has no author")
        doi = normalize_doi(_text(entry, "doi"))
        # arXiv supplies journal_ref as metadata; it is not independently verified.
        journal = _text(entry, "journal_ref")
        status = "arXiv record; journal reference supplied" if journal else "arXiv preprint; publication not verified"
        papers.append({"id": paper_id, "title": html.unescape(title), "authors": authors,
                       "date": date, "updated": updated, "status": status, "url": url,
                       "doi": doi, "journal": journal or None, "category": category})
    return papers


class ArxivClient:
    def __init__(self, cache_path: Path | None = None, *, fetch: Callable[[str], bytes] | None = None,
                 clock: Callable[[], float] = time.time, sleep: Callable[[float], None] = time.sleep):
        self.cache_path = Path(cache_path) if cache_path else Path(__file__).with_name("data") / "paper-cache.json"
        self.fetch = fetch or self._fetch_url
        self.clock, self.sleep = clock, sleep
        self._rate_lock = threading.Lock()
        self._cache_lock = threading.Lock()
        self._last_request: float | None = None

    @staticmethod
    def _fetch_url(url: str) -> bytes:
        request = urllib.request.Request(url, headers={"User-Agent": "physics-observatory/1.0"})
        with urllib.request.urlopen(request, timeout=REQUEST_TIMEOUT) as response:
            body = response.read(MAX_BODY + 1)
        if len(body) > MAX_BODY:
            raise ValueError("arXiv response too large")
        return body

    def _request(self, category: str) -> bytes:
        with self._rate_lock:
            now = self.clock()
            if self._last_request is not None and now - self._last_request < RATE_INTERVAL:
                self.sleep(RATE_INTERVAL - (now - self._last_request))
            self._last_request = self.clock()
            params = urllib.parse.urlencode({"search_query": "cat:" + category, "max_results": 8,
                                             "sortBy": "submittedDate", "sortOrder": "descending"})
            return self.fetch(ARXIV_API + "?" + params)

    def _read_cache(self) -> dict[str, Any]:
        try:
            value = json.loads(self.cache_path.read_text(encoding="utf-8"))
            return value if isinstance(value, dict) else {}
        except (OSError, ValueError, TypeError):
            return {}

    def _write_cache(self, cache: dict[str, Any]) -> None:
        try:
            self.cache_path.parent.mkdir(parents=True, exist_ok=True)
            temp = self.cache_path.with_suffix(".tmp")
            temp.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")
            temp.replace(self.cache_path)
        except OSError:
            pass

    def get_papers(self, category: str) -> dict[str, Any]:
        with self._cache_lock:
            return self._get_papers(category)

    def _get_papers(self, category: str) -> dict[str, Any]:
        if category not in ALLOWED_CATEGORIES:
            raise KeyError(category)
        now = self.clock()
        cache = self._read_cache()
        prior = cache.get(category) if isinstance(cache.get(category), dict) else None
        if prior and isinstance(prior.get("fetchedAt"), str) and isinstance(prior.get("papers"), list):
            try:
                age = now - _dt.datetime.fromisoformat(prior["fetchedAt"].replace("Z", "+00:00")).timestamp()
            except (ValueError, TypeError, OverflowError):
                age = CACHE_TTL + 1
            if 0 <= age < CACHE_TTL:
                return {"papers": prior["papers"], "fetchedAt": prior["fetchedAt"], "cached": True, "category": category}
        try:
            papers = parse_arxiv_feed(self._request(category), category)
        except Exception as exc:
            if prior and isinstance(prior.get("papers"), list) and isinstance(prior.get("fetchedAt"), str):
                return {"papers": prior["papers"], "fetchedAt": prior["fetchedAt"], "cached": True,
                        "category": category, "error": "refresh failed; showing cached data"}
            return {"papers": [], "fetchedAt": None, "cached": False, "category": category,
                    "error": str(exc) or "refresh failed"}
        fetched = _dt.datetime.fromtimestamp(self.clock(), _dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
        cache[category] = {"papers": papers, "fetchedAt": fetched}
        self._write_cache(cache)
        return {"papers": papers, "fetchedAt": fetched, "cached": False, "category": category}


class PhysicsHandler(BaseHTTPRequestHandler):
    server_version = "PhysicsObservatory/1.0"

    def _json(self, status: int, payload: dict[str, Any]) -> None:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def _allowed_request(self) -> bool:
        allowed = {f'localhost:{self.server.server_port}',f'127.0.0.1:{self.server.server_port}'}
        if self.headers.get('Host','').lower() not in allowed:
            return False
        origin = self.headers.get("Origin")
        if origin:
            if origin.lower() not in {'http://'+host for host in allowed}:
                return False
        return True

    def do_GET(self) -> None:
        if not self._allowed_request():
            self._json(HTTPStatus.FORBIDDEN, {"error": "localhost access required"}); return
        parsed = urllib.parse.urlsplit(self.path)
        if parsed.path == "/api/papers":
            query = urllib.parse.parse_qs(parsed.query, strict_parsing=False)
            category = query.get("category", [""])[0]
            if category not in ALLOWED_CATEGORIES:
                self._json(HTTPStatus.BAD_REQUEST, {"error": "unsupported category"}); return
            result = self.server.arxiv.get_papers(category)
            self._json(HTTPStatus.OK, result); return
        if parsed.path.startswith("/api/"):
            self._json(HTTPStatus.NOT_FOUND, {"error": "not found"}); return
        self._serve_static(parsed.path)

    def _serve_static(self, path: str) -> None:
        relative = urllib.parse.unquote(path.lstrip("/")) or "index.html"
        root = self.server.dist.resolve()
        target = (root / relative).resolve()
        if root != target and root not in target.parents:
            self._json(HTTPStatus.NOT_FOUND, {"error": "not found"}); return
        if not target.is_file():
            self._json(HTTPStatus.NOT_FOUND, {"error": "not found"}); return
        data = target.read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", mimetypes.guess_type(str(target))[0] or "application/octet-stream")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers(); self.wfile.write(data)

    def log_message(self, fmt: str, *args: Any) -> None:
        pass


def make_server(port: int = 8001, dist: Path | None = None, cache_path: Path | None = None) -> ThreadingHTTPServer:
    server = ThreadingHTTPServer(("127.0.0.1", port), PhysicsHandler)
    server.dist = Path(dist) if dist else Path(__file__).with_name("dist")
    server.arxiv = ArxivClient(cache_path)
    return server


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Serve the local Physics Observatory")
    parser.add_argument("--port", type=int, default=8001)
    parser.add_argument("--no-browser", action="store_true")
    args = parser.parse_args(argv)
    if not 1 <= args.port <= 65535:
        parser.error('--port must be between 1 and 65535')
    try:
        server = make_server(args.port)
    except OSError as exc:
        parser.exit(1,f'Could not start on port {args.port}: {exc}. Try --port 8002.\n')
    url = f"http://127.0.0.1:{args.port}/"
    if not args.no_browser:
        webbrowser.open(url)
    print(f"Serving {server.dist} at {url}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
