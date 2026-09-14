#!/usr/bin/env python3
"""Render Round21 with source-checked gates and preserve prior research routes.

Only advisor data and verified gate content supply scientific statements.
The build checks evidence bytes; release-tree validation remains a separate gate.
"""
from __future__ import annotations

import hashlib
import json
import re
from copy import deepcopy
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[2]
ROUND = ROOT / "research/round21"
DIST = ROOT / "dist"
STATES = {"accepted", "limited", "pending", "running", "rejected", "deferred"}
REPOSITORY = "https://github.com/occult-kranti/yang_mills_workbench"


def strict_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def read(path):
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=strict_object)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def as_list(value):
    return value if isinstance(value, list) else [value] if value else []


def resolve_path(value, *, inventory=False):
    if not isinstance(value, str) or not value or "\\" in value:
        return None
    rel = PurePosixPath(value)
    if rel.is_absolute() or any(part in {".", ".."} for part in value.split("/")):
        return None
    if any(part.startswith(".") or part == "__pycache__" for part in rel.parts):
        return None
    if rel.suffix in {".pyc", ".pyo"}:
        return None
    candidate = ROOT / value if inventory or value.startswith(("research/", "docs/", "scripts/")) else ROUND / value
    # Inspect lexical ancestors before resolve() hides a linked directory.
    # Even a link whose target stays inside ROOT is not the admitted Git blob.
    if any(component.is_symlink() for component in (candidate, *candidate.parents)):
        return None
    path = candidate.resolve()
    return path if path.is_relative_to(ROOT) else None


def evidence(value):
    item = dict(value) if isinstance(value, dict) else {"path": value}
    name = item.get("path") or item.get("repo_path") or item.get("source") or item.get("href")
    label = item.get("label") or item.get("title") or name or "Evidence pending"
    if isinstance(name, str) and re.match(r"^https://[^/\s]+(?:/|$)", name):
        return {"label": label, "href": name, "exists": True, "external": True}
    path = resolve_path(name)
    if path is None or not path.is_file():
        return {"label": label, "exists": False}
    rel = path.relative_to(ROOT).as_posix()
    return {"label": item.get("label") or item.get("title") or path.name,
            "path": rel, "href": f"{REPOSITORY}/blob/main/{rel}",
            "exists": True, "sha256": digest(path)}


def verify_gate(value, loop_id):
    name = value.get("path") or value.get("repo_path") if isinstance(value, dict) else value
    path = resolve_path(name)
    if path is None or not path.is_file():
        return {"state": "pending", "verified": False,
                "problems": ["Advisor gate not yet recorded."], "file_count": 0}
    source = evidence(path.relative_to(ROOT).as_posix())
    try:
        gate = read(path)
        if not isinstance(gate, dict):
            raise ValueError("Gate must be an object.")
    except (ValueError, OSError) as exc:
        return {"state": "running", "verified": False, "file_count": 0,
                "source": source, "problems": [f"Unreadable gate: {exc}"]}
    problems = []
    files = gate.get("files")
    if not isinstance(files, dict) or not files:
        problems.append("Gate has no source-hash inventory.")
        files = {}
    for rel, expected in files.items():
        target = resolve_path(rel, inventory=True)
        if target is None:
            problems.append(f"Forbidden or non-repository-relative source: {rel}")
        elif not isinstance(expected, str) or not re.fullmatch(r"[a-f0-9]{64}", expected):
            problems.append(f"Invalid source digest: {rel}")
        elif not target.is_file():
            problems.append(f"Missing source: {rel}")
        elif digest(target) != expected:
            problems.append(f"Changed source: {rel}")
    if gate.get("loop") != str(loop_id).lower():
        problems.append("Gate must identify this loop in lower case.")
    state = gate.get("status", "pending")
    if state not in STATES:
        problems.append("Unknown gate status.")
        state = "running"
    if state in {"accepted", "limited"}:
        for field in ("claim", "scope", "target_verdict"):
            if not isinstance(gate.get(field), str) or not gate[field].strip():
                problems.append(f"Gate has no authoritative {field}.")
        if not isinstance(gate.get("equations"), list):
            problems.append("Gate has no authoritative equation list.")
    verified = not problems and state in {"accepted", "limited"}
    return {"state": state if verified or state not in {"accepted", "limited"} else "running",
            "verified": verified, "problems": problems, "file_count": len(files),
            "source": source, "claim": gate.get("claim"), "equations": gate.get("equations"),
            "scope": gate.get("scope"), "target_verdict": gate.get("target_verdict"),
            "limitations": gate.get("limits", gate.get("limitations", []))}


