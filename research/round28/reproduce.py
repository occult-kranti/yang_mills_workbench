"""Source-complete admission and replay of the completed Round28 prefix.

An empty admission registry is intentional before scientific review. Hashes and
fixtures establish reproducibility, not truth or completion of Yang--Mills.
Every check uses explicit exceptions and remains active with python -O.
"""
import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

sys.dont_write_bytecode = True
# Frozen AI3 rational endpoints exceed Python's default 4300-digit parsing
# limit. Retain a finite limit while admitting these exact, source-bound values.
if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(100000)
ROOT = Path(__file__).resolve().parents[2]
PREFIX = "research/round28/"
BASE = "a7f4b8dd42ce0f31f2442c068815f6d1f75ade1a"
HEX = re.compile(r"[0-9a-f]{64}\Z")
LABEL = re.compile(r"[a-z]+[1-9][0-9]*\Z")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode()


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def nonempty_text(value, name):
    require(isinstance(value, str) and bool(value.strip()), "missing " + name)


def text_list(value, name, empty=False):
    require(isinstance(value, list) and (empty or bool(value)) and
            all(isinstance(item, str) and bool(item.strip()) for item in value), "invalid " + name)
    require(len(value) == len(set(value)), "duplicate " + name)


def reject_promotion(value):
    if isinstance(value, dict):
        for key, item in value.items():
            label = key.lower().replace("-", "_")
            promoted = label in {"solved_yang_mills", "yang_mills_solved", "clay_problem_solved"}
            promoted = promoted or ("continuum" in label and any(
                token in label for token in ["solved", "proven", "proved", "claim", "established"]))
            if promoted:
                require(item is False or item is None, "unsupported target upgrade: " + key)
            reject_promotion(item)
    elif isinstance(value, list):
        for item in value:
            reject_promotion(item)


def projection(record, role):
    fields = (["schema", "loop", "sequence", "goal", "goal_loop", "model", "verdict", "accepted", "limitations"]
              if role == "gate" else ["schema", "loop", "model", "accepted", "verdict", "supported", "limitations"])
    return hashlib.sha256(encoded({key: record.get(key) for key in fields})).hexdigest()


def pointer(value, path):
    require(isinstance(path, str) and (path == "" or path.startswith("/")), "invalid JSON pointer")
    for part in path.split("/")[1:] if path else []:
        require(not re.search(r"~(?![01])", part), "invalid JSON pointer escape")
        key = part.replace("~1", "/").replace("~0", "~")
        if isinstance(value, list):
            require(re.fullmatch(r"0|[1-9][0-9]*", key) is not None, "invalid array pointer")
            require(int(key) < len(value), "missing array control")
            value = value[int(key)]
        else:
            require(isinstance(value, dict) and key in value, "missing semantic control: " + path)
            value = value[key]
    return value


def exact(value):
    if isinstance(value, dict) and set(value) == {"numerator", "denominator"}:
        require(type(value["numerator"]) is int and type(value["denominator"]) is int and value["denominator"] > 0,
                "invalid exact fraction")
        return Fraction(value["numerator"], value["denominator"])
    if isinstance(value, dict) and "exact" in value:
        value = value["exact"]
    require(type(value) in [int, str], "exact rational operand required")
    return Fraction(value)


def operand(result, expression, depth=0):
    require(depth < 20 and isinstance(expression, dict) and len(expression) == 1, "invalid rational expression")
    operation, argument = next(iter(expression.items()))
    if operation == "pointer":
        return exact(pointer(result, argument))
    if operation == "constant":
        return exact(argument)
    if operation == "length":
        collection = pointer(result, argument)
        require(isinstance(collection, (dict, list)), "collection length required")
        return Fraction(len(collection))
    require(operation in {"sum", "product", "difference", "quotient", "minimum", "maximum", "absolute", "power"}
            and isinstance(argument, list) and bool(argument),
            "unknown rational expression")
    values = [operand(result, item, depth + 1) for item in argument]
    if operation in {"minimum", "maximum"}:
        return min(values) if operation == "minimum" else max(values)
    if operation == "absolute":
        require(len(values) == 1, "unary absolute expression required")
        return abs(values[0])
    if operation == "sum":
        return sum(values, Fraction(0))
    if operation == "product":
        answer = Fraction(1)
        for value in values:
            answer *= value
        return answer
    require(len(values) == 2, "binary rational expression required")
    if operation == "difference":
        return values[0] - values[1]
    if operation == "power":
        require(values[1].denominator == 1 and 0 <= values[1] <= 64, "bounded nonnegative integer exponent required")
        return values[0] ** int(values[1])
    require(values[1] != 0, "zero rational denominator")
    return values[0] / values[1]


