"""AH2 semantic attack controls, independent of any outer checksum binding.

The same mutations must fail even if a file publisher coherently rebinds hashes.
These are verifier tests of the existing frozen result, not physics experiments.
"""
import argparse
import copy
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from reproduce import PREFIX, Validator, digest, semantics, require


def run(spec_name):
    validator = Validator()
    spec = validator.load(spec_name)
    require(spec.get("loop") == "ah2", "AH2 admission specification required")
    original = {side: validator.load(PREFIX + f"{side}/ah2/output/results.json")
                for side in ["forward", "reverse"]}
    rejected = []

    def attack(name, side, change, relations_only=False):
        result = copy.deepcopy(original[side])
        configuration = copy.deepcopy(spec["producers"][side])
        if relations_only:
            # These attacks must be detected by mathematical relations, not by
            # exact pins of the already-reported numerical constants.
            configuration["semantic_controls"] = [
                {"id": "schema-only", "pointer": "/schema", "equals": result["schema"]}]
        semantics(result, configuration)
        change(result)
        try:
            semantics(result, configuration)
        except ValueError:
            rejected.append({"name": name, "side": side, "relations_only": relations_only})
        else:
            raise ValueError("AH2 semantic attack admitted: " + name)

    attack("missing loaded channel", "forward", lambda r: r["blocks"]["C_without_minus_lambda_entries"].pop())
    attack("same-count wrong face coefficient", "forward",
           lambda r: r["blocks"]["C_without_minus_lambda_entries"][0].__setitem__(2, "1/4"))
    attack("wrong triplet physical metric", "reverse",
           lambda r: next(row for row in r["full_blocks"]["N_rows"] if row["kind"] == "triplet").__setitem__("metric", {"numerator": 1, "denominator": 1}))
    attack("Boolean basis identity", "reverse",
           lambda r: r["full_blocks"]["N_rows"][0].__setitem__("basis_id", True))
    attack("stationary component dropped", "forward", lambda r: r["uniform_inputs"].__setitem__("q", "0"), True)
    attack("second projector comparison omitted", "reverse", lambda r: r["envelopes"].__setitem__("p0_nested", {"numerator": 0, "denominator": 1}), True)
    attack("center defect omitted", "forward", lambda r: r["uniform_inputs"].__setitem__("delta", "0"), True)
    attack("feedback control falsely passes", "forward", lambda r: r["control_evidence"].__setitem__("positive_feedback_second_derivative_difference", "0"), True)
    attack("physical integrated leakage omitted", "forward", lambda r: r["fixtures"][25].__setitem__("physical_integrated_leakage_upper", "0"), True)
    attack("approximate denominator substituted", "reverse", lambda r: r["certificate_grid"][8].__setitem__("true_denominator", {"numerator": 1, "denominator": 1}), True)
    attack("negative true denominator", "forward", lambda r: r["uniform_inputs"].__setitem__("denominator", "-1"), True)
    attack("Boolean true denominator", "forward", lambda r: r["uniform_inputs"].__setitem__("denominator", True), True)
    attack("unsupported sharper all-time bound", "reverse", lambda r: r["join_certificate"].__setitem__("all_time_true_relative_upper", {"numerator": 1, "denominator": 1000000}), True)
    attack("zero initial outside source means invariance", "forward", lambda r: r["controls"].__setitem__("BP0_zero_means_B_zero", False))
    attack("nondiscriminating candidate erased", "forward", lambda r: r.__setitem__("nondiscriminating_controls", []))
    attack("certificate relabeled computed heat", "reverse", lambda r: r["scope"].__setitem__("actual_heat_errors_computed", True))
    attack("unproved full outside Gram", "reverse", lambda r: r["scope"].__setitem__("full_outside_Gram_evaluated", True))
    attack("finite graph promoted to continuum", "reverse", lambda r: r["scope"].__setitem__("continuum_gap", True))
    return {"status": "passed", "specification": spec_name,
            "specification_sha256": digest(validator.source(spec_name)),
            "semantic_mutations_rejected": len(rejected), "controls": rejected,
            "new_research_loops": 0,
            "scope": "Hash-independent semantic attacks on frozen AH2 data; no producer execution or new physics."}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--spec", default=PREFIX + "advisor/ah2-admission.json")
    args = parser.parse_args()
    print(json.dumps(run(args.spec), sort_keys=True))


if __name__ == "__main__":
    main()