def scaffold():
    return [{"id": letter, "title": f"Goal {letter} · title pending" if letter in "IJK" else f"Goal {letter} · select after I–K",
             "description": "The advisor will supply the frozen contract." if letter in "IJK" else "Selection waits for the first three goals and their two-loop reviews.",
             "loops": [{"id": f"{letter}{number}", "title": "Forward and reverse evidence pending",
                        "status": "pending" if letter in "IJK" else "deferred"} for number in (1, 2)]}
            for letter in "IJKLM"]


def prepare():
    path = ROUND / "site-data.json"
    live = read(path) if path.is_file() else {}
    if not isinstance(live, dict):
        raise ValueError("Site data must be an object.")
    incoming = live.get("goals", [])
    if not isinstance(incoming, list) or any(not isinstance(g, dict) for g in incoming):
        raise ValueError("Goals must be a list of objects.")
    ids = [str(g.get("id", "")).upper() for g in incoming]
    if len(ids) != len(set(ids)) or any(i not in "IJKLM" or len(i) != 1 for i in ids):
        raise ValueError("Goal IDs must uniquely identify I, J, K, L or M.")
    updates = dict(zip(ids, incoming))
    goals = scaffold()
    loops = []
    for goal in goals:
        update = deepcopy(updates.get(goal["id"], {}))
        members = update.pop("loops", [])
        if not isinstance(members, list) or any(not isinstance(v, dict) for v in members):
            raise ValueError("Loops must be a list of objects.")
        keys = [str(v.get("id", "")).upper() for v in members]
        allowed = {goal["id"] + "1", goal["id"] + "2"}
        if len(keys) != len(set(keys)) or not set(keys).issubset(allowed):
            raise ValueError("Loop IDs must uniquely match their parent goal.")
        loop_updates = dict(zip(keys, members))
        goal.update({k: v for k, v in update.items() if k not in {"id", "status"}})
        if members and goal["id"] in {"L", "M"} and not update.get("description"):
            goal["description"] = "Selected from the first three completed goals. Read each loop for the contract and review."
        for loop in goal["loops"]:
            loop.update({k: v for k, v in loop_updates.get(loop["id"], {}).items() if k != "id"})
            review = verify_gate(loop.get("gate"), loop["id"])
            requested = str(loop.get("status", "pending")).lower()
            requested = {"in_progress": "running", "planned": "pending"}.get(requested, requested)
            loop["status"] = review["state"] if review["verified"] else "running" if requested in {"accepted", "limited"} else requested if requested in STATES else "pending"
            loop["gate_review"] = review
            if review["verified"]:
                for field in ("claim", "equations", "scope", "target_verdict"):
                    loop[field] = deepcopy(review[field])
            loop["equations"] = as_list(loop.get("equations"))
            loop["limitations"] = as_list(loop.get("limitations")) + [x for x in as_list(review.get("limitations")) if x not in as_list(loop.get("limitations"))]
            loop["evidence"] = [evidence(v) for v in as_list(loop.get("evidence"))]
            loops.append(loop)
        statuses = [v["status"] for v in goal["loops"]]
        goal["status"] = "accepted" if all(s == "accepted" for s in statuses) else "limited" if all(s in {"accepted", "limited"} for s in statuses) else "running" if any(s in {"accepted", "limited", "running"} for s in statuses) else "deferred" if all(s == "deferred" for s in statuses) else "pending"
    by_id = {v["id"].lower(): v for v in loops}
    contributions = []
    for index, item in enumerate(as_list(live.get("contributions"))):
        item = deepcopy(item) if isinstance(item, dict) else {"title": str(item)}
        linked = by_id.get(str(item.get("loop", "")).lower())
        item["id"] = item.get("id", f"result-{index + 1}")
        item["gate_review"] = linked["gate_review"] if linked else {"verified": False, "state": "pending", "problems": ["No Round21 loop links this contribution to a gate."]}
        item["status"] = linked["status"] if linked else "pending"
        item["classification"] = "Supported model-specific result" if item["gate_review"]["verified"] else "Candidate contribution"
        if linked and linked["gate_review"]["verified"]:
            for field in ("claim", "equations", "scope", "target_verdict"):
                item[field] = deepcopy(linked[field])
            for field in ("derivation", "failure", "workaround", "limitations", "evidence"):
                item.setdefault(field, deepcopy(linked.get(field)))
        item["equations"] = as_list(item.get("equations"))
        item["evidence"] = [v if isinstance(v, dict) and "exists" in v else evidence(v)
                            for v in as_list(item.get("evidence"))]
        item["sources"] = [evidence(v) for v in as_list(item.get("sources") or item.get("source"))]
        contributions.append(item)
    data = {k: deepcopy(v) for k, v in live.items() if k not in {"goals", "contributions", "completed_research_loops", "accepted_research_loops", "total_research_loops", "repository"}}
    data.update({"schema": "ym21-source-bound-view-v1", "repository": REPOSITORY,
                 "title": live.get("title", "Five goals. Ten paired reviews."),
                 "summary": live.get("summary", "Continue the model calculations, test their exceptions, and state what each result establishes."),
                 "novelty_note": live.get("novelty_note", "These are contributions to this workbench. Scientific priority remains unverified."),
                 "goals": goals, "contributions": contributions, "total_research_loops": len(loops),
                 "completed_research_loops": sum(v["gate_review"]["verified"] for v in loops),
                 "accepted_research_loops": sum(v["status"] == "accepted" for v in loops),
                 "limited_research_loops": sum(v["status"] == "limited" for v in loops),
                 "source_binding": evidence("research/round21/site-data.json"),
                 "build": {"source_sha256": digest(path) if path.is_file() else None}})
    repair = deepcopy(live.get("c2_repair", {}))
    if not isinstance(repair, dict):
        repair = {"summary": str(repair)}
    repair["evidence"] = [evidence(v) for v in as_list(repair.get("evidence"))]
    # A release inventory/replay is reported separately from the ten physics loops.
    data["c2_repair"] = repair
    data["supporting_docs"] = [evidence(v) for v in as_list(live.get("supporting_docs"))]
    data.setdefault("next_roadmap", {})["evidence"] = [evidence(v) for v in as_list(data.get("next_roadmap", {}).get("evidence"))]
    return data


