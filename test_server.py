import json
import tempfile
import unittest
from types import SimpleNamespace
from pathlib import Path
from unittest.mock import patch

import start

FEED = b'''<?xml version="1.0"?><feed xmlns="http://www.w3.org/2005/Atom"><entry><id>http://arxiv.org/abs/2401.12345</id><title> A test paper </title><published>2024-01-02T00:00:00Z</published><updated>2024-01-03T00:00:00Z</updated><author><name>A. Author</name></author><journal_ref>Journal 1</journal_ref><doi>10.1234/test.1</doi></entry></feed>'''

class Clock:
    def __init__(self): self.t = 1000.0
    def __call__(self): return self.t
    def sleep(self, n): self.t += n

class ServerTests(unittest.TestCase):
    def test_parser_and_validation(self):
        paper = start.parse_arxiv_feed(FEED, "quant-ph")[0]
        self.assertEqual(paper["id"], "2401.12345"); self.assertEqual(paper["date"], "2024-01-02")
        self.assertEqual(paper["status"], "arXiv record; journal reference supplied")
        self.assertEqual(paper["doi"], "10.1234/test.1")
        with self.assertRaises(ValueError): start.normalize_arxiv_id("https://evil.test/abs/2401.12345")
        with self.assertRaises(ValueError): start.normalize_arxiv_id("https://arxiv.org/pdf/2401.12345")

    def test_empty_and_error_or_malformed_feed(self):
        self.assertEqual(start.parse_arxiv_feed(b'<feed xmlns="http://www.w3.org/2005/Atom"/>', "quant-ph"), [])
        with self.assertRaises(ValueError): start.parse_arxiv_feed(b"<broken>", "quant-ph")
        with self.assertRaises(ValueError): start.parse_arxiv_feed(b"<html>upstream error</html>", "quant-ph")
        with self.assertRaises(ValueError): start.parse_arxiv_feed(b'<feed xmlns="http://www.w3.org/2005/Atom"><entry><error>bad</error></entry></feed>', "quant-ph")

    def test_wrong_category_no_outgoing(self):
        with tempfile.TemporaryDirectory() as d:
            client = start.ArxivClient(Path(d) / "cache.json", fetch=lambda _: self.fail("outgoing"))
            with self.assertRaises(KeyError): client.get_papers("nope")

    def test_ttl_and_stale_failure_does_not_overwrite(self):
        with tempfile.TemporaryDirectory() as d:
            c = Clock(); calls=[]
            client = start.ArxivClient(Path(d) / "cache.json", fetch=lambda _: calls.append(1) or FEED, clock=c, sleep=c.sleep)
            fresh = client.get_papers("quant-ph"); self.assertFalse(fresh["cached"])
            self.assertTrue(client.get_papers("quant-ph")["cached"]); self.assertEqual(len(calls), 1)
            c.t += start.CACHE_TTL + 1; client.fetch = lambda _: (_ for _ in ()).throw(OSError("offline"))
            stale = client.get_papers("quant-ph"); self.assertTrue(stale["cached"]); self.assertIn("error", stale)
            saved = json.loads((Path(d) / "cache.json").read_text()); self.assertEqual(saved["quant-ph"]["papers"], fresh["papers"])

    def test_rate_spacing(self):
        c = Clock(); times=[]
        client = start.ArxivClient(Path(tempfile.gettempdir()) / "physics-test-cache.json", fetch=lambda _: times.append(c()) or b'<feed xmlns="http://www.w3.org/2005/Atom"/>', clock=c, sleep=c.sleep)
        client._request("quant-ph"); client._request("quant-ph")
        self.assertGreaterEqual(times[1] - times[0], start.RATE_INTERVAL)

    def test_loopback_request_origin(self):
        handler=object.__new__(start.PhysicsHandler)
        handler.server=SimpleNamespace(server_port=8001)
        for headers, expected in [
            ({'Host':'127.0.0.1:8001'},True),
            ({'Host':'localhost:8001','Origin':'http://localhost:8001'},True),
            ({'Host':'localhost:8001','Origin':'http://localhost:9000'},False),
            ({'Host':'evil.example:8001'},False),
            ({'Host':'localhost:8001','Origin':'null'},False),
            ({'Host':'localhost:8001','Origin':'http://localhost:invalid'},False),
        ]:
            handler.headers=headers
            self.assertEqual(handler._allowed_request(),expected)

    def test_future_cache_does_not_mask_refresh(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'cache.json'; calls=[]
            path.write_text(json.dumps({'quant-ph':{'fetchedAt':'2099-01-01T00:00:00Z','papers':[]}}))
            client=start.ArxivClient(path,fetch=lambda _:calls.append(1) or FEED)
            self.assertFalse(client.get_papers('quant-ph')['cached'])
            self.assertEqual(len(calls),1)

if __name__ == "__main__": unittest.main()
