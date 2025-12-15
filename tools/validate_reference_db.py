from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Dict, List

from jsonschema import Draft7Validator

from build_exports import build_exports
from parse_markdown_tables import parse_markdown_tables

ID_PATTERN = re.compile(r"[A-Z]{3}-\d{3}")
ROOT = Path(__file__).resolve().parents[1]
REFERENCE_DIR = ROOT / "reference"
SCHEMA_DIR = REFERENCE_DIR / "schemas"
EXPORT_DIR = REFERENCE_DIR / "exports"

TABLE_FILES = {
    "technology": REFERENCE_DIR / "technology.md",
    "crafting_recipes": REFERENCE_DIR / "crafting_recipes.md",
    "jobs": REFERENCE_DIR / "jobs.md",
    "structures": REFERENCE_DIR / "structures.md",
    "equipment": REFERENCE_DIR / "equipment.md",
    "spells": REFERENCE_DIR / "spells.md",
    "materials": REFERENCE_DIR / "materials.md",
    "profiles": REFERENCE_DIR / "profiles.md",
    "inventories": REFERENCE_DIR / "inventories.md",
    "flora": REFERENCE_DIR / "flora.md",
    "fauna": REFERENCE_DIR / "fauna.md",
    "biomes": REFERENCE_DIR / "biomes.md",
    "templates": REFERENCE_DIR / "templates.md",
}


class ValidationError(Exception):
    pass


def collect_domain_ids() -> Dict[str, Dict[str, str]]:
    domain_map: Dict[str, Dict[str, str]] = {}
    seen: Dict[str, str] = {}
    for name, path in TABLE_FILES.items():
        if not path.exists():
            continue
        for table in parse_markdown_tables(path):
            headers = table.get("headers", [])
            if not headers or headers[0] != "ID":
                continue
            for row in table.get("rows", []):
                row_id = row.get("ID")
                if not row_id:
                    continue
                if not ID_PATTERN.fullmatch(row_id):
                    raise ValidationError(f"{path}: row ID '{row_id}' has invalid format")
                prefix = row_id.split("-", 1)[0]
                domain_map.setdefault(prefix, {})[row_id] = path.name
                if row_id in seen:
                    raise ValidationError(f"Duplicate ID {row_id} found in {path.name} and {seen[row_id]}")
                seen[row_id] = path.name
    return domain_map


def extract_ids(value: str) -> List[str]:
    if not value or value.lower() == "none":
        return []
    return ID_PATTERN.findall(value)


def detect_cycles(graph: Dict[str, List[str]], errors: List[str]):
    visited: Dict[str, str] = {}

    def dfs(node: str, stack: List[str]):
        visited[node] = "visiting"
        for neighbor in graph.get(node, []):
            state = visited.get(neighbor)
            if state == "visiting":
                errors.append(f"Technology prerequisite cycle detected: {' -> '.join(stack + [neighbor])}")
            elif state != "visited":
                dfs(neighbor, stack + [neighbor])
        visited[node] = "visited"

    for node in graph:
        if visited.get(node) is None:
            dfs(node, [node])


def validate_tokens(tokens: List[str], prefix_hint: str, file_label: str, row_id: str, column: str, domain_map: Dict[str, Dict[str, str]], errors: List[str]):
    for token in tokens:
        prefix = token.split("-", 1)[0]
        if prefix_hint and prefix != prefix_hint:
            errors.append(f"{file_label} row {row_id} column '{column}': expected prefix {prefix_hint} got {token}")
            continue
        if prefix not in domain_map or token not in domain_map[prefix]:
            errors.append(f"{file_label} row {row_id} column '{column}': unknown ID {token}")


def validate_schema(export_path: Path, schema_path: Path, errors: List[str]):
    if not export_path.exists():
        errors.append(f"Missing export file {export_path}")
        return
    data = json.loads(export_path.read_text())
    schema = json.loads(schema_path.read_text())
    validator = Draft7Validator(schema)
    for err in sorted(validator.iter_errors(data), key=lambda e: e.path):
        errors.append(f"Schema error in {export_path.name}: {err.message}")


def validate_exports(domain_map: Dict[str, Dict[str, str]]):
    errors: List[str] = []
    exports = build_exports(write_files=True)

    tech_nodes = exports["tech_graph"]["nodes"]
    adjacency: Dict[str, List[str]] = {}
    for node in tech_nodes:
        tech_id = node["id"]
        prereqs = node.get("prerequisites", [])
        unlocks = node.get("unlocks", [])
        validate_tokens(prereqs, "TEC", "technology.md", tech_id, "Prerequisites (IDs)", domain_map, errors)
        validate_tokens(unlocks, "", "technology.md", tech_id, "Unlocks (IDs)", domain_map, errors)
        for prereq in prereqs:
            adjacency.setdefault(prereq, []).append(tech_id)
    detect_cycles(adjacency, errors)

    structures = exports["structures"]
    structure_ids = {s["id"] for s in structures}
    for struct in structures:
        validate_tokens(struct.get("required_tech", []), "TEC", "structures.md", struct["id"], "Required tech (TEC)", domain_map, errors)
        for target in struct.get("upgrade_path", []):
            if target not in structure_ids:
                errors.append(f"structures.md row {struct['id']} column 'Upgrade path': unknown structure {target}")

    # cross checks for other tables
    if (TABLE_FILES["crafting_recipes"].exists()):
        for table in parse_markdown_tables(TABLE_FILES["crafting_recipes"]):
            headers = table.get("headers", [])
            if "Unlocked by (TEC)" in headers:
                idx = headers.index("Unlocked by (TEC)")
                for row in table.get("rows", []):
                    row_id = row.get("ID", "")
                    tokens = extract_ids(row.get(headers[idx], ""))
                    validate_tokens(tokens, "TEC", TABLE_FILES["crafting_recipes"].name, row_id, "Unlocked by (TEC)", domain_map, errors)

    if TABLE_FILES["jobs"].exists():
        for table in parse_markdown_tables(TABLE_FILES["jobs"]):
            headers = table.get("headers", [])
            if "Required tech (TEC)" in headers:
                idx = headers.index("Required tech (TEC)")
                for row in table.get("rows", []):
                    row_id = row.get("ID", "")
                    tokens = extract_ids(row.get(headers[idx], ""))
                    validate_tokens(tokens, "TEC", TABLE_FILES["jobs"].name, row_id, "Required tech (TEC)", domain_map, errors)

    # ensure system keys unique
    for key_group in ("systems_districts", "systems_events", "systems_difficulty"):
        keys = [entry["key"] for entry in exports.get(key_group, [])]
        dupes = {k for k in keys if keys.count(k) > 1}
        for dup in dupes:
            errors.append(f"Duplicate key {dup} found in {key_group}")

    # schema validation
    schema_map = {
        "structures.json": SCHEMA_DIR / "structures.schema.json",
        "tech_graph.json": SCHEMA_DIR / "technology.schema.json",
        "systems_districts.json": SCHEMA_DIR / "systems_districts.schema.json",
        "systems_events.json": SCHEMA_DIR / "systems_events.schema.json",
        "systems_difficulty.json": SCHEMA_DIR / "systems_difficulty.schema.json",
    }
    for export_name, schema_path in schema_map.items():
        validate_schema(EXPORT_DIR / export_name, schema_path, errors)

    if errors:
        raise ValidationError("\n".join(errors))


def main():
    try:
        domain_map = collect_domain_ids()
        validate_exports(domain_map)
    except ValidationError as exc:
        print(exc)
        sys.exit(1)


if __name__ == "__main__":
    main()
