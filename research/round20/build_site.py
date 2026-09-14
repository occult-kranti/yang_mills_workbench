#!/usr/bin/env python3
"""Build a source-bound Round20 dashboard without changing scientific evidence.

Run from any directory: python research/round20/build_site.py
Editorial defaults live in site-content.json. The advisor owns site-data.json.
Accepted labels require an accepted gate and an exact, nonempty file inventory.
"""
from __future__ import annotations

import hashlib
import json
import re
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ROUND = ROOT / "research/round20"
DIST = ROOT / "dist"
STATES = {"accepted", "limited", "pending", "running", "rejected", "deferred"}


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def resolve_path(value, base=ROUND):
    if not isinstance(value, str) or not value:
        return None
    path = (ROOT / value if value.startswith("research/") else base / value).resolve()
    return path if path.is_relative_to(ROOT / "research") else None


def evidence(value, base=ROUND, branch="main"):
    item = dict(value) if isinstance(value, dict) else {"path": str(value)}
    name = item.get("path") or item.get("repo_path") or item.get("source")
    if name and str(name).startswith("https://"):
        return {"label": item.get("label") or item.get("title") or "Primary source", "href": name, "exists": True}
    path = resolve_path(name, base)
    if path is None or not path.is_file():
        return {"label": item.get("label") or name or "Evidence pending", "exists": False}
    rel = path.relative_to(ROOT).as_posix()
    return {"label": item.get("label") or item.get("title") or path.name, "path": rel,
            "href": f"https://github.com/occult-kranti/yang_mills_workbench/blob/{branch}/{rel}",
            "exists": True, "sha256": digest(path)}


def verify_gate(value, loop_id=None, base=ROUND, branch="main"):
    path_value = value.get("path") or value.get("repo_path") if isinstance(value, dict) else value
    path = resolve_path(path_value, base)
    if path is None or not path.is_file():
        return {"state": "pending", "verified": False, "problems": ["Advisor gate not yet recorded."]}
    gate = read(path)
    inventory = gate.get("files")
    problems = []
    if not isinstance(inventory, dict) or not inventory:
        problems.append("Gate has no source-hash inventory.")
        inventory = {}
    gate_base = ROOT / "research" / path.relative_to(ROOT / "research").parts[0]
    for rel, expected in inventory.items():
        target = resolve_path(rel, gate_base)
        if not isinstance(expected, str) or not re.fullmatch(r"[a-fA-F0-9]{64}", expected):
            problems.append(f"Invalid source digest: {rel}")
        elif target is None or not target.is_file():
            problems.append(f"Missing source: {rel}")
        elif digest(target) != expected.lower():
            problems.append(f"Changed source: {rel}")
    if loop_id and gate.get("loop") and str(gate["loop"]).lower() != str(loop_id).lower():
        problems.append("Gate loop identifier does not match this claim.")
    state = str(gate.get("status", "pending")).lower()
    if state not in STATES:
        state = "pending"
    verified = not problems and state in {"accepted", "limited"}
    if state in {"accepted", "limited"} and not verified:
        state = "running"
    return {"state": state, "verified": verified, "problems": problems,
            "file_count": len(inventory), "scope": gate.get("scope", ""),
            "source": evidence(path.relative_to(ROOT).as_posix(), branch=branch)}


def as_list(value):
    return value if isinstance(value, list) else [value] if value else []


def normalized_state(value):
    value = str(value or "pending").lower()
    return {"in_progress": "running", "in progress": "running", "planned": "pending"}.get(value, value)


