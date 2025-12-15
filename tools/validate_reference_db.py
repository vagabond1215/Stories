from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

ID_PATTERN = re.compile(r"[A-Z]{3}-\d{3}")
ROOT = Path(__file__).resolve().parents[1]
REFERENCE_DIR = ROOT / "reference"

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


def parse_markdown_tables(path: Path) -> List[Tuple[List[str], List[List[str]]]]:
    lines = path.read_text().splitlines()
    tables: List[Tuple[List[str], List[List[str]]]] = []
    idx = 0
    while idx < len(lines):
        line = lines[idx]
        if line.lstrip().startswith("|") and idx + 1 < len(lines) and lines[idx + 1].lstrip().startswith("| ---"):
            headers = [cell.strip() for cell in line.strip().strip("|").split("|")]
            idx += 2
            rows: List[List[str]] = []
            while idx < len(lines) and lines[idx].lstrip().startswith("|"):
                cells = [cell.strip() for cell in lines[idx].strip().strip("|").split("|")]
                if len(cells) == len(headers):
                    rows.append(cells)
                idx += 1
            tables.append((headers, rows))
        else:
            idx += 1
    return tables


def extract_ids(value: str) -> List[str]:
    if not value or value.lower() == "none":
        return []
    return ID_PATTERN.findall(value)


def collect_domain_ids() -> Dict[str, Dict[str, str]]:
    domain_map: Dict[str, Dict[str, str]] = {}
    seen: Dict[str, str] = {}
    for name, path in TABLE_FILES.items():
        if not path.exists():
            continue
        for headers, rows in parse_markdown_tables(path):
            if not headers or headers[0] != "ID":
                continue
            for cells in rows:
                if len(cells) != len(headers):
                    continue
                row = dict(zip(headers, cells))
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


def validate_reference(domain_map: Dict[str, Dict[str, str]]):
    errors: List[str] = []

    def validate_tokens(tokens: List[str], prefix_hint: str, file_label: str, row_id: str, column: str):
        for token in tokens:
            prefix = token.split("-", 1)[0]
            if prefix_hint and prefix != prefix_hint:
                errors.append(f"{file_label} row {row_id} column '{column}': expected prefix {prefix_hint} got {token}")
                continue
            if prefix not in domain_map or token not in domain_map[prefix]:
                errors.append(f"{file_label} row {row_id} column '{column}': unknown ID {token}")

    tech_rows = parse_markdown_tables(TABLE_FILES["technology"])[0][1]
    tech_headers = parse_markdown_tables(TABLE_FILES["technology"])[0][0]
    tech_index = {h: i for i, h in enumerate(tech_headers)}

    adjacency: Dict[str, List[str]] = {}
    for cells in tech_rows:
        row = dict(zip(tech_headers, cells))
        tech_id = row["ID"]
        prereqs = extract_ids(row.get("Prerequisites (IDs)", ""))
        unlocks = extract_ids(row.get("Unlocks (IDs)", ""))
        validate_tokens(prereqs, "TEC", TABLE_FILES["technology"].name, tech_id, "Prerequisites (IDs)")
        validate_tokens(unlocks, "", TABLE_FILES["technology"].name, tech_id, "Unlocks (IDs)")
        for prereq in prereqs:
            adjacency.setdefault(prereq, []).append(tech_id)

    detect_cycles(adjacency, errors)

    crafting_headers, crafting_rows = parse_markdown_tables(TABLE_FILES["crafting_recipes"])[0]
    idx_unlock = crafting_headers.index("Unlocked by (TEC)")
    for cells in crafting_rows:
        row_id = cells[0]
        tokens = extract_ids(cells[idx_unlock])
        validate_tokens(tokens, "TEC", TABLE_FILES["crafting_recipes"].name, row_id, "Unlocked by (TEC)")

    job_headers, job_rows = parse_markdown_tables(TABLE_FILES["jobs"])[0]
    idx_job = job_headers.index("Required tech (TEC)")
    for cells in job_rows:
        row_id = cells[0]
        tokens = extract_ids(cells[idx_job])
        validate_tokens(tokens, "TEC", TABLE_FILES["jobs"].name, row_id, "Required tech (TEC)")

    structure_headers, structure_rows = parse_markdown_tables(TABLE_FILES["structures"])[0]
    idx_struct = structure_headers.index("Required tech (TEC)")
    for cells in structure_rows:
        row_id = cells[0]
        tokens = extract_ids(cells[idx_struct])
        validate_tokens(tokens, "TEC", TABLE_FILES["structures"].name, row_id, "Required tech (TEC)")

    spell_headers, spell_rows = parse_markdown_tables(TABLE_FILES["spells"])[0]
    idx_spell = spell_headers.index("Unlocked by (TEC)")
    for cells in spell_rows:
        row_id = cells[0]
        tokens = extract_ids(cells[idx_spell])
        validate_tokens(tokens, "TEC", TABLE_FILES["spells"].name, row_id, "Unlocked by (TEC)")

    equip_headers, equip_rows = parse_markdown_tables(TABLE_FILES["equipment"])[0]
    idx_eqp = equip_headers.index("Unlocked by (TEC)")
    for cells in equip_rows:
        row_id = cells[0]
        tokens = extract_ids(cells[idx_eqp])
        validate_tokens(tokens, "TEC", TABLE_FILES["equipment"].name, row_id, "Unlocked by (TEC)")

    mat_headers, mat_rows = parse_markdown_tables(TABLE_FILES["materials"])[0]
    idx_mat = mat_headers.index("Unlocked by (TEC)")
    for cells in mat_rows:
        row_id = cells[0]
        tokens = extract_ids(cells[idx_mat])
        validate_tokens(tokens, "TEC", TABLE_FILES["materials"].name, row_id, "Unlocked by (TEC)")

    if errors:
        raise ValidationError("\n".join(errors))


def detect_cycles(graph: Dict[str, List[str]], errors: List[str]):
    visited: Dict[str, str] = {}

    def dfs(node: str, stack: List[str]):
        visited[node] = "visiting"
        for neighbor in graph.get(node, []):
            state = visited.get(neighbor)
            if state == "visiting":
                cycle_path = " -> ".join(stack + [neighbor])
                errors.append(f"Technology prerequisite cycle detected: {cycle_path}")
            elif state != "visited":
                dfs(neighbor, stack + [neighbor])
        visited[node] = "visited"

    for node in graph:
        if visited.get(node) is None:
            dfs(node, [node])


def main():
    try:
        domain_map = collect_domain_ids()
        validate_reference(domain_map)
    except ValidationError as exc:
        print(exc)
        sys.exit(1)


if __name__ == "__main__":
    main()
