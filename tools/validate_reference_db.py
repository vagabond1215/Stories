import json
import sys
from pathlib import Path
from typing import Dict, List, Set

from jsonschema import Draft202012Validator

import build_exports
from parse_markdown_tables import parse_markdown_tables

ROOT = Path(__file__).resolve().parent.parent
REFERENCE = ROOT / "reference"
SCHEMAS = REFERENCE / "schemas"


def _load_schema(name: str) -> Dict:
    return json.loads((SCHEMAS / name).read_text())


def _collect_ids(rows: List[Dict[str, str]], key: str) -> Set[str]:
    return {row.get(key, '') for row in rows if row.get(key, '')}


def _tokenize(cell: str) -> List[str]:
    tokens: List[str] = []
    for part in cell.replace(';', ',').split(','):
        token = part.strip()
        if token:
            tokens.append(token)
    return tokens


def _check_references(struct_rows: List[Dict[str, str]], tech_rows: List[Dict[str, str]]) -> List[str]:
    errors: List[str] = []
    struct_ids = _collect_ids(struct_rows, 'ID')
    tech_ids = _collect_ids(tech_rows, 'ID')

    for row in struct_rows:
        sid = row.get('ID', '')
        for req in _tokenize(row.get('Requirements (IDs)', '')):
            if req.startswith('STR-') and req not in struct_ids:
                errors.append(f"structures.md {sid}: missing structure requirement {req}")
            if req.startswith('TEC-') and req not in tech_ids:
                errors.append(f"structures.md {sid}: missing tech requirement {req}")
        for req in _tokenize(row.get('Required tech (TEC)', '')):
            if req.startswith('TEC-') and req not in tech_ids:
                errors.append(f"structures.md {sid}: missing tech requirement {req}")
        for upgrade in _tokenize(row.get('Upgrade path', '')):
            if upgrade.startswith('STR-') and upgrade not in struct_ids:
                errors.append(f"structures.md {sid}: missing upgrade path target {upgrade}")

    for row in tech_rows:
        tid = row.get('ID', '')
        for pre in _tokenize(row.get('Prerequisites (IDs)', '')):
            if pre.startswith('TEC-') and pre not in tech_ids:
                errors.append(f"technology.md {tid}: missing prerequisite {pre}")
        for unlock in _tokenize(row.get('Unlocks (IDs)', '')):
            if unlock.startswith('TEC-') and unlock not in tech_ids:
                errors.append(f"technology.md {tid}: missing unlock {unlock}")
            if unlock.startswith('STR-') and unlock not in struct_ids:
                errors.append(f"technology.md {tid}: missing unlock {unlock}")
    return errors


def _detect_cycles(rows: List[Dict[str, str]]) -> List[str]:
    graph: Dict[str, List[str]] = {}
    for row in rows:
        tid = row.get('ID', '')
        graph[tid] = [t for t in _tokenize(row.get('Prerequisites (IDs)', '')) if t.startswith('TEC-')]

    visited: Dict[str, int] = {}  # 0=unvisited,1=visiting,2=done
    cycle_errors: List[str] = []

    def dfs(node: str, stack: List[str]):
        state = visited.get(node, 0)
        if state == 1:
            cycle_errors.append(f"technology.md cycle detected: {' -> '.join(stack + [node])}")
            return
        if state == 2:
            return
        visited[node] = 1
        for neighbor in graph.get(node, []):
            dfs(neighbor, stack + [node])
        visited[node] = 2

    for tid in graph:
        if visited.get(tid, 0) == 0:
            dfs(tid, [])
    return cycle_errors


def _validate_schema(data: object, schema_name: str) -> List[str]:
    schema = _load_schema(schema_name)
    validator = Draft202012Validator(schema)
    return [f"schema:{schema_name} path={'/'.join(str(x) for x in error.path)} error={error.message}" for error in validator.iter_errors(data)]


def main() -> int:
    struct_table = parse_markdown_tables(REFERENCE / "structures.md")[0][1]
    tech_table = parse_markdown_tables(REFERENCE / "technology.md")[0][1]

    errors = _check_references(struct_table, tech_table)
    errors += _detect_cycles(tech_table)

    exports = build_exports.build_all()
    schema_errors: List[str] = []
    schema_errors += _validate_schema(exports['structures'], 'structures.schema.json')
    schema_errors += _validate_schema(exports['technology'], 'technology.schema.json')
    schema_errors += _validate_schema(exports['calendar'], 'systems_calendar.schema.json')
    schema_errors += _validate_schema(exports['districts'], 'systems_districts.schema.json')
    schema_errors += _validate_schema(exports['events'], 'systems_events.schema.json')
    schema_errors += _validate_schema(exports['difficulty'], 'systems_difficulty.schema.json')

    errors += schema_errors

    if errors:
        for err in errors:
            print(err)
        return 1
    print("Validation passed: references, cycles, and schemas clean.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