def prepare():
    data = read(ROUND / "site-content.json")
    live_path = ROUND / "site-data.json"
    live = read(live_path) if live_path.exists() else {}
    # A milestone may contain only completed/current loops. Preserve the ten
    # planned slots rather than making unstarted goals disappear from the view.
    incoming_goals = {g["id"]: g for g in live.get("goals", [])}
    for goal in data.get("goals", []):
        incoming = incoming_goals.get(goal["id"], {})
        loop_updates = {l["id"]: l for l in incoming.get("loops", [])}
        for loop in goal.get("loops", []):
            loop.update(deepcopy(loop_updates.get(loop["id"], {})))
        goal.update({k: deepcopy(v) for k, v in incoming.items() if k != "loops"})
        if goal["id"] in {"G", "H"} and incoming.get("loops") and not incoming.get("description"):
            goal["description"] = "Selected from the first three completed goals. Open each loop for its statement, assumptions and evidence."
    data.update({k: deepcopy(v) for k, v in live.items() if k not in {"repository", "branch", "live_site", "goals"}})
    branch = data["branch"]
    data["source_binding"] = evidence("research/round20/site-data.json", branch=branch)
    loops = []
    for goal in data.get("goals", []):
        for loop in goal.get("loops", []):
            status = normalized_state(loop.get("status", "pending"))
            loop["gate_review"] = verify_gate(loop.get("gate"), loop.get("id"), branch=branch)
            if loop["gate_review"]["verified"]:
                status = loop["gate_review"]["state"]
            elif status in {"accepted", "limited"}:
                status = "running"
            loop["status"] = status if status in STATES else "pending"
            loop["evidence"] = [evidence(v, branch=branch) for v in as_list(loop.get("evidence"))]
            loop["equations"] = as_list(loop.get("equations"))
            loop["limitations"] = as_list(loop.get("limitations"))
            loops.append(loop)
        states = [v["status"] for v in goal.get("loops", [])]
        goal["status"] = ("accepted" if states and all(v == "accepted" for v in states)
                          else "limited" if states and all(v in {"accepted", "limited"} for v in states)
                          else "running" if any(v in {"accepted", "limited", "running"} for v in states)
                          else "deferred" if states and all(v == "deferred" for v in states) else "pending")
    by_id = {v["id"]: v for v in loops}
    for item in data.get("contributions", []):
        linked = by_id.get(item.get("loop"), {})
        item["gate_review"] = linked.get("gate_review") or verify_gate(item.get("gate"), item.get("loop"), branch=branch)
        classification = str(item.get("classification", "candidate hypothesis")).replace("_", " ").lower()
        if classification in {"accepted", "accepted within model", "model theorem", "theorem"}:
            classification = "accepted within model" if item["gate_review"]["verified"] else "candidate hypothesis"
        elif classification not in {"candidate hypothesis", "known method", "obstruction"}:
            classification = "candidate hypothesis"
        item["classification"] = classification
        item["equations"] = as_list(item.get("equations") or item.get("equation"))
        if item.get("loop") == "F2":
            # Reuse the exact gate-linked loop expression for the spotlight;
            # never reconstruct a scientific equation from prose.
            for expression in as_list(by_id.get("F2", {}).get("equations")):
                if isinstance(expression, str) and expression.startswith("H_tilde=") and expression not in item["equations"]:
                    item["equations"].append(expression)
        item["sources"] = [evidence(v, branch=branch) for v in as_list(item.get("source") or item.get("sources"))]
        item["novelty"] = "Scientific novelty not established by this audit."
    data["completed_research_loops"] = sum(v["status"] in {"accepted", "limited", "rejected"} and v["gate_review"]["verified"] for v in loops)
    data["accepted_research_loops"] = sum(v["status"] == "accepted" for v in loops)
    data["total_research_loops"] = len(loops)
    data["c2"] = {**(data.get("c2") if isinstance(data.get("c2"), dict) else {}),
                  "gate_review": verify_gate("research/round19/advisor/c2-gate.json", "c2", branch=branch)}
    data["c2"]["status"] = data["c2"]["gate_review"]["state"]
    data["audit_files"] = [evidence(v, branch=branch) for v in as_list(data.get("audit_files"))]
    clarification = ROUND / "advisor/f-conditional-space-clarification.md"
    if clarification.is_file():
        clarification_source = evidence(clarification.relative_to(ROOT).as_posix(), branch=branch)
        scope_text = ("Conditional three-link space SU(2)^3, with the exterior links fixed. "
                      "No equivalence to a gauge fixing of the full unfixed graph is proved; "
                      "the diffusion generator is not identified with physical Yang–Mills dynamics.")
        for loop in loops:
            if loop["id"] in {"F1", "F2"}:
                loop["scope_clarification"] = scope_text
                loop["evidence"].append(clarification_source)
        for item in data.get("contributions", []):
            if item.get("loop") in {"F1", "F2"}:
                item["scope_clarification"] = scope_text
                item["sources"].append(clarification_source)
    ledger_path = ROUND / "advisor/exception-ledger.json"
    if ledger_path.is_file():
        ledger = read(ledger_path)
        data["exception_ledger"] = {
            "entries": ledger.get("entries", []),
            "source": evidence(ledger_path.relative_to(ROOT).as_posix(), branch=branch),
        }
    data["inherited_stability"] = evidence("research/round13/advisor/weak-coupling-stability.md", branch=branch)
    data["build"] = {"schema": "ym20-source-bound-view-v1", "editorial_sha256": digest(ROUND / "site-content.json"),
                     "source_sha256": digest(live_path) if live_path.exists() else None}
    return data


