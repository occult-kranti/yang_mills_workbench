"""Verify explicit failed gates cannot disappear under Python optimization."""
from pathlib import Path
import json
import subprocess
import sys

root=Path(__file__).resolve().parent
cases=[]
for flags in ([],["-O"]):
    result=subprocess.run([sys.executable,*flags,str(root/"test_solver.py"),"--inject-failure"],
                          capture_output=True,text=True,timeout=60)
    passed=(result.returncode!=0 and '"status": "passed"' not in result.stdout
            and "deliberate failure must survive optimization" in result.stderr)
    cases.append({"optimized":bool(flags),"returncode":result.returncode,"negative_control_detected":passed,
                  "stdout":result.stdout,"stderr":result.stderr})
    if not passed:
        raise RuntimeError("deliberate failed gate was not detected")
report={"status":"passed","cases":cases}
(root/"output"/"optimized_failure_checks.json").write_text(json.dumps(report,indent=2)+"\n")
print(json.dumps({"status":"passed","negative_controls":len(cases)}))