SCRIPT = r'''/* Round21 source-bound research view. Generated; edit build_site.py. */
(() => {
  'use strict';
  const prior = window.ResearchObservatory;
  if (!prior) return;
  const D = __DATA__;
  const list = v => Array.isArray(v) ? v : v ? [v] : [];
  const words = v => typeof v === 'object' && v !== null ? Object.entries(v).map(([k,x])=>`${k.replaceAll('_',' ')}: ${list(x).map(words).join('; ')}`).join(' · ') : String(v ?? '');
  const e = v => words(v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const safeUrl = value => { try { const u=new URL(String(value)); return u.protocol==='https:'&&!u.username&&!u.password?e(u.href):'#research/round21-review'; } catch { return '#research/round21-review'; } };
  const route = (r,t,cls='') => `<a class="${e(cls)}" href="#research/${e(r)}">${e(t)}</a>`;
  const labels = {accepted:'Supported in model',limited:'Supported with limits',pending:'Pending',running:'Under review',deferred:'Select later',rejected:'Rejected'};
  const badge = status => `<span class="rc-badge rc-${e(status)}">${e(labels[status]||status)}</span>`;
  const paragraph = v => v ? `<p>${e(v)}</p>` : '';
  const allLoops = () => D.goals.flatMap(g=>g.loops);
  const byId = id => allLoops().find(l=>l.id.toLowerCase()===String(id).toLowerCase());
  const format = v => e(words(v).replace(/\b(alpha|beta|epsilon|kappa|tau|eta|Gamma|Delta|omega|Omega|hbar|infty)\b/g,token=>({alpha:'α',beta:'β',epsilon:'ε',kappa:'κ',tau:'τ',eta:'η',Gamma:'Γ',Delta:'Δ',omega:'ω',Omega:'Ω',hbar:'ℏ',infty:'∞'}[token])).replace(/<=/g,'≤').replace(/>=/g,'≥').replace(/\|\|/g,'‖'));
  const formula = v => `<figure class="rc-formula"><div class="rc-equation" role="math" aria-label="${e(v)}">${format(v)}</div><details class="rc-original"><summary>Original expression</summary><code>${e(v)}</code></details></figure>`;
  const sources = v => list(v).map(s=>s.exists?`<a class="rc-source" href="${safeUrl(s.href)}" target="_blank" rel="noopener noreferrer">${e(s.label)} ↗</a>`:`<span class="r21-missing">${e(s.label)} · unavailable</span>`).join('');
  const ordered = v => `<ol class="r21-steps">${list(v).map(x=>`<li>${paragraph(x)}</li>`).join('')}</ol>`;
  const limits = v => list(v).length ? `<div class="r21-limits"><h3>Limits</h3><ul>${list(v).map(x=>`<li>${e(x)}</li>`).join('')}</ul></div>` : '';
  function gate(g){return `<div class="rc-gate">${badge(g?.state||'pending')}<p>${g?.verified?`${g.file_count} evidence files match this gate. The narrow statement passed review; its target verdict is separate.`:e(list(g?.problems).join(' ')||'Advisor review pending.')}</p>${sources(g?.source?[g.source]:[])}${g?.source?.sha256?`<details class="rc-digest"><summary>Recorded gate fingerprint</summary><code>${e(g.source.sha256)}</code></details>`:''}</div>`;}
  const verdict = v => v ? `<p class="r21-verdict"><strong>Target verdict</strong> ${e(v)}</p>` : '';
  const title = (k,t,summary) => `<header class="rc-heading"><p class="rc-kicker">${e(k)}</p><h1>${e(t)}</h1>${paragraph(summary)}</header>`;
  const provenance = c => c.origin_type ? `<div class="r21-origin"><p class="rc-kicker">${e(c.origin_type)}</p><p><strong>Contribution here</strong> ${e(c.local_contribution)}</p><p><strong>Prior-work boundary</strong> ${e(c.prior_work_limit)}</p></div>` : '';
  function modelTable(){return `<section class="rc-section"><div class="rc-section-heading"><h2>Four models. Keep their conclusions separate.</h2></div><p>The shared positive reference E_star permits an energy comparison. It does not identify different states, generators or coupling profiles.</p><div class="r21-table-wrap" role="region" aria-label="Research model boundaries" tabindex="0"><table class="r21-table"><thead><tr><th scope="col">Model and loops</th><th scope="col">Definition</th><th scope="col">Energy scale</th><th scope="col">What still needs proof</th></tr></thead><tbody>${list(D.models).map(m=>`<tr><th scope="row">${e(m.title)}<div class="r21-inline-links">${list(m.loops).map(id=>route('round21-'+id.toLowerCase(),id)).join(' ')}</div></th><td>${e(m.definition)}</td><td>${e(m.energy)}</td><td>${e(m.boundary)}</td></tr>`).join('')}</tbody></table></div></section>`;}
  function parameterTable(id){const rows=list(D.parameters).filter(p=>!id||list(p.loops).includes(id));return `<div class="r21-table-wrap" role="region" aria-label="${id?e(id)+' ':''}Variable definitions" tabindex="0"><table class="r21-table r21-parameters"><thead><tr><th scope="col">Symbol</th><th scope="col">Role and units</th><th scope="col">Definition and boundary</th></tr></thead><tbody>${rows.map(p=>`<tr><th scope="row">${format(p.symbol)}</th><td><strong>${e(p.role)}</strong><br>${e(p.units)}</td><td>${e(p.definition)}</td></tr>`).join('')}</tbody></table></div>`;}
  function openQuestions(){const n=D.next_roadmap||{};return `<section class="rc-section r21-open"><p class="rc-kicker">Next decisions</p><h2>${e(n.title||'What remains open')}</h2>${paragraph(n.summary)}${list(n.goals).length?ordered(n.goals):''}<ul>${list(D.open_questions).map(v=>`<li>${e(v)}</li>`).join('')}</ul><div class="rc-sources">${sources(n.evidence)}${sources(D.supporting_docs)}</div></section>`;}
  function variables(){return `${title('Round21 · definitions and model boundaries','Every variable has a role.','A new symbol can specify a model, a measurement or a coordinate change. It does not replace an unproved physical matching or convergence premise.')}${modelTable()}${parameterTable()}${shared()}`;}
  function result(c,index){return `<article class="rc-result r21-result" id="r21-contribution-${e(c.id)}"><div class="rc-result-meta"><span class="rc-index">${String(index+1).padStart(2,'0')}</span>${badge(c.status)}</div><p class="r21-classification">${e(c.classification)}</p><h3>${e(c.title||c.loop||'Contribution pending')}</h3>${paragraph(c.claim||c.summary)}${provenance(c)}${list(c.equations).map(formula).join('')}${verdict(c.target_verdict)}<p class="rc-scope"><strong>Applies to</strong> ${e(c.scope||'Scope awaits the reviewed statement.')}</p><details class="rc-details"><summary>Step-by-step derivation, exceptions and evidence</summary><div class="rc-detail-body">${ordered(c.derivation||c.steps)}${exceptions(c)}${limits(c.limitations)}${gate(c.gate_review)}<div class="rc-sources">${sources(c.sources)}${sources(c.evidence)}</div></div></details>${c.loop?route('round21-'+String(c.loop).toLowerCase(),'Open '+String(c.loop).toUpperCase()+' review →','rc-text-link'):''}</article>`;}
  function exceptions(v){return v.failure||v.workaround?`<div class="rc-repair"><h3>Failure and repair</h3>${v.failure?`<h4>Failed premise or counterexample</h4>${paragraph(v.failure)}`:''}${v.workaround?`<h4>Workaround and its conditions</h4>${paragraph(v.workaround)}`:''}</div>`:'';}
  function goals(){return `<div class="rc-goals">${D.goals.map((g,i)=>`<article class="rc-goal"><div class="rc-goal-letter" aria-hidden="true">${e(g.id)}</div><div class="rc-goal-main"><div class="rc-goal-top">${badge(g.status)}<span class="rc-mini">Goal ${i+1} / 5</span></div><h3>${e(g.title)}</h3>${paragraph(g.description)}<div class="rc-loop-links">${g.loops.map(l=>route('round21-'+l.id.toLowerCase(),l.id+' · '+labels[l.status],'rc-loop-link rc-'+l.status)).join('')}</div></div></article>`).join('')}</div>`;}
  function shared(){return `<aside class="r21-shared"><p class="rc-kicker">Conditions shared across directions</p><h2>Compare at one physical scale.</h2><p>Keep a fixed positive physical energy reference. State each added parameter, its units, and the model it changes. A conditional or deformed generator needs a matching argument before it describes the original dynamics.</p><p>Forward derivation and reverse reconstruction check the same contract. Agreement between implementations does not supply independent physical evidence.</p></aside>`;}
  function c2(){const c=D.c2_repair||{};return `<section class="rc-checkpoint"><div><span class="rc-checkpoint-dot" aria-hidden="true"></span><strong>C2 reproducibility repair</strong></div>${paragraph(c.summary||c.result||'Release inventory and replay status pending.')}${c.status?paragraph('Recorded release status: '+c.status):''}<div class="rc-sources">${sources(c.evidence)}</div><p class="rc-footnote">This release repair is separate from the ten research loops. The historical gates remain unchanged.</p></section>`;}
  function home(){return `<section class="rc-hero"><div><p class="rc-kicker">Round21 · paired physics research</p><h1>${e(D.title)}</h1><div class="rc-hero-deck">${paragraph(D.summary)}</div><div class="rc-hero-actions">${route('contributions','Inspect contributions','rc-button')}${route('round21-roadmap','Open the five-goal roadmap →','rc-hero-link')}</div></div><aside class="rc-score"><span class="rc-score-number">${D.completed_research_loops}<span>/ 10</span></span><strong>Source-verified loop reviews</strong><p>${D.accepted_research_loops} supported · ${D.limited_research_loops} supported with limits</p><div class="rc-score-dots" aria-hidden="true">${allLoops().map(l=>`<i class="rc-${e(l.status)}"></i>`).join('')}</div><small>Completed reviews measure this research cycle. They do not measure progress toward a continuum mass-gap proof.</small></aside></section><div class="r21-novelty"><strong>What is new here</strong>${paragraph(D.novelty_note)}<p>A successful validation supports its stated result. It does not mean the original research target was solved.</p></div>${c2()}${modelTable()}<section class="rc-section"><div class="rc-section-heading"><h2>Model-specific contributions</h2>${route('contributions','All contributions and limits →','rc-text-link')}</div>${D.contributions.length?`<div class="rc-results rc-results-all">${D.contributions.map(result).join('')}</div>`:`<div class="rc-empty"><h3>Evidence is still being prepared.</h3><p>Reviewed statements will appear with their equations, scope and source gate.</p></div>`}</section><section class="rc-section"><div class="rc-section-heading"><h2>Five goals, two loops each</h2></div><p class="rc-process-note">Each second loop follows its first-loop review. Goals L and M are selected after goals I, J and K finish.</p>${goals()}</section>${openQuestions()}${shared()}`;}
  function contributions(){return `${title('Round21 · contribution ledger','Results, exceptions and limits.',D.novelty_note)}<p class="r21-priority">The ledger records workbench contributions. Scientific priority remains unverified unless the linked review establishes a specific primary-source comparison.</p>${D.contributions.length?`<div class="rc-results rc-results-all">${D.contributions.map(result).join('')}</div>`:paragraph('No contributions have been supplied yet.')}${shared()}`;}
  function roadmap(){return `${title('Round21 · adaptive roadmap','Five goals, ten paired loops.','Inspect the claim, common scale, failed premise and review for each loop.')}<p class="rc-process-note">Loop 2 is selected after loop 1. The final two goals follow the completed reviews of the first three goals.</p>${goals()}${openQuestions()}${shared()}`;}
  function review(){return `${title('Round21 · evidence review','Trace each result to its evidence.','Gate acceptance and research-target success are separate decisions.')}<div class="r21-review-note"><p>The site checks the exact source-hash inventory when it is built. Missing files, stale hashes, wrong loop IDs and interpreter caches cannot support an accepted label.</p><p>Source agreement alone is not a mathematical proof. Read the reports, assumptions and skeptical decision linked for each result.</p>${sources([D.source_binding])}</div>${c2()}<div class="rc-review-grid">${allLoops().map(l=>`<article class="rc-review-card"><h2>${e(l.id)} · ${e(l.title)}</h2>${verdict(l.target_verdict)}${gate(l.gate_review)}${route('round21-'+l.id.toLowerCase(),'Read the statement and steps →','rc-text-link')}</article>`).join('')}</div>`;}
  function loopPage(l){return `${title('Round21 · '+l.id,l.title,l.claim||'The reviewed statement has not yet been recorded.')}<div class="rc-loop-status">${badge(l.status)}${route('round21-roadmap','Back to roadmap','rc-text-link')}</div>${verdict(l.target_verdict)}<p class="rc-scope r21-loop-scope"><strong>Applies to</strong> ${e(l.scope||'Scope pending.')}</p>${l.equations.map(formula).join('')}${provenance(l)}<details class="rc-details r21-variable-details"><summary>Variable definitions and units for ${e(l.id)}</summary><div class="rc-detail-body">${parameterTable(l.id)}</div></details><section class="rc-section"><h2>Step-by-step derivation</h2>${list(l.derivation||l.steps).length?ordered(l.derivation||l.steps):paragraph('Read the bound forward and reverse reports when they become available.')}</section>${l.forward||l.reverse?`<div class="rc-pair-cards"><section><h2>Forward derivation</h2>${paragraph(l.forward)}</section><section><h2>Reverse reconstruction</h2>${paragraph(l.reverse)}</section></div>`:''}<section class="rc-section">${exceptions(l)}${limits(l.limitations)}</section><section class="rc-section"><h2>Evidence and skeptical review</h2>${gate(l.gate_review)}<div class="rc-sources">${sources(l.evidence)}</div>${l.reproduction?`<h3>Reproduce this loop</h3><p>Use a new output directory. A replay adds no research loop.</p><pre class="r21-command"><code>${e(l.reproduction)}</code></pre>`:''}</section>${route('round21-roadmap','← Back to the five-goal roadmap','rc-text-link')}`;}
  const pages={home:'Current research',contributions:'Contributions','round21-roadmap':'Five-goal roadmap','round21-review':'Evidence review','round21-variables':'Variables and models'};
  const aliases={'review20-home':'home',contributions20:'contributions'};
  const ownRoute = r => Object.hasOwn(pages,r)||/^round21-[i-m][12]$/.test(r)&&!!byId(r.slice(8));
  const nav = r => `<nav class="rc-nav" aria-label="Round21 research navigation">${Object.entries(pages).map(([key,label])=>`<a href="#research/${key}"${r===key?' aria-current="page"':''}>${e(label)}</a>`).join('')}${route('review20-home','Round20 history')}</nav>`;
  function history(r){return `<div class="rc-history-notice">Round20 research record. ${route('home','Return to Round21 →')} · ${route('contributions20','Round20 contributions')}</div>`+prior.render(aliases[r]).replaceAll('href="#research/home"','href="#research/review20-home"').replaceAll('href="#research/contributions"','href="#research/contributions20"');}
  function wireHistoricalH1(){
    // Retain the archived interaction using Round20's published calculator.
    const historic=window.ResearchContributions,input=document.getElementById('rc-h1-q');
    if(!input||!historic?.data?.goals?.flatMap(g=>g.loops).find(l=>l.id==='H1')?.gate_review?.verified)return;
    input.oninput=()=>{const q=Number(input.value);if(!Number.isFinite(q)||q<.1||q>.95)return;const v=historic.h1Value(q),positive=v.margin>0,label=document.getElementById('rc-h1-q-value'),readout=document.getElementById('rc-h1-readout'),plot=document.getElementById('rc-h1-plot');if(label)label.textContent=q.toFixed(3);if(readout)readout.innerHTML=`<div class="rc-h1-number ${positive?'':'rc-h1-insufficient'}"><span>${positive?'Sufficient lower bound':'No positive lower bound from this certificate'}</span><strong>${positive?`gap / α ≥ ${v.margin.toFixed(6)}`:'Certificate insufficient'}</strong><p>${positive?'Within the declared summable strip model.':`Signed certificate margin: ${v.margin.toFixed(6)}. This does not establish physical gap closure.`}</p></div><div class="rc-h1-budget"><span>Omitted-face budget B(q)</span><strong>${v.budget.toFixed(6)}</strong></div>`;if(plot)plot.innerHTML=historic.h1Plot(q);if(input.setAttribute)input.setAttribute('aria-valuetext',`${q.toFixed(3)}, ${positive?'positive sufficient certificate':'certificate insufficient'}`);};
  }
  function render(r='home'){
    if(Object.hasOwn(aliases,r))return history(r);
    if(!ownRoute(r))return prior.render(r);
    const body=r==='home'?home():r==='contributions'?contributions():r==='round21-roadmap'?roadmap():r==='round21-review'?review():r==='round21-variables'?variables():loopPage(byId(r.slice(8)));
    return `<div class="rc20 r21">${nav(r)}${body}<footer class="rc-footer"><div><strong>Yang–Mills Workbench</strong><p>Round21 · statements, conditions and evidence</p></div><div>${route('round21-review','Evidence review')}${route('review20-home','Round20 history')}${route('contributions20','Round20 contributions')}<a href="${safeUrl(D.repository)}" target="_blank" rel="noopener noreferrer">Repository ↗</a></div></footer></div>`;
  }
  function afterRender(){const r=location.hash.split('/')[1]||'home';if(ownRoute(r))document.title=(pages[r]||r.slice(8).toUpperCase()+' · Paired loop')+' · Yang–Mills Workbench';else if(Object.hasOwn(aliases,r)){document.title='Round20 research record · Yang–Mills Workbench';wireHistoricalH1();}else prior.afterRender();}
  window.ResearchRound21={render,afterRender,data:D,format,safeUrl};
  window.ResearchObservatory={...prior,render,afterRender};
})();
'''