SCRIPT = r'''/* Round20 contributions view. Generated by research/round20/build_site.py. */
(() => {
  'use strict';
  const prior = window.ResearchObservatory;
  if (!prior) return;
  const D = __DATA__;
  const e = v => String(v ?? '').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const list = v => Array.isArray(v) ? v : v ? [v] : [];
  const words = v => typeof v === 'object' ? Object.entries(v || {}).map(([k,x])=>`${k.replaceAll('_',' ')}: ${Array.isArray(x)?x.join('; '):typeof x==='object'?words(x):x}`).join(' · ') : String(v ?? '');
  const url = v => /^https:\/\//.test(String(v)) ? e(v) : '#research/contributions';
  const route = (r,t,cl='') => `<a class="${e(cl)}" href="#research/${e(r)}">${e(t)}</a>`;
  const labels = {accepted:'Accepted within model',limited:'Accepted with limits',running:'Under review',pending:'Pending',deferred:'Selected later',rejected:'Rejected'};
  const badge = (s,t) => `<span class="rc-badge rc-${e(s)}">${e(t || labels[s] || s)}</span>`;
  function displayFormula(value){
    // Typography only. Exact token boundaries keep names such as alphabetical
    // and metadata intact; the complete source expression remains copyable.
    const symbols={alpha:'α',beta:'β',delta:'δ',epsilon:'ε',kappa:'κ',tau:'τ',eta:'η',sigma:'σ',Gamma:'Γ',Delta:'Δ',DeltaS:'ΔS',omega:'ω',Omega:'Ω',Psi:'Ψ',hbar:'ℏ',infty:'∞',H_tilde:'H̃'};
    let text=words(value).replace(/(?<![A-Za-z])(alpha|beta|delta|epsilon|kappa|tau|eta|sigma|Gamma|DeltaS|Delta|omega|Omega|Psi|hbar|infty|H_tilde)(?![A-Za-z])/g,token=>symbols[token]);
    text=text.replace(/\|\|/g,'‖').replace(/<=/g,'≤').replace(/>=/g,'≥').replace(/\btensor\b/g,'⊗');
    return e(text).replace(/_([LMNH]|HL|GNS|box|ref|out|star|κ|∞|c|q|[0-9]+)(?![A-Za-z0-9_])/g,(_,sub)=>`<sub>${sub==='star'?'★':sub}</sub>`).replace(/\^([234])(?![0-9])/g,'<sup>$1</sup>').replace(/\^\(3\/2\)/g,'<sup>(3/2)</sup>');
  }
  const formula = text => `<figure class="rc-formula"><div class="rc-equation" role="math" aria-label="${e(words(text))}">${displayFormula(text)}</div><details class="rc-original"><summary>Original expression</summary><code>${e(words(text))}</code></details></figure>`;
  const links = items => list(items).filter(x=>x.exists).map(x=>`<a class="rc-source" href="${url(x.href)}" target="_blank" rel="noopener noreferrer">${e(x.label)} <span aria-hidden="true">↗</span></a>`).join('');
  const paragraph = value => value ? `<p>${e(words(value))}</p>` : '';
  const allLoops = () => list(D.goals).flatMap(g=>list(g.loops));
  const count = () => D.completed_research_loops || 0;
  const byId = id => allLoops().find(x=>String(x.id).toLowerCase()===String(id).toLowerCase());
  const title = (k,h,d) => `<header class="rc-heading"><p class="rc-kicker">${e(k)}</p><h1>${e(h)}</h1>${paragraph(d)}</header>`;
  function gate(g){
    if(!g?.source) return `<p class="rc-gate-pending">Advisor gate pending. This view does not confer acceptance.</p>`;
    return `<div class="rc-gate">${badge(g.state)}<p>${g.verified?`${g.file_count} evidence files match the recorded gate.`:e(list(g.problems).join(' '))}</p>${links([g.source])}<details class="rc-digest"><summary>Source fingerprint</summary><code>${e(g.source.sha256)}</code></details></div>`;
  }
  function article(item,index=0){
    const category=item.classification || 'candidate hypothesis',kind=category==='accepted within model'?'accepted':category==='obstruction'?'rejected':category==='known method'?'method':'pending';
    return `<article class="rc-result rc-result-${e(kind)}" id="contribution-${e(item.id)}"><div class="rc-result-meta"><span class="rc-index">${String(index+1).padStart(2,'0')}</span>${badge(kind,category)}</div><h3>${e(item.title)}</h3>${paragraph(item.summary || item.claim)}${list(item.equations).map(formula).join('')}<p class="rc-scope"><strong>Applies to</strong> ${e(words(item.scope || 'Scope awaits the advisor’s statement.'))}</p>${paragraph(item.implication)}${item.scope_clarification?`<p class="rc-scope-clarification"><strong>Conditional model</strong> ${e(item.scope_clarification)}</p>`:''}<details class="rc-details"><summary>Derivation, limits and evidence</summary><div class="rc-detail-body">${paragraph(item.derivation || 'Read the bound evidence for the derivation and its premises.')}${list(item.steps).length?`<ol>${list(item.steps).map(s=>`<li>${e(words(s))}</li>`).join('')}</ol>`:''}${item.failure || item.workaround?`<div class="rc-repair"><h4>Failed premise → repair</h4>${paragraph(item.failure)}${paragraph(item.workaround)}</div>`:''}${list(item.limitations).length?`<h4>Limits</h4><ul>${list(item.limitations).map(x=>`<li>${e(words(x))}</li>`).join('')}</ul>`:''}${gate(item.gate_review)}<div class="rc-sources">${links(item.sources)}</div><p class="rc-footnote">${e(item.novelty)}</p></div></details></article>`;
  }
  function goals(){return `<div class="rc-goals">${list(D.goals).map((g,i)=>`<article class="rc-goal"><div class="rc-goal-letter" aria-hidden="true">${e(g.id)}</div><div class="rc-goal-main"><div class="rc-goal-top">${badge(g.status)}<span class="rc-mini">Goal ${i+1} / ${list(D.goals).length}</span></div><h3>${e(g.title)}</h3>${paragraph(g.description)}<div class="rc-loop-links">${list(g.loops).map(l=>route(`round20-${l.id.toLowerCase()}`,`${l.id} · ${labels[l.status] || l.status}`,'rc-loop-link rc-'+l.status)).join('')}</div></div></article>`).join('')}</div>`;}
  function spiral(){
    const nodes=allLoops(), n=Math.max(nodes.length-1,1), phi=(1+Math.sqrt(5))/2;
    // Equal radial increments on a logarithmic spiral give equal arc-length
    // increments. This keeps inner labels apart without moving nodes off-curve.
    const pos=(i,side)=>{const r=24+i/n*93,t=.48+(Math.PI/2)*Math.log(r/24)/Math.log(phi),x=145+r*Math.cos(t),y=182+r*Math.sin(t);return {x:side==='f'?x:600-x,y};};
    const path=side=>Array.from({length:151},(_,i)=>{const p=pos(i/150*n,side);return `${i?'L':'M'}${p.x.toFixed(2)},${p.y.toFixed(2)}`;}).join(' ');
    return `<figure class="rc-spiral"><svg viewBox="0 0 600 370" role="img" aria-labelledby="rc-spiral-title rc-spiral-desc"><title id="rc-spiral-title">Paired forward and reverse research nodes</title><desc id="rc-spiral-desc">Two opposed golden logarithmic spirals organize ${nodes.length} research loops. Matching node labels identify the same loop. This geometry is an organizing analogy, not a physical result.</desc><text x="145" y="33" class="rc-svg-label">FORWARD DERIVATION</text><text x="455" y="33" class="rc-svg-label">REVERSE RECONSTRUCTION</text><path class="rc-spiral-path rc-forward" d="${path('f')}"/><path class="rc-spiral-path rc-reverse" d="${path('r')}"/>${nodes.map((l,i)=>{const a=pos(i,'f'),b=pos(i,'r');return `<path class="rc-pair-bridge" d="M${a.x.toFixed(2)},${a.y.toFixed(2)} H${b.x.toFixed(2)}"/><a href="#research/round20-${e(l.id.toLowerCase())}" aria-label="Open ${e(l.id)} paired loop, ${e(labels[l.status])}">${['f','r'].map(s=>{const p=pos(i,s);return `<g class="rc-spiral-node rc-${e(l.status)}"><circle cx="${p.x.toFixed(2)}" cy="${p.y.toFixed(2)}" r="13"/><text x="${p.x.toFixed(2)}" y="${p.y.toFixed(2)}">${e(l.id)}</text></g>`;}).join('')}</a>`;}).join('')}<rect x="218" y="302" width="164" height="49" rx="10" class="rc-scale-box"/><text x="300" y="322" class="rc-scale-title">Common scale: E★ &gt; 0</text><text x="300" y="339" class="rc-scale-sub">only after physical matching</text></svg><figcaption>${e(D.geometry_note)}</figcaption></figure>`;
  }
  function ledger(){const rows=[...list(D.obstructions),...list(D.exception_ledger?.entries).map(x=>({title:`${x.loop} · ${x.failed_premise}`,detail:x.executed_failure,workaround:x.repair,equation:x.equation,scope:x.scope}))];return `<section class="rc-section"><div class="rc-section-heading"><div><p class="rc-kicker">Where the argument stops</p><h2>Obstructions and repairs</h2></div><span class="rc-mini">Failures stay in the record</span></div><div class="rc-obstructions">${rows.map((x,i)=>`<details class="rc-obstruction"><summary><span class="rc-obstruction-no">${String(i+1).padStart(2,'0')}</span><span>${e(typeof x==='string'?x:x.title || x.id || 'Open obstruction')}</span><span class="rc-plus" aria-hidden="true">+</span></summary><div class="rc-detail-body">${paragraph(typeof x==='string'?'No workaround has been admitted for this obstruction.':x.detail || x.failure || x.description)}${x.workaround?`<h4>Workaround and applicability</h4>${paragraph(x.workaround)}`:''}${list(x.equations || x.equation).map(formula).join('')}${paragraph(x.limit || x.scope)}</div></details>`).join('')}</div><div class="rc-sources">${links(D.exception_ledger?.source?[D.exception_ledger.source]:[])}</div>${D.inherited_stability?.exists?`<aside class="rc-prior-result">${badge("method","Known inherited result")}<p>Round13’s qualitative homogeneous lattice stability result remains admitted under its small-local-interaction hypotheses. Explicit selected-strip constants remain a next target. H2 limits the global absolute-sum budget route.</p>${links([D.inherited_stability])}</aside>`:''}</section>`;}
  function scale(){const value=D.scale_register;return `<section class="rc-scale-panel"><div><p class="rc-kicker">One comparison, declared units</p><h2>The scale is part of the claim.</h2><p>α and E★ carry physical energy units. Static κ and a spiral node number do not supply a physical clock.</p></div><div>${value?Object.entries(value).map(([k,v])=>`<div class="rc-register"><strong>${displayFormula(k)}</strong><span>${e(words(v))}</span></div>`).join(''):`<div class="rc-register"><strong>E★ &gt; 0</strong><span>Keep the physical reference fixed across comparisons.</span></div><div class="rc-register"><strong>κ → physical time</strong><span>A matching argument remains required.</span></div>`}</div></section>`;}
  function h1Value(input){const q=Number(input);if(!Number.isFinite(q)||q<.1||q>.95)throw new RangeError('Illustration q must be between 0.1 and 0.95.');const budget=(2+5*q+5*q*q+6*q**3+3*q**4)/(24*(1-q)**3*(1+q)**2*(1+q*q));return {q,budget,margin:1/8-budget/64};}
  function h1Readout(q){const v=h1Value(q),positive=v.margin>0;return `<div class="rc-h1-number ${positive?'':'rc-h1-insufficient'}"><span>${positive?'Sufficient lower bound':'No positive lower bound from this certificate'}</span><strong>${positive?`gap / α ≥ ${v.margin.toFixed(6)}`:'Certificate insufficient'}</strong><p>${positive?'Within the declared summable strip model.':`Signed certificate margin: ${v.margin.toFixed(6)}. This does not establish physical gap closure.`}</p></div><div class="rc-h1-budget"><span>Omitted-face budget B(q)</span><strong>${v.budget.toFixed(6)}</strong></div>`;}
  function h1Plot(q){
    const value=h1Value(q),xmin=.1,xmax=.95,ymin=-.15,ymax=.13,x=v=>48+(v-xmin)/(xmax-xmin)*452,y=v=>20+(ymax-v)/(ymax-ymin)*162;
    const points=Array.from({length:171},(_,i)=>{const qi=xmin+i/170*(xmax-xmin);return `${i?'L':'M'}${x(qi).toFixed(2)},${y(h1Value(qi).margin).toFixed(2)}`;}).join(' '),outside=value.margin<ymin;
    return `<svg viewBox="0 0 550 230" role="img" aria-labelledby="rc-h1-chart-title rc-h1-chart-desc"><title id="rc-h1-chart-title">Signed sufficient-certificate margin as the action profile q changes</title><desc id="rc-h1-chart-desc">Floating illustration at fixed τ = 1/64. A positive margin supplies a lower bound within the model. A nonpositive margin is insufficient and does not establish gap closure. Current q ${q.toFixed(3)}, margin ${value.margin.toFixed(6)}${outside?', below the plotted range':''}.</desc><defs><clipPath id="rc-h1-chart-clip"><rect x="48" y="20" width="452" height="162"/></clipPath></defs><rect x="48" y="20" width="452" height="162" rx="4" class="rc-h1-chart-bg"/><rect x="${x(.7640035).toFixed(2)}" y="20" width="${(500-x(.7640035)).toFixed(2)}" height="162" class="rc-h1-chart-warning"/>${[.125,0,-.15].map(v=>`<path d="M48,${y(v).toFixed(2)} H500" class="rc-h1-grid ${v===0?'rc-h1-zero':''}"/><text x="39" y="${(y(v)+3).toFixed(2)}" text-anchor="end" class="rc-h1-axis">${v}</text>`).join('')}<path d="${points}" class="rc-h1-curve" clip-path="url(#rc-h1-chart-clip)"/><path d="M${x(q).toFixed(2)},20 V182" class="rc-h1-selector"/><circle cx="${x(q).toFixed(2)}" cy="${y(Math.max(ymin,value.margin)).toFixed(2)}" r="5" class="rc-h1-point ${value.margin<=0?'rc-h1-point-warning':''}"/>${[.1,.5,.7640035,.95].map(v=>`<text x="${x(v).toFixed(2)}" y="201" text-anchor="middle" class="rc-h1-axis">${v===.7640035?'qcrit':v}</text>`).join('')}<text x="48" y="12" class="rc-h1-axis">Certificate margin / α</text><text x="500" y="218" text-anchor="end" class="rc-h1-axis">q · action-profile parameter</text>${outside?'<text x="490" y="175" text-anchor="end" class="rc-h1-axis">point below plotted range</text>':''}</svg>`;
  }
  function h1Illustration(){const h=byId('H1');if(!h?.gate_review?.verified || h.status!=='accepted')return '';return `<section class="rc-h1"><div class="rc-section-heading"><div><p class="rc-kicker">H1 · Explore the continuous parameter</p><h2>How far does this certificate reach?</h2></div>${links([h.gate_review.source])}</div><p class="rc-h1-intro">Change the decay profile q while τ stays at 1/64. The curve illustrates the exact gated bound with floating-point arithmetic; it is not a new proof or a measured gap.</p><div class="rc-h1-layout"><div><label class="rc-h1-label" for="rc-h1-q">Action profile q <output id="rc-h1-q-value" for="rc-h1-q">0.500</output></label><input id="rc-h1-q" type="range" min="0.1" max="0.95" step="0.001" value="0.5" aria-describedby="rc-h1-domain"><div class="rc-h1-range-labels"><span>0.1 · faster decay</span><span>0.95 · slower decay</span></div><div id="rc-h1-readout" aria-live="polite" aria-atomic="true">${h1Readout(.5)}</div></div><figure class="rc-h1-chart"><div id="rc-h1-plot">${h1Plot(.5)}</div><figcaption id="rc-h1-domain">The exact boundary satisfies 0.764003 &lt; qcrit &lt; 0.764004. Failure of this sufficient certificate does not establish that the physical gap closes.</figcaption></figure></div><details class="rc-details"><summary>Exact formula, baseline and model scope</summary><div class="rc-detail-body">${formula('B(q) = (2+5q+5q^2+6q^3+3q^4) / [24(1-q)^3(1+q)^2(1+q^2)]')}${formula('certificate / alpha = 1/8 - B(q)/64')}<p>Exact baseline: q = 1/2 gives B = 107/135 and certificate / α = 973/8640. Positive certificate means gap / α is at least this value.</p><p>Fixed selected-strip reference, summable coefficients and fixed lattice spacing. q and τ are dimensionless profile parameters; α is the original lattice energy coefficient and E★ remains a fixed positive reference. The separate conditional-diffusion coefficient c is not equated with α.</p></div></details></section>`;}
  function wireH1(){const input=document.getElementById('rc-h1-q');if(!input||!byId('H1')?.gate_review?.verified)return;input.oninput=()=>{const q=Number(input.value);if(!Number.isFinite(q)||q<.1||q>.95)return;const label=document.getElementById('rc-h1-q-value'),readout=document.getElementById('rc-h1-readout'),plot=document.getElementById('rc-h1-plot');if(label)label.textContent=q.toFixed(3);if(readout)readout.innerHTML=h1Readout(q);if(plot)plot.innerHTML=h1Plot(q);if(input.setAttribute)input.setAttribute('aria-valuetext',`${q.toFixed(3)}, ${h1Value(q).margin>0?'positive sufficient certificate':'certificate insufficient'}`);};}
  function spotlight(){const rank={E2:0,F2:1,H2:2};const items=list(D.contributions).map((item,i)=>({item,rank:Object.hasOwn(rank,item.loop)?rank[item.loop]:10+i})).sort((a,b)=>a.rank-b.rank).map(x=>x.item);return `<section class="rc-section"><div class="rc-section-heading"><div><p class="rc-kicker">New in this investigation</p><h2>Results you can inspect.</h2></div>${route('contributions','All contributions →','rc-text-link')}</div>${items.length?`<div class="rc-results">${items.slice(0,3).map(article).join('')}</div>`:`<div class="rc-empty"><span class="rc-empty-symbol" aria-hidden="true">∴</span><h3>Results follow the review.</h3><p>The ten new loops begin from C2. Accepted equations will appear here only when their advisor gates match the evidence.</p>${route('round20-roadmap','Inspect the five-goal roadmap →','rc-text-link')}</div>`}<p class="rc-footnote">${e(D.novelty_note)}</p></section>`;}
  function c2(){const c=D.c2 || {}, s=c.status || 'pending';return `<div class="rc-checkpoint"><div><span class="rc-checkpoint-dot ${s==='accepted'?'rc-done':''}" aria-hidden="true"></span><strong>Inherited checkpoint · C2</strong> ${badge(s)}</div><p>${e(c.claim || (s==='accepted'?'The Round19 continuous static-coupling certificate has a source-bound advisor gate.':'The continuous static-coupling certificate is awaiting its final source-bound advisor gate.'))}</p>${route('paired-c2','Read the C2 result and scope →','rc-text-link')}</div>`;}
  function home(){return `<section class="rc-hero"><div class="rc-hero-copy"><p class="rc-kicker">${e(D.round_label)}</p><h1>${e(D.title)}</h1><p class="rc-hero-deck">${e(D.subtitle)}</p><div class="rc-hero-actions">${route('contributions','Inspect the contributions','rc-button')}${route('round20-roadmap','Follow the ten loops →','rc-hero-link')}</div></div><aside class="rc-score" aria-label="Research loop status"><span class="rc-score-number">${count()}<span>/ ${D.total_research_loops || 10}</span></span><strong>research loops reviewed</strong><p>${D.accepted_research_loops || 0} accepted within model</p><div class="rc-score-dots" aria-hidden="true">${allLoops().map(x=>`<i class="rc-${e(x.status)}"></i>`).join('')}</div><small>Loops count completed reviews,<br>not progress toward a mass-gap proof.</small></aside></section>${c2()}${spotlight()}${h1Illustration()}<section class="rc-section rc-roadmap-section"><div class="rc-section-heading"><div><p class="rc-kicker">The next five goals</p><h2>Two directions. One evidence check.</h2></div>${route('round20-roadmap','Open the full roadmap →','rc-text-link')}</div><div class="rc-roadmap-preview">${spiral()}<div><p class="rc-process-note">Each second loop is selected from the first loop’s reviewed result. The final two goals are selected after the first three goal pairs.</p>${goals()}</div></div></section>${scale()}${ledger()}`;}
  function contributions(){const items=list(D.contributions);return title('Round20 · Contribution ledger','Equations with their conditions.','A result is useful when its assumptions, failed alternatives and remaining limits are visible.')+`<div class="rc-classification">${badge('accepted','Accepted within model')}${badge('pending','Candidate hypothesis')}${badge('method','Known method')}${badge('rejected','Obstruction')}</div><p class="rc-footnote">${e(D.novelty_note)}</p>${items.length?`<div class="rc-results rc-results-all">${items.map(article).join('')}</div>`:`<div class="rc-empty"><h2>No new contribution gate has been recorded.</h2><p>The roadmap contains the next tests. Results will populate this page from reviewed evidence.</p></div>`}${h1Illustration()}${ledger()}`;}
  function roadmap(){return title('Round20 · Paired investigation','Five goals, ten research loops.','The roadmap changes when the evidence changes. Ordinary and optimized replays verify a loop; they do not count as extra research loops.')+`<div class="rc-roadmap-preview">${spiral()}<div>${goals()}</div></div>${h1Illustration()}${scale()}<section class="rc-section"><p class="rc-kicker">After the tenth research loop</p><h2>The skeptic’s roadmap update</h2>${paragraph(D.skeptic_summary || 'After ten reviewed research loops, the skeptic will separate accepted model results, candidate hypotheses, known methods and obstructions, then select the next work.')}${links(D.audit_files)}<p class="rc-footnote">${e(D.scope_note)}</p></section>`;}
  function evidencePage(){return title('Round20 · Review record','Every accepted label has a gate.','The dashboard checks the recorded SHA-256 inventory against the current evidence files. This is an evidence-integrity check, not a formal proof assistant.')+`<div class="rc-review-grid">${allLoops().map(l=>`<article class="rc-review-card"><h2>${e(l.id)} · ${e(labels[l.status])}</h2>${paragraph(l.claim)}${gate(l.gate_review)}<div class="rc-sources">${links(l.evidence)}</div></article>`).join('')}</div><section class="rc-section"><h2>Page source</h2>${links([D.source_binding,...list(D.audit_files)])}<p class="rc-footnote">${e(D.scope_note)}</p></section>`;}
  function loopPage(l){return title(`Round20 · ${l.id}`,l.title || `Paired loop ${l.id}`,l.claim)+`<div class="rc-loop-status">${badge(l.status)}<span class="rc-mini">One research loop · two independently reviewed directions</span></div><div class="rc-pair-cards"><section><p class="rc-kicker">01 · Forward derivation</p><h2>${e(l.forward_title || 'From assumptions to consequence')}</h2>${paragraph(l.forward || l.forward_summary || 'The frozen contract and forward evidence record this direction.')}</section><section><p class="rc-kicker">02 · Reverse reconstruction</p><h2>${e(l.reverse_title || 'From consequence back to premises')}</h2>${paragraph(l.reverse || l.reverse_summary || 'Independent reconstruction checks the premises, counterexamples and scale.')}</section></div><section class="rc-section"><h2>Statement and applicability</h2>${list(l.equations).map(formula).join('')}${paragraph(l.scope || l.gate_review?.scope)}${l.scope_clarification?`<p class="rc-scope-clarification"><strong>Conditional model</strong> ${e(l.scope_clarification)}</p>`:''}${paragraph(l.result)}<details class="rc-details"><summary>Derivation and failure/workaround record</summary><div class="rc-detail-body">${paragraph(l.derivation || 'Read the forward and reverse reports linked below for the recorded derivations.')}${paragraph(l.failure)}${paragraph(l.workaround)}${list(l.exceptions).map(x=>paragraph(words(x))).join('')}</div></details></section><section class="rc-section"><h2>Advisor gate and evidence</h2>${gate(l.gate_review)}<div class="rc-sources">${links(l.evidence)}</div></section>${list(l.limitations).length?`<section class="rc-section"><h2>What remains open</h2><ul>${list(l.limitations).map(x=>`<li>${e(words(x))}</li>`).join('')}</ul></section>`:''}${route('round20-roadmap','← Back to the five-goal roadmap','rc-text-link')}`;}
  const pages={home:'Research contributions',contributions:'Contribution ledger','round20-roadmap':'Five-goal roadmap','round20-review':'Evidence review'};
  const ownRoute = r => Object.hasOwn(pages,r) || /^round20-[a-z][12]$/.test(r) && !!byId(r.slice(8));
  const nav = active => `<nav class="rc-nav" aria-label="Current research navigation">${Object.entries(pages).map(([r,t])=>`<a href="#research/${r}"${active===r?' aria-current="page"':''}>${e(t)}</a>`).join('')}${route('review19-home','Round19 history')}</nav>`;
  function render(r='home'){
    if(r==='review19-home')return `<div class="rc-history-notice">Round19 research record. ${route('home','Return to current contributions →')}</div>`+prior.render('home');
    if(!ownRoute(r))return prior.render(r);
    const body=r==='home'?home():r==='contributions'?contributions():r==='round20-roadmap'?roadmap():r==='round20-review'?evidencePage():loopPage(byId(r.slice(8)));
    return `<div class="rc20">${nav(r)}${body}<footer class="rc-footer"><div><strong>Yang–Mills Workbench</strong><p>Claims, counterexamples and evidence.</p></div><div>${route('round20-review','Evidence review')}${route('review19-home','Round19 history')}${route('review18-home','Round18 history')}<a href="${url(D.repository)}" target="_blank" rel="noopener noreferrer">Repository ↗</a></div></footer></div>`;
  }
  function afterRender(){const r=location.hash.split('/')[1] || 'home';if(ownRoute(r)||r==='review19-home')document.title=(pages[r] || (r==='review19-home'?'Round19 research record':r.slice(8).toUpperCase()+' · Paired loop'))+' · Yang–Mills Workbench';else prior.afterRender();if(ownRoute(r))wireH1();}
  window.ResearchContributions={render,afterRender,data:D,spiral,displayFormula,h1Value,h1Plot};
  window.ResearchObservatory={...prior,render,afterRender};
})();
'''


