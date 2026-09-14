# Bounded documentation and integration review

No blocking route, model/units or command mismatch was found in the current
README, Round22 guide, index wiring or package scripts. This is source review,
not a completed build, release-data test or live-site verification. R2's
pending-review wording is intentional and should be updated only after its
admission. No current opposite R2 solution was read or producer file changed.

## Checked integration

- `README.md:7,15,19` and `research/round22/README.md:7,67` use the actual
  current routes: `journey`, `contributions`, `round22-roadmap`,
  `round22-review`, `round21-home` and `journey21`. The older overview aliases
  remain delegated through the inherited renderer chain. The historical
  navigation repair remains consistent with the earlier presentation follow-up.
- `dist/index.html:3,47–51` loads the Round22 stylesheet and orders the
  scripts correctly: Round21, old journey, Round22 data, Round22 renderer,
  then the application. Thus the current renderer captures the complete
  historical chain before the application first renders. The new data asset
  must be generated before this wired index is served as the completed release;
  its pending build is not treated as a defect in this staging phase.
- `package.json:6–10` matches the documented build, test and launch commands.
  The actual Pages builder is `scripts/build_pages.py`: `npm run build`
  copies existing `dist` assets and does not generate scientific data.
  Both guides correctly put `build_claim_map.py` and `build_site.py` before
  it. The three named Node suites exist and correspond to the declared scripts.
- The replay flags in `README.md:134–138` and the Round22 guide's lines
  42–48 match the parsers. The optimized replay correctly supplies both
  parent `-O` and `--optimized`, which enables `-O` in producer subprocesses.
  The full runner's twenty implementations and per-output byte comparisons
  describe its code, not an assertion that the pending full replay passed.
- `README.md:11–15,119` and the Round22 guide's lines 28–36 keep the models
  separate. They distinguish energy-valued historical lambda from Q's
  dimensionless lambda, retain O/R's delta=alpha/8, and do not transfer Q's
  gap or positivity to R. R's initial H0+D is explicitly distinguished from
  the full operator with the residual. Endpoint, interacting-ground and
  continuum limitations remain visible.

## Small documentation clarifications

1. `README.md:7` still labels the current journey “Toward Yang–Mills. One
   proof at a time.”, the older journey title. Its destination is correct,
   but “Round22 research journey” would match the current page more clearly.
2. `README.md:132` and `research/round22/README.md:40` should say the replay
   output directory must be **outside the repository checkout** as well as
   fresh and absolute. `reproduce.py:44` rejects an absolute path inside
   the repository. The displayed `/absolute/new/...` examples are compatible;
   the missing qualification can confuse readers choosing their own paths.

Neither clarification blocks the reviewed source integration. Before final
publication, finish the already planned ten-gate/claim-map/three-goal-roadmap
sequence, update the pending R2 wording to its actual verdict, build the real
data and Pages tree, and execute the bound full UI/release checks. This review
does not count those pending actions as passed and adds zero research loops.
