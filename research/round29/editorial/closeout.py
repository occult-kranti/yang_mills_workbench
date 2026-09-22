#!/usr/bin/env python3
"""Typeset the actual post-ten advisor decision; execute no research goals."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'papers/draft-02'
def require(condition,message):
 if not condition:raise ValueError(message)
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def tx(value):
 value=str(value).replace('–','--').replace('—','---')
 return ''.join({'&':r'\&','%':r'\%','$':r'\$','#':r'\#','_':r'\_','{':r'\{','}':r'\}','^':r'\textasciicircum{}','\\':r'\textbackslash{}'}.get(c,c) for c in value)
path=ROOT/'research/round29/advisor/roadmap.json';roadmap=json.loads(path.read_text())
require(roadmap['selected_after_reviewed_loops']==10,'Closeout requires ten reviewed investigations.')
require(roadmap['executed_future_loops']==0,'This release records future advice, not extra research.')
require(len(roadmap['goals'])==5,'The post-ten roadmap must contain the actual five selected goals.')
for name,digest in roadmap['gate_bindings'].items():require(sha(ROOT/name)==digest,'Roadmap gate binding mismatch: '+name)
text=r'''\section{Round29 closeout and the next five goals}
\label{sec:round29-closeout}
The five selected goal pairs are complete: AL1--AL2, AM1--AM2, AN1--AN2, AO1--AO2 and AQ1--AQ2. These are ten reviewed investigations, not ten independent discoveries. AM1's insufficient source-template transfer remains visible; AM2 supplies a separately proved alternative certificate. The last two pairs were chosen only after the first six reviews, and each second investigation responded to its preceding review. Scientific production stops at this checkpoint. Subsequent builds, evidence replays and presentation repairs do not count as research loops.

\subsection{What the completed cycle changes}
\begin{longtable}{@{}p{17mm}p{69mm}p{64mm}@{}}
\toprule Pair & Admitted change & Surviving boundary\\\midrule\endhead
AL & Exact complete-model scale dictionary and common-scale invariants; the declared weak-bare-coupling path leaves the sufficient regime. & Magnetic-only suppression changes the action. A failed sufficient certificate does not prove that the physical gap closes.\\\addlinespace
AM & A full four-site creation proof gives a unique finite-volume ground and gap at least $\alpha/16$ at both signs of $|\tau|\le10^{-8}$, with representation cutoffs removed. & The named external stability constants are not numerically evaluated. Finite-volume data alone do not construct a thermodynamic state; AQ is the separate extension.\\\addlinespace
AN & Specified deep-bulk translates of the old orthant state converge in local state norm to the compatible centered-box state, with independent outer cutoffs. & The original symbolic radius and independent HTW smallness remain; this is state identification under those conditions, not generator identification or all-boundary uniqueness.\\\addlinespace
AO & The actual old orthant Wilson vector has finite second spectral moment, belongs to the physical operator domain and has exact first energy $\alpha\omega(1-W^2)$. & Both inherited restrictions remain. Equality of second moments is unproved; this result is not automatically a statement about the new AQ state.\\\addlinespace
AQ & At the numerical cap, a full-lattice locally normal subsequential state has complete original-endpoint physical sector, gap at least $\alpha/16$, simple vacuum in its representation and original Wilson variance $\ge61999/250000>1/5$. & No uniqueness of all thermodynamic states, whole-sequence limit, translation invariance, old-state identity, Wilson moment/domain theorem, particle mass or continuum construction is inferred.\\\bottomrule
\end{longtable}

The stronger full-GNS AQ2 conclusion explicitly uses AM2's separately reviewed full-Hilbert finite-volume gap. The reverse AQ2 variance refinement is separately attributed in that chapter; the table uses the common forward floor. Gauvin's Supplement A.10 and the matched unbounded-onsite dynamics sources retain credit for the general limiting strategy. HNM labels locate this project's checked model application and constants, without settling scientific priority.

The two state branches must remain distinct. AO refers to the inherited conditional orthant state with $|\tau|<\tau_*$ and $|\tau|\le2^{-16}$. AN's bulk identification further retains the HTW hypothesis. AQ uses the fully numerical cap $|\tau|\le10^{-8}$ and a selected centered full-lattice subsequence; it has not been identified with those older states. A simple vacuum in the chosen AQ representation is not a theorem that every thermodynamic limit equals it. The new numerical interval also does not repair AL's weak-bare-coupling obstruction. Fixed positive $\alpha$, $\hbar$, lattice spacing and energy reference remain part of each physical claim.

\subsection{Prospective roadmap: planned and unexecuted}
The following five goals are the advisor's actual post-ten selection in \repo{research/round29/advisor/roadmap.json}. Their order is qualitative scientific dependency and utility, not a novelty score or a percentage of the Clay problem. The first AT deliverable is especially bounded, even though state identification and the weak-coupling strategy have higher scientific priority. Each first contract must be frozen prospectively; each second investigation is selected only after independent directions and skeptical review. None of these future goals is executed in this release.
'''
for goal in sorted(roadmap['goals'],key=lambda x:x['rank']):
 require(goal['status']=='planned_not_executed','A future goal was incorrectly marked executed.')
 text+=r'\subsubsection{'+str(goal['rank'])+'. HNM roadmap '+tx(goal['id'])+': '+tx(goal['title'])+'}\n'
 for key,label in [('target','Target'),('missing_premise','Missing premise'),('proposed_first_loop_test','Prospective first test'),('second_loop_rule','Adaptive second test'),('exact_model','Exact model'),('reason_for_rank','Reason for priority')]:
  text+=r'\textbf{'+label+'.} '+tx(goal[key])+'\n\n'
 text+=r'\textbf{Limits.} '+tx(' '.join(goal['limitations']))+'\n\n'
text+=r'''The current priorities preserve the deferred AP identity and the finite-graph heat evaluation as separate questions. Improving a conservative constant is not automatically an extra research pair. All later conclusions still require their own prospective contracts, source dictionary and actual reviewed evidence.
'''
(OUT/'sections/round29-closeout.tex').write_text(text)
(OUT/'closeout-inputs.json').write_text(json.dumps({'roadmap':str(path.relative_to(ROOT)),'sha256':sha(path),'gate_bindings':roadmap['gate_bindings'],'future_goals_executed':0},indent=2)+'\n')
print(json.dumps({'goal_pairs_completed':5,'reviewed_investigations':10,'future_goals':[g['id'] for g in roadmap['goals']],'future_goals_executed':0}))