STYLES = r'''
/* Additive Round21 styles; Round20 assets and historical pages are unchanged. */
.r21 .rc-hero h1{max-width:670px;font-size:clamp(43px,5.8vw,68px)}
.r21 .rc-hero-deck p{color:#d7e4d9}
.r21-novelty{padding:22px 26px;margin:20px 0;border-left:4px solid #b58c43;background:#fbf4e3;border-radius:0 13px 13px 0;color:#5f522e}
.r21-novelty>strong{font:24px/1.2 Georgia,serif;color:#564625}
.r21-novelty p{font-size:13px;max-width:920px}
.r21 .r21-classification{font-size:10px;letter-spacing:.035em;font-weight:700;color:#617a67}
.r21 .r21-result:before{background:linear-gradient(90deg,#c89c4c,#78a98e)}
.r21 .r21-result h3{min-height:0;font-size:27px}
.r21 .r21-verdict{font-size:13px;line-height:1.65;padding:13px 15px;background:#f1f3e8;border:1px solid #d7dec8;border-radius:9px;color:#465b35}
.r21-verdict strong{display:block;text-transform:uppercase;font-size:10px;letter-spacing:.055em;margin-bottom:4px}
.r21-shared{border:1px solid #d1dfd5;border-radius:17px;padding:28px 30px;margin:38px 0;background:#edf3ed}
.r21-shared h2{font-size:30px}
.r21-shared p{font-size:13px;max-width:850px;color:#586e5d}
.r21-steps{padding:0 0 0 25px;margin:22px 0;max-width:950px;counter-reset:r21step}
.r21-steps li{padding:0 0 9px 8px;color:#526b56}
.r21-steps li::marker{font-weight:750;color:#648166}
.r21-steps p{font-size:14px;line-height:1.8;overflow-wrap:anywhere}
.rc-detail-body .r21-steps{padding-left:20px}
.rc-detail-body .r21-steps p{font-size:12px}
.r21 .r21-limits{margin:22px 0;padding:18px 20px;border:1px solid #e4d6b5;background:#fffaf0;border-radius:10px}
.r21 .r21-limits h3,.r21 .rc-repair h3{font-size:20px;margin:0 0 12px}
.r21 .r21-limits ul{padding-left:18px;font-size:13px;line-height:1.8;color:#766544}
.r21 .r21-limits li{margin:5px 0}
.r21 .rc-detail-body .r21-limits{padding:14px}
.r21 .rc-detail-body .r21-limits ul{font-size:12px}
.r21-loop-scope{background:#eef3ef;padding:19px 22px;border-radius:12px;color:#526959;font-size:14px}
.r21-priority,.r21-review-note{font-size:14px;color:#5d725e;max-width:920px;padding:19px 22px;border:1px solid #d6e1d5;border-radius:12px;background:#f0f4ec;margin-bottom:28px}
.r21-missing{display:block;font-size:11px;color:#866538;margin:5px 0;overflow-wrap:anywhere}
.r21 .rc-equation{font-size:18px;line-height:1.8}
.r21 .rc-detail-body .rc-repair{margin-top:18px}
.r21 .rc-result>.rc-text-link{display:inline-block;margin-top:19px}
.r21 .rc-review-grid{margin-top:26px}
.r21 .rc-review-card h2{font-size:23px}
@media(max-width:760px){.r21 .rc-hero h1{font-size:51px}.r21-shared{padding:23px}.r21-novelty{padding:19px 21px}.r21 .rc-hero-deck p{font-size:14px}.r21 .r21-result h3{font-size:26px}}
@media(max-width:520px){.r21 .rc-hero h1{font-size:44px}.r21-shared{padding:21px 18px}.r21-shared h2{font-size:26px}.r21-steps{padding-left:21px}.r21-steps li{padding-left:3px}.r21-steps p{font-size:13px}.r21 .r21-limits{padding:15px}.r21-novelty{padding:18px}.r21 .rc-equation{font-size:16px}.r21-priority,.r21-review-note{padding:16px;font-size:13px}}
.r21 .r21-origin{margin:17px 0;padding:15px 17px;background:#f1f5ed;border:1px solid #dce4d3;border-radius:10px}
.r21 .r21-origin p{font-size:12px;line-height:1.7;margin:7px 0}
.r21 .r21-origin .rc-kicker{color:#627849;font-size:10px;line-height:1.6}
.r21 .r21-table-wrap{overflow-x:auto;max-width:100%;border:1px solid #d5e0d3;border-radius:12px;margin:22px 0;background:#fff}
.r21 .r21-table{border-collapse:collapse;width:100%;min-width:730px;font-size:12px;line-height:1.75;text-align:left}
.r21 .r21-table th,.r21 .r21-table td{padding:15px 17px;vertical-align:top;border-bottom:1px solid #e0e7dc}
.r21 .r21-table thead th{background:#edf3e8;color:#496141;font-weight:700;font-size:11px}
.r21 .r21-table tbody th{font-weight:600;width:20%;color:#35543c}
.r21 .r21-table td{color:#5a6c58}
.r21 .r21-table tbody tr:last-child>*{border-bottom:0}
.r21 .r21-inline-links{display:flex;gap:8px;flex-wrap:wrap;margin-top:10px}
.r21 .r21-inline-links a{font-size:11px;color:#4f7450;text-decoration:underline;text-underline-offset:3px}
.r21 .r21-variable-details{margin:26px 0}
.r21 .r21-variable-details .rc-detail-body{padding:1px 14px}
.r21 .r21-parameters{min-width:620px}
.r21 .r21-parameters tbody th{width:20%}
.r21 .r21-parameters td:nth-child(2){width:30%}
.r21 .r21-open{padding:27px 30px;background:#f4f4e9;border:1px solid #dedfc7;border-radius:15px}
.r21 .r21-open ul{padding-left:21px;font-size:13px;color:#5e6b53;line-height:1.85}
.r21 .r21-open li{padding:5px 0}
.r21 .r21-command{white-space:pre-wrap;overflow-wrap:anywhere;word-break:break-word;max-width:100%;padding:18px;background:#ecf1e8;border:1px solid #d6e0cf;border-radius:9px;font:12px/1.7 monospace;color:#36513a}
@media(max-width:520px){.r21 .r21-open{padding:21px 18px}.r21 .r21-table th,.r21 .r21-table td{padding:12px}.r21 .r21-origin{padding:13px}.r21 .r21-variable-details .rc-detail-body{padding:1px 7px}}
'''


def build():
    data = prepare()
    encoded = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")
    DIST.mkdir(exist_ok=True)
    (DIST / "research-round21.js").write_text(SCRIPT.replace("__DATA__", encoded), encoding="utf-8")
    (DIST / "research-round21.css").write_text(STYLES.lstrip("\n"), encoding="utf-8")
    print(json.dumps({"output": "dist/research-round21.js", "loops": data["total_research_loops"],
                      "verified": data["completed_research_loops"], "source": data["source_binding"].get("path")}))


if __name__ == "__main__":
    build()