def build():
    data = prepare()
    encoded = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")
    script = SCRIPT.replace("__DATA__", encoded)
    DIST.mkdir(exist_ok=True)
    (DIST / "research-contributions.js").write_text(script, encoding="utf-8")
    css = (DIST / "research-contributions.css").read_text(encoding="utf-8")
    standalone = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Research contributions · Yang–Mills Workbench</title><style>*{box-sizing:border-box}body{margin:0;background:#f5f6f2;color:#152923;font:16px/1.6 system-ui,sans-serif}main{max-width:1320px;padding:28px;margin:auto}button,a,summary{-webkit-tap-highlight-color:transparent}:focus-visible{outline:3px solid #bd822b;outline-offset:4px}@media(max-width:560px){main{padding:12px}}</style><style>'''+css+'''</style></head><body><main id="main"></main><script>window.ResearchObservatory={render(r){return '<div class="rc-history-notice"><h1>Historical research record</h1><p>This standalone file contains Round20. <a href="https://occult-kranti.github.io/yang_mills_workbench/#research/'+encodeURIComponent(r)+'">Open this route on the full workbench →</a></p><a href="#research/home">Back to current contributions</a></div>';},afterRender(){}};</script><script>'''+script+'''</script><script>function render(){const r=location.hash.split('/')[1]||'home';document.getElementById('main').innerHTML=window.ResearchObservatory.render(r);window.ResearchObservatory.afterRender();}addEventListener('hashchange',()=>{render();window.scrollTo(0,0)});render();</script></body></html>'''
    (ROUND / "overview.html").write_text(standalone, encoding="utf-8")
    if data["completed_research_loops"] == 10 and (DIST / "index.html").is_file():
        index_path = DIST / "index.html"
        index = index_path.read_text(encoding="utf-8")
        description = "Inspect C2 and ten paired research loops: finite-box state convergence, conditional three-link generators, decay-profile limits, exact equations and evidence."
        index = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="' + description + '">', index, count=1)
        index_path.write_text(index, encoding="utf-8")
    print(json.dumps({"source":data["source_binding"].get("path"),"loops":data["total_research_loops"],"reviewed":data["completed_research_loops"],"c2":data["c2"]["status"],"output":"dist/research-contributions.js"}))


if __name__ == "__main__":
    build()