def semantics(result, specification):
    reject_promotion(result)
    scope = pointer(result, specification.get("scope_pointer", "/scope"))
    require((isinstance(scope, str) and bool(scope.strip())) or (isinstance(scope, dict) and bool(scope)), "producer scope absent")
    controls = specification.get("semantic_controls")
    require(isinstance(controls, list) and bool(controls), "required semantic controls absent")
    seen = set()
    for control in controls:
        require(isinstance(control, dict), "malformed semantic control")
        identity = control.get("id")
        nonempty_text(identity, "control identity")
        require(identity not in seen, "duplicate semantic control")
        seen.add(identity)
        require("equals" in control, "missing expected semantic value")
        require(encoded(pointer(result, control.get("pointer"))) == encoded(control["equals"]),
                "semantic control failed: " + identity)
    # Exact relations supplement labels with actual arithmetic. Booleans and
    # binary floats cannot silently become rational evidence.
    for relation in specification.get("rational_relations", []):
        nonempty_text(relation.get("id"), "relation identity")
        require(relation["id"] not in seen, "duplicate relation identity")
        seen.add(relation["id"])
        left, right = operand(result, relation.get("left")), operand(result, relation.get("right"))
        tests = {"eq": left == right, "ne": left != right, "lt": left < right,
                 "le": left <= right, "gt": left > right, "ge": left >= right}
        require(relation.get("op") in tests and tests[relation["op"]], "rational control failed: " + relation["id"])
    return len(seen)


def replay_artifacts(destination, stored_directory, artifacts):
    """Validate every fresh output tree, then compare declared auxiliary bytes."""
    require(destination.is_absolute() and ".." not in destination.parts, "invalid fresh output path")
    require(destination.is_dir() and not any(path.is_symlink() for path in [destination, *destination.parents]),
            "missing/linked fresh output directory")
    paths = list(destination.rglob("*"))
    require(not any(path.is_symlink() for path in paths), "linked fresh scientific output")
    require(not any(part in {"__pycache__", ".pytest_cache", ".mypy_cache", ".venv", "node_modules"}
                    for path in [destination, *paths] for part in path.relative_to(destination.parent).parts)
            and not any(path.suffix in {".pyc", ".pyo"} for path in paths), "cache/environment fresh output")
    require(all(path.is_file() or path.is_dir() for path in paths), "nonregular fresh output entry")
    files = {str(path.relative_to(destination)) for path in paths if path.is_file()}
    require(files == {"results.json", *artifacts}, "undeclared fresh scientific output file")
    for name, expected in artifacts.items():
        produced = destination / name
        require(produced.is_file() and not any(p.is_symlink() for p in [produced, *produced.parents]),
                "missing/linked fresh scientific artifact")
        require(produced.read_bytes() == (stored_directory / name).read_bytes() and digest(produced) == expected,
                "auxiliary producer replay bytes differ: " + name)


class Validator:
    def __init__(self, root=ROOT):
        self.root = Path(root).resolve()

    def source(self, name):
        nonempty_text(name, "source path")
        relative = Path(name)
        require(not relative.is_absolute() and ".." not in relative.parts, "nonportable source: " + name)
        require(not any(part in {"__pycache__", ".pytest_cache", ".mypy_cache", ".venv", "node_modules"}
                        for part in relative.parts) and relative.suffix not in {".pyc", ".pyo"}, "cache/environment source: " + name)
        path = self.root / relative
        require(path.is_file() and path.resolve().is_relative_to(self.root), "missing source: " + name)
        require(not any(part.is_symlink() for part in [path, *path.parents] if part.is_relative_to(self.root)),
                "linked source: " + name)
        return path

    def load(self, name):
        def unique(pairs):
            result = {}
            for key, value in pairs:
                require(key not in result, "duplicate JSON key: " + name + "/" + key)
                result[key] = value
            return result
        value = json.loads(self.source(name).read_text(), object_pairs_hook=unique,
                           parse_constant=lambda x: require(False, "nonfinite JSON: " + x))
        require(isinstance(value, dict), "JSON object required: " + name)
        return value

    def hashes(self, bindings, empty=False):
        require(isinstance(bindings, dict) and (empty or bool(bindings)), "empty/malformed bindings")
        for name, expected in bindings.items():
            require(isinstance(expected, str) and HEX.fullmatch(expected), "invalid SHA256: " + str(name))
            require(digest(self.source(name)) == expected, "changed source: " + name)

    def sequence(self, complete=False):
        cycle = self.load(PREFIX + "advisor/cycle.json")
        require(cycle.get("schema") == "ym28-cycle-v1" and cycle.get("baseline_commit") == BASE, "initial cycle identity")
        require((cycle.get("requested_goals"), cycle.get("loops_per_goal"), cycle.get("target_new_research_loops")) == (5, 2, 10),
                "cycle counts changed")
        self.hashes(cycle.get("sources"))
        selected = self.load(PREFIX + "advisor/sequence.json")
        progress = self.load(PREFIX + "advisor/progress.json")
        pairs = self.load(PREFIX + "advisor/goal-pairs.json")
        loops, done = selected.get("loops"), progress.get("completed_loops")
        text_list(loops, "selected loops", empty=True)
        text_list(done, "completed loops", empty=True)
        require(all(LABEL.fullmatch(loop) for loop in loops) and len(loops) <= 10, "invalid selected sequence")
        require(selected.get("target_loops") == progress.get("target_loops") == 10 and progress.get("requested_goals") == 5,
                "progress counts changed")
        require(done == loops[:len(done)] and len(done) <= len(loops) <= len(done) + 1, "completed prefix or active-loop order")
        active = loops[len(done)] if len(loops) > len(done) else None
        require(progress.get("active_loop") == active, "active loop disagrees with selected sequence")
        initial = pairs.get("initial_goals")
        require(isinstance(initial, list) and len(initial) == 3, "initial three goals missing")
        require([x.get("id") for x in initial] == [x.get("goal") for x in cycle["initial_goal_order"]], "initial goals changed")
        first_six = []
        for item, plan in zip(initial, cycle["initial_goal_order"]):
            require(item.get("loops") == [plan["first_loop"], plan["second_loop_label"]], "initial pair changed")
            first_six.extend(item["loops"])
        require(loops[:6] == first_six[:len(loops[:6])], "first three pairs reordered")
        later = pairs.get("later_goals")
        require(isinstance(later, list) and len(later) <= 2, "later goal count")
        require(len(done) >= 6 or not later, "later goals selected before six reviewed loops")
        full = list(first_six)
        for item in later:
            text_list(item.get("loops"), "later pair")
            require(len(item["loops"]) == 2, "two loops per later goal required")
            full.extend(item["loops"])
        require(len(set(full)) == len(full) and loops == full[:len(loops)], "selected loops disagree with goal pairs")
        if complete:
            require(len(done) == len(loops) == 10 and len(later) == 2 and active is None, "ten completed reviewed loops required")
        return loops, done, pairs

    def contract(self, loop):
        record = self.load(PREFIX + f"contracts/{loop}.json")
        require(record.get("schema") == "ym28-contract-v1" and record.get("loop") == loop, "contract identity")
        for key in ["model", "frozen_at", "acceptance", "goal"]:
            nonempty_text(record.get(key), "contract " + key)
        text_list(record.get("requirements"), "contract requirements")
        require(isinstance(record.get("parameters"), dict) and bool(record["parameters"]), "contract parameter domains absent")
        self.hashes(record.get("sources"))
        require({"AGENTS.md", PREFIX + "advisor/cycle.json", PREFIX + "methods/prospective-guide.md"} <= record["sources"].keys(),
                "contract required instruction/cycle dependency absent")
        reject_promotion(record)
        return record

    def manifests(self, loop, side, manifests, instruction_manifests):
        base = PREFIX + f"{side}/{loop}/"
        closure, snapshots, origins = {}, {}, {}
        names = manifests + instruction_manifests
        typed_aj1_sources = None
        text_list(manifests, "source manifests")
        text_list(instruction_manifests, "instruction manifests", empty=True)
        require(len(names) == len(set(names)), "duplicate manifest")
        for name in names:
            require(name.startswith(base + "inputs/"), "foreign input manifest")
            record = self.load(name)
            closure[name] = digest(self.source(name))
            typed_skill_origins = False
            if record.get("schema") == "ym28-aj1-forward-source-inventory-v1":
                require(loop == "aj1" and side == "forward" and name == base + "inputs/source-inventory.json"
                        and name in manifests, "foreign typed AJ1 source inventory")
                contract_name = PREFIX + "contracts/aj1.json"
                contract = self.contract(loop)
                expected_contract = digest(self.source(contract_name))
                require(record.get("contract") == contract_name and record.get("contract_sha256") == expected_contract,
                        "typed AJ1 contract identity")
                require(record.get("instructions") == base + "inputs/instruction-inventory.json"
                        and record["instructions"] in instruction_manifests, "typed AJ1 instruction inventory omitted")
                typed_aj1_sources = record.get("sources")
                self.hashes(typed_aj1_sources)
                required = {**contract["sources"], contract_name: expected_contract}
                require(all(typed_aj1_sources.get(origin) == expected for origin, expected in required.items()),
                        "typed AJ1 contract source coverage")
                expected_snapshots = {base + "inputs/" + origin: expected for origin, expected in typed_aj1_sources.items()}
                require(record.get("snapshots") == expected_snapshots, "typed AJ1 source/snapshot maps disagree")
                entries = [{"source": origin, "snapshot": base + "inputs/" + origin, "sha256": expected}
                           for origin, expected in typed_aj1_sources.items()]
            elif record.get("schema") == "ym28-aj1-forward-instructions-v1":
                require(loop == "aj1" and side == "forward" and name == base + "inputs/instruction-inventory.json"
                        and name in instruction_manifests and typed_aj1_sources is not None,
                        "foreign/unpaired typed AJ1 instruction inventory")
                repository = {base + "inputs/" + origin: expected for origin, expected in typed_aj1_sources.items()
                              if origin == "AGENTS.md" or origin.startswith(".codex/skills/")
                              or origin == PREFIX + "methods/prospective-guide.md"
                              or origin.startswith("research/round27/methods/historical-physics-panel/")}
                require(len(repository) == 11 and record.get("repository_instructions") == repository,
                        "typed AJ1 repository instruction coverage")
                require(all(snapshots.get(snapshot) == expected for snapshot, expected in repository.items()),
                        "typed AJ1 instruction is not a verified source snapshot")
                resources = record.get("installed_resources")
                require(isinstance(resources, list) and len(resources) == 6,
                        "typed AJ1 installed instruction coverage")
                entries = []
                resource_locators = set()
                for resource in resources:
                    require(isinstance(resource, dict) and set(resource) == {"path", "resource", "sha256"},
                            "typed AJ1 installed instruction entry")
                    require(isinstance(resource["path"], str) and resource["path"].startswith(base + "inputs/installed-methods/"),
                            "foreign typed AJ1 installed instruction snapshot")
                    locator = resource["resource"]
                    require(isinstance(locator, str) and locator not in resource_locators,
                            "missing/duplicate typed AJ1 skill resource")
                    resource_locators.add(locator)
                    entries.append({"source": locator, "snapshot": resource["path"], "sha256": resource["sha256"],
                                    "external_instruction_snapshot": True})
                typed_skill_origins = True
            elif "entries" in record:
                entries = record["entries"]
                require(isinstance(entries, list) and bool(entries), "empty snapshot entries")
            elif name in instruction_manifests:
                require(bool(record) and all(isinstance(entry, dict) and {"origin", "sha256"} <= entry.keys()
                                             for entry in record.values()), "unknown external instruction inventory format")
                entries = [{"source": entry["origin"], "snapshot": base + "inputs/instructions/" + filename,
                            "sha256": entry["sha256"], "external_instruction_snapshot": True}
                           for filename, entry in record.items()]
            else:
                entries = [{"source": origin, "snapshot": base + "inputs/" + origin, "sha256": value}
                           for origin, value in record.items()]
            for entry in entries:
                origin, snapshot, expected = entry.get("source"), entry.get("snapshot"), entry.get("sha256")
                require(isinstance(snapshot, str) and snapshot.startswith(base + "inputs/"), "foreign/missing snapshot")
                require(snapshot not in snapshots, "duplicate snapshot: " + snapshot)
                self.hashes({snapshot: expected})
                snapshots[snapshot] = expected
                closure[snapshot] = expected
                nonempty_text(origin, "snapshot origin")
                if entry.get("external_instruction_snapshot") is True:
                    if typed_skill_origins:
                        require(re.fullmatch(r"skill://flora-skills/root/\.codex/skills/remote-skills/skill-[0-9a-f]{32}/"
                                             r"(?:SKILL\.md|references/(?:[A-Za-z0-9][A-Za-z0-9_.-]*/)*[A-Za-z0-9][A-Za-z0-9_.-]*\.md)", origin)
                                is not None, "invalid typed AJ1 external skill locator")
                    else:
                        require(Path(origin).is_absolute(), "external instruction origin must be explicitly absolute")
                    # External origins are provenance, never a release-time dependency.
                else:
                    self.hashes({origin: expected})
                    require(origin not in origins or origins[origin] == expected, "conflicting source origin")
                    origins[origin] = expected
                    closure[origin] = expected
        return closure, snapshots, origins

    def preflight(self, loop):
        """Check only declared inputs; never read current producer mathematics."""
        contract = self.contract(loop)
        reports = {}
        for side in ["forward", "reverse"]:
            base = PREFIX + f"{side}/{loop}/"
            manifests = [base + "inputs/source-inventory.json"]
            instructions = [base + "inputs/instruction-inventory.json"] if (self.root / base / "inputs/instruction-inventory.json").is_file() else []
            closure, snapshots, origins = self.manifests(loop, side, manifests, instructions)
            required = {**contract["sources"], PREFIX + f"contracts/{loop}.json": digest(self.source(PREFIX + f"contracts/{loop}.json"))}
            require(all(origins.get(name) == expected for name, expected in required.items()), "missing contract-declared input snapshot")
            reports[side] = {"source_count": len(origins), "snapshot_count": len(snapshots), "validated_bindings": len(closure)}
        return {"status": "input_preflight_passed", "loop": loop, "new_research_loops": 0,
                "scope": "declared source and instruction snapshots only; no scientific execution or admission", "producers": reports}

    def scope(self, gate, review, pin):
        require(review.get("accepted") is True, "review did not admit evidence")
        require(isinstance(review.get("blocking_issues"), list) and not review["blocking_issues"], "review objections absent/malformed/unresolved")
        nonempty_text(review.get("supported"), "review supported statement")
        for role, record in [("gate", gate), ("review", review)]:
            text_list(record.get("limitations"), role + " limitations")
            require(any("continuum" in text.lower() for text in record["limitations"]), role + " continuum limitation absent")
            reject_promotion(record)
            require(projection(record, role) == pin.get(role + "_claim_projection"), "changed reviewed " + role + " target/scope")
        return list(dict.fromkeys(gate["limitations"] + review["limitations"]))

    def producer(self, loop, side, contract, spec, gate_bindings):
        base = PREFIX + f"{side}/{loop}/"
        result = self.load(base + "output/results.json")
        binding_field = spec.get("binding_field", "bindings")
        require(binding_field in {"bindings", "sources", "source_inventory", "aj1_provenance_pack"}, "unsupported producer binding field")
        bindings = result.get(binding_field)
        if binding_field == "aj1_provenance_pack":
            require(loop == "aj1" and side == "forward", "foreign AJ1 provenance adapter")
            provenance = result.get("provenance")
            require(isinstance(provenance, dict), "AJ1 producer provenance absent")
            pack_name = base + "inputs/input-pack-freeze.json"
            contract_name = PREFIX + "contracts/aj1.json"
            require(spec.get("input_pack") == pack_name, "AJ1 input-pack declaration absent")
            direct = {pack_name: provenance.get("input_pack_sha256"), base + "check.py": provenance.get("checker_sha256"),
                      contract_name: provenance.get("contract_sha256")}
            self.hashes(direct)
            pack = self.load(pack_name)
            require(pack.get("schema") == "ym28-aj1-forward-input-pack-freeze-v1"
                    and pack.get("contract_sha256") == direct[contract_name], "AJ1 frozen input-pack identity")
            self.hashes(pack.get("bindings"))
            require(type(provenance.get("input_binding_count")) is int
                    and provenance["input_binding_count"] == len(pack["bindings"]), "AJ1 executed input-pack count")
            source_name = base + "inputs/source-inventory.json"
            instruction_name = base + "inputs/instruction-inventory.json"
            require({source_name, instruction_name} <= pack["bindings"].keys(), "AJ1 pack omits executed manifests")
            source_record = self.load(source_name)
            require(source_record.get("schema") == "ym28-aj1-forward-source-inventory-v1", "AJ1 pack source convention")
            # manifests() below verifies the typed source map, exact copies and
            # contract coverage. The executed pack must bind every such copy.
            require(isinstance(source_record.get("snapshots"), dict) and all(
                pack["bindings"].get(name) == expected for name, expected in source_record["snapshots"].items()),
                "AJ1 executed pack omits required source snapshots")
            bindings = {**pack["bindings"], **source_record.get("sources", {}), **direct}
        elif binding_field == "source_inventory":
            require(isinstance(bindings, dict), "source inventory absent")
            bindings = dict(bindings)
            producer_bindings = result.get("producer_bindings")
            require(isinstance(producer_bindings, dict) and bool(producer_bindings), "split producer bindings absent")
            for name, value in producer_bindings.items():
                require(isinstance(name, str) and not Path(name).is_absolute() and ".." not in Path(name).parts,
                        "nonlocal split producer binding")
                require(base + name not in bindings or bindings[base + name] == value, "conflicting split bindings")
                bindings[base + name] = value
        if isinstance(bindings, dict) and set(bindings) == {"sources", "producer", "instructions"}:
            grouped = bindings
            instructions = spec.get("instruction_manifests", [])
            require(len(instructions) == 1 and grouped["instructions"] == self.load(instructions[0]),
                    "executed instruction inventory disagrees with frozen manifest")
            bindings = dict(grouped["sources"])
            for name, value in grouped["producer"].items():
                require(base + name not in bindings or bindings[base + name] == value, "conflicting producer bindings")
                bindings[base + name] = value
            for name, value in grouped["instructions"].items():
                bindings[base + "inputs/instructions/" + name] = value["sha256"]
        self.hashes(bindings)
        # Reports describe the execution and can be frozen after output is
        # written. Require the report in the immutable freeze below; requiring
        # it in self-produced output invents a dependency absent in AI3 forward.
        required = {base + "check.py", PREFIX + f"contracts/{loop}.json", *contract["sources"]}
        report_binding = spec.get("report_binding", "output_and_freeze")
        require(report_binding in {"output_and_freeze", "freeze"}, "unknown report binding convention")
        if report_binding == "output_and_freeze":
            required.add(base + "report.md")
        require(required <= bindings.keys(), "producer missing active script/contract source")
        source_manifests = spec.get("source_manifests")
        instruction_manifests = spec.get("instruction_manifests", [])
        closure, snapshots, origins = self.manifests(loop, side, source_manifests, instruction_manifests)
        if binding_field == "aj1_provenance_pack":
            require(all(pack["bindings"].get(name) == expected for name, expected in snapshots.items()),
                    "AJ1 executed pack omits source/instruction snapshot")
        require(set(source_manifests + instruction_manifests) <= bindings.keys(), "producer omitted executed input manifest")
        self.hashes(spec.get("required_snapshots"))
        require(spec["required_snapshots"] == snapshots, "required snapshot/instruction set changed")
        required_sources = {**contract["sources"], PREFIX + f"contracts/{loop}.json": digest(self.source(PREFIX + f"contracts/{loop}.json"))}
        require(all(origins.get(name) == value for name, value in required_sources.items()), "contract snapshot coverage incomplete")
        freeze_name = spec.get("freeze")
        require(freeze_name == base + "freeze.json", "current freeze path")
        freeze = self.load(freeze_name)
        require(freeze.get("loop") == loop, "freeze loop identity")
        freeze_field = spec.get("freeze_binding_field", "files" if "files" in freeze else "sha256")
        require(freeze_field in {"files", "sha256", "bindings"}, "unknown freeze binding convention")
        if freeze_field == "files":
            path_base = spec.get("freeze_path_base", "producer")
            require(path_base in {"producer", "repository"}, "unknown freeze path namespace")
            if path_base == "repository":
                require(loop == "ak1", "repository files convention is restricted to AK1")
                frozen = freeze["files"]
                require(isinstance(frozen, dict) and all(isinstance(name, str) and name.startswith(base)
                                                       for name in frozen), "foreign repository freeze member")
                owned = list((self.root / base).rglob("*"))
                require(not any(path.is_symlink() for path in owned), "linked producer freeze member")
                expected_files = {str(path.relative_to(self.root)) for path in owned
                                  if path.is_file() and str(path.relative_to(self.root)) != freeze_name}
                require(set(frozen) == expected_files, "AK1 freeze omits or adds owned file")
            else:
                frozen = {base + name: value for name, value in freeze["files"].items()}
        else:
            frozen = freeze.get(freeze_field)
        self.hashes(frozen)
        require({base + "check.py", base + "report.md", base + "output/results.json"} <= frozen.keys(), "freeze omits active producer")
        closure.update(bindings)
        closure.update(frozen)
        artifacts = {}
        artifact_files = spec.get("output_artifacts", {})
        require(isinstance(artifact_files, dict), "invalid auxiliary output declaration")
        if "artifact_sha256" in result:
            require(set(result["artifact_sha256"]) == set(artifact_files), "undeclared scientific output artifact")
        for filename, declaration in artifact_files.items():
            require(isinstance(filename, str) and re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*\.json", filename) is not None
                    and filename != "results.json", "escaping/cache/invalid auxiliary output filename")
            name = base + "output/" + filename
            expected = declaration.get("sha256")
            self.hashes({name: expected})
            convention = declaration.get("binding", "result_pointer")
            require(convention in {"result_pointer", "freeze"}, "unknown auxiliary output binding convention")
            if convention == "freeze":
                require(loop == "aj1" and (side, filename) in {("forward", "source-manifest.json"), ("reverse", "geometry.json")}
                        and "sha256_pointer" not in declaration, "foreign/fabricated freeze-only auxiliary binding")
                if side == "forward":
                    require(declaration.get("equals_result_pointer") == "/provenance"
                            and encoded(self.load(name)) == encoded(pointer(result, "/provenance")),
                            "AJ1 auxiliary manifest differs from executed provenance")
            else:
                require(pointer(result, declaration.get("sha256_pointer")) == expected, "result omits auxiliary artifact hash")
            require(frozen.get(name) == gate_bindings.get(name) == expected, "auxiliary output absent from freeze/gate closure")
            artifacts[filename] = self.load(name)
        if artifact_files:
            require(not any(path.is_symlink() for path in (self.root / base / "output").rglob("*")),
                    "linked stored scientific output")
            actual_outputs = {str(path.relative_to(self.root / base / "output"))
                              for path in (self.root / base / "output").rglob("*") if path.is_file()}
            require(actual_outputs == {"results.json", *artifact_files}, "undeclared additional scientific output file")
        for adoption in spec.get("adoption_records", []):
            require(adoption.startswith(base), "foreign producer adoption")
            require(adoption in closure, "adoption not bound by frozen producer closure")
            self.load(adoption)
        required_active = {str(path.relative_to(self.root)) for path in (self.root / base / "inputs").rglob("*") if path.is_file()}
        require(required_active <= closure.keys(), "input file missing from frozen producer closure")
        require(all(gate_bindings.get(name) == value for name, value in closure.items() if name.startswith(base)),
                "gate omits current producer closure")
        count = semantics(result, spec)
        structure = spec.get("structural_validator")
        structure_evidence = None
        if structure is not None:
            require(loop == "ah1" and structure.get("schema") == "ym28-ah1-generated-span-v1" and
                    structure.get("path") == PREFIX + "release/ah1_structure.py", "unknown structural validator")
            self.hashes({structure["path"]: structure.get("sha256")})
            from release.ah1_structure import verify
            structure_evidence = verify(result, side, artifacts)
        return {"side": side, "semantic_controls": count, "snapshot_count": len(snapshots),
                "results_sha256": digest(self.source(base + "output/results.json")),
                "output_artifacts": {name: value["sha256"] for name, value in artifact_files.items()},
                "structure_evidence": structure_evidence}

    def validate(self, loop):
        loops, completed, pairs = self.sequence()
        require(loop in loops, "loop never selected")
        position = loops.index(loop)
        contract = self.contract(loop)
        require(contract.get("sequence") == position + 1, "contract sequence")
        all_pairs = pairs["initial_goals"] + pairs["later_goals"]
        pair = next((item for item in all_pairs if loop in item["loops"]), None)
        require(pair is not None and contract.get("goal") == pair["id"] and
                contract.get("goal_loop") == pair["loops"].index(loop) + 1, "contract goal/pair identity")
        if position:
            predecessor = loops[position - 1]
            require({PREFIX + f"advisor/{predecessor}-gate.json", PREFIX + f"skeptic/{predecessor}.json"} <= contract["sources"].keys(),
                    "adaptive contract lacks immediately preceding admitted gate/review")
        registry = self.load(PREFIX + "release/admitted.json")
        require(registry.get("schema") == "ym28-reviewed-admission-pins-v1", "reviewed pin registry schema")
        pin = registry.get("loops", {}).get(loop)
        require(isinstance(pin, dict), "scientific review not registered: " + loop)
        require(digest(self.source(PREFIX + f"contracts/{loop}.json")) == pin.get("contract_sha256"), "frozen contract identity changed")
        admission_name = PREFIX + f"advisor/{loop}-admission.json"
        spec = self.load(admission_name)
        require(digest(self.source(admission_name)) == pin.get("admission_sha256"), "reviewed admission specification changed")
        require(spec.get("schema") == "ym28-admission-v1" and spec.get("loop") == loop, "admission specification identity")
        self.hashes(spec.get("bindings"))
        require(spec["bindings"].get(PREFIX + f"contracts/{loop}.json") == pin["contract_sha256"], "admission contract binding absent")
        gate = self.load(PREFIX + f"advisor/{loop}-gate.json")
        review = self.load(PREFIX + f"skeptic/{loop}.json")
        require(gate.get("schema") == "ym28-gate-v1" and gate.get("loop") == loop, "gate schema/loop")
        require((gate.get("sequence"), gate.get("goal"), gate.get("goal_loop")) ==
                (contract["sequence"], contract["goal"], contract["goal_loop"]), "gate order/goal")
        require(gate.get("verdict") in {"accepted_with_limits", "accepted_within_scope", "limited", "conditional"}, "unsupported target verdict")
        nonempty_text(gate.get("model"), "gate model")
        nonempty_text(gate.get("accepted"), "gate claim")
        effective = self.scope(gate, review, pin)
        self.hashes(gate.get("bindings"))
        self.hashes(review.get("bindings"))
        require(admission_name in gate["bindings"] and admission_name in review["bindings"], "admission specification not reviewed/bound")
        required = {PREFIX + f"contracts/{loop}.json", PREFIX + f"skeptic/{loop}.json", PREFIX + f"skeptic/{loop}.md", admission_name}
        for side in ["forward", "reverse"]:
            required.update(PREFIX + f"{side}/{loop}/" + suffix for suffix in ["check.py", "report.md", "freeze.json", "output/results.json"])
        require(required <= gate["bindings"].keys(), "gate missing required evidence")
        require((required - {PREFIX + f"skeptic/{loop}.json"}) <= review["bindings"].keys(), "review missing required current evidence")
        # The contract is itself directly review-bound above, and contract()
        # has checked every declared source hash. A checker input may therefore
        # be reviewed through that explicit one-hop chain (AI4's admitted AI3
        # output). Do not traverse arbitrary historical JSON or accept inputs
        # merely because they appear in the gate/specification.
        reviewed_inputs = {**contract["sources"], **review["bindings"]}
        for checker in spec.get("skeptic_checkers", []):
            require({checker.get("script"), checker.get("output")} <= review["bindings"].keys(), "skeptic script/output not directly reviewed")
            inputs = set(checker.get("inputs", []))
            unreviewed_inputs = inputs - reviewed_inputs.keys()
            snapshot_inputs = {}
            # AH2 post-review executes owned copies of directly reviewed data.
            # Admit only one explicit copy edge, never an arbitrary traversal
            # of historical JSON. The immutable spec pins the inventory and
            # copied bytes, while the review pins both inventory and original.
            for manifest_name in inputs & review["bindings"].keys():
                if not unreviewed_inputs:
                    break
                if re.fullmatch(re.escape(PREFIX + "skeptic/" + loop) +
                                r"(?:-[a-z0-9]+)*-inputs/source-inventory\.json", manifest_name) is None:
                    continue
                expected = review["bindings"][manifest_name]
                require(spec["bindings"].get(manifest_name) == gate["bindings"].get(manifest_name) == expected,
                        "reviewed checker snapshot inventory absent from specification/gate")
                manifest = self.load(manifest_name)
                require(manifest.get("loop") == loop and isinstance(manifest.get("entries"), list),
                        "checker snapshot inventory loop/schema")
                owned = manifest_name.rsplit("/", 1)[0] + "/"
                for entry in manifest["entries"]:
                    require(isinstance(entry, dict), "invalid checker snapshot entry")
                    snapshot = entry.get("snapshot")
                    if not isinstance(snapshot, str) or snapshot not in unreviewed_inputs:
                        continue
                    original, expected = entry.get("source"), entry.get("sha256")
                    require(snapshot.startswith(owned), "checker snapshot outside owned inventory")
                    require(original in reviewed_inputs and reviewed_inputs[original] == expected,
                            "checker snapshot original not reviewed")
                    require(spec["bindings"].get(snapshot) == gate["bindings"].get(snapshot) == expected,
                            "checker snapshot absent from specification/gate")
                    if original not in review["bindings"]:
                        require(gate["bindings"].get(original) == contract["sources"][original],
                                "snapshot contract source absent from gate closure")
                    self.hashes({original: expected, snapshot: expected})
                    require(snapshot not in snapshot_inputs, "duplicate checker snapshot input")
                    snapshot_inputs[snapshot] = expected
            require(inputs <= reviewed_inputs.keys() | snapshot_inputs.keys(),
                    "skeptic input not reviewed directly, through contract, or by an owned snapshot")
            for dependency in inputs - review["bindings"].keys() - snapshot_inputs.keys():
                require(gate["bindings"].get(dependency) == contract["sources"][dependency],
                        "contract-reviewed checker input absent from gate closure")
        require(isinstance(spec.get("skeptic_checkers"), list) and bool(spec["skeptic_checkers"]), "independent skeptic checker missing")
        for producer in spec["producers"].values():
            structure = producer.get("structural_validator")
            if structure is not None:
                name, expected = structure.get("path"), structure.get("sha256")
                require(spec["bindings"].get(name) == gate["bindings"].get(name) == review["bindings"].get(name) == expected,
                        "structural validator not specification/gate/review bound")
        for side, producer in spec["producers"].items():
            for filename, declaration in producer.get("output_artifacts", {}).items():
                if declaration.get("binding") == "freeze":
                    name = PREFIX + f"{side}/{loop}/output/" + filename
                    require(spec["bindings"].get(name) == gate["bindings"].get(name) == review["bindings"].get(name) == declaration.get("sha256"),
                            "freeze-only auxiliary output not specification/gate/direct-review bound")
        producer_records = [self.producer(loop, side, contract, spec["producers"][side], gate["bindings"])
                            for side in ["forward", "reverse"]]
        supplemental = []
        for evidence in spec.get("supplemental_evidence", []):
            name = evidence.get("path")
            require(name in gate["bindings"] and name in review["bindings"], "supplemental evidence not gate/review bound")
            record = self.load(name)
            binding_field = evidence.get("binding_field", "bindings")
            require(binding_field in {"bindings", "sources"}, "unknown supplemental binding convention")
            if binding_field in record:
                self.hashes(record[binding_field])
            supplemental.append({"path": name, "semantic_controls": semantics(record, evidence)})
        return {"loop": loop, "counted_completed": loop in completed, "effective_limitations": effective,
                "producer_evidence": producer_records, "skeptic_checkers": spec["skeptic_checkers"],
                "supplemental_evidence": supplemental,
                "gate_sha256": digest(self.source(PREFIX + f"advisor/{loop}-gate.json"))}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--preflight", metavar="LOOP")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--loops", nargs="+")
    parser.add_argument("--optimized", action="store_true")
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()
    validator = Validator()
    if args.preflight:
        print(json.dumps(validator.preflight(args.preflight), indent=2))
        return
    selected, completed, _ = validator.sequence()
    loops = args.loops or completed
    text_list(loops, "requested loops", empty=args.validate_only)
    require(set(loops) <= set(completed), "replay requested before completed admission")
    if args.validate_only:
        admitted = [validator.validate(loop) for loop in loops]
        print(json.dumps({"status": "validated", "selected_loops": selected, "completed_loops": completed,
                          "loops_validated": [record["loop"] for record in admitted], "new_research_loops": 0}))
        return
    require(args.output is not None and args.output.is_absolute(), "absolute output directory required")
    out = args.output.resolve()
    require(not out.exists() and not out.is_relative_to(ROOT), "fresh external output required")
    out.mkdir(parents=True)
    receipt = {"status": "running", "optimized": args.optimized, "loops_replayed": loops,
               "new_research_loops": 0, "checks": [], "admissions": []}
    try:
        for loop in loops:
            admission = validator.validate(loop)
            receipt["admissions"].append(admission)
            for side in ["forward", "reverse"]:
                destination = out / f"{loop}-{side}"
                command = [sys.executable, "-B"] + (["-O"] if args.optimized else []) + [
                    str(validator.source(PREFIX + f"{side}/{loop}/check.py")), "--output", str(destination)]
                run = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
                logfile = out / f"{loop}-{side}.log"
                logfile.write_text(run.stdout + run.stderr)
                receipt["checks"].append({"command": command, "exit_code": run.returncode, "log_sha256": digest(logfile)})
                require(run.returncode == 0, "producer failed: " + str(logfile))
                fresh = destination / "results.json"
                stored = validator.source(PREFIX + f"{side}/{loop}/output/results.json")
                evidence = next(item for item in admission["producer_evidence"] if item["side"] == side)
                artifacts = evidence["output_artifacts"]
                replay_artifacts(destination, stored.parent, artifacts)
                require(fresh.is_file() and fresh.read_bytes() == stored.read_bytes(), "producer replay bytes differ: " + loop + "/" + side)
                receipt["checks"][-1]["results_sha256"] = digest(fresh)
                if artifacts:
                    receipt["checks"][-1]["output_artifacts"] = artifacts
        receipt["status"] = "passed"
    except Exception as error:
        receipt["status"] = "failed"
        receipt["failure"] = str(error)
        raise
    finally:
        path = out / "receipt.json"
        path.write_text(json.dumps(receipt, indent=2) + "\n")
        (out / "receipt.sha256").write_text(digest(path) + "  receipt.json\n")
        print(json.dumps({"status": receipt["status"], "producer_executions": len(receipt["checks"]), "receipt_sha256": digest(path)}))


if __name__ == "__main__":
    main()
