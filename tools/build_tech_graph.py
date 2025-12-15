from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Dict, List

ID_PATTERN = re.compile(r"[A-Z]{3}-\d{3}")
ROOT = Path(__file__).resolve().parents[1]
TECH_PATH = ROOT / "reference" / "technology.md"
OUTPUT_PATH = ROOT / "reference" / "tech_tree" / "tech_tree.json"


def parse_markdown_table(path: Path) -> List[Dict[str, str]]:
    lines = path.read_text().splitlines()
    rows: List[Dict[str, str]] = []
    headers: List[str] = []
    for idx, line in enumerate(lines):
        if line.lstrip().startswith("|") and idx + 1 < len(lines) and lines[idx + 1].lstrip().startswith("| ---"):
            headers = [cell.strip() for cell in line.strip().strip("|").split("|")]
            continue
        if headers and line.lstrip().startswith("|"):
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            if len(cells) != len(headers):
                continue
            rows.append(dict(zip(headers, cells)))
        elif headers and line.strip() == "":
            break
    return rows


def extract_ids(raw: str) -> List[str]:
    if not raw or raw.lower() == "none":
        return []
    return ID_PATTERN.findall(raw)


def tier_to_int(tier: str) -> int | None:
    match = re.search(r"(\d+)", tier)
    return int(match.group(1)) if match else None


def unlock_type(token: str) -> str:
    prefix = token.split("-", 1)[0]
    return {
        "STR": "structure",
        "CRF": "recipe",
        "EQP": "equipment",
        "SPL": "spell",
        "MAT": "material",
        "JOB": "job",
        "TEC": "technology",
        "PPF": "profile",
        "STP": "settlement",
        "INV": "inventory",
        "BIO": "biome",
        "FAU": "fauna",
        "FLR": "flora",
    }.get(prefix, "unknown")


def build_graph():
    tech_rows = parse_markdown_table(TECH_PATH)
    nodes = []
    edges = []
    unlocks: Dict[str, List[Dict[str, str]]] = {}

    for row in tech_rows:
        tech_id = row.get("ID")
        tier_value = tier_to_int(row.get("Tier", ""))
        nodes.append({"id": tech_id, "name": row.get("Name"), "tier": tier_value})

        for prereq in extract_ids(row.get("Prerequisites (IDs)", "")):
            edges.append({"from": prereq, "to": tech_id, "type": "prereq"})

        for target in extract_ids(row.get("Unlocks (IDs)", "")):
            unlocks.setdefault(tech_id, []).append({"type": unlock_type(target), "id": target})

    nodes.sort(key=lambda n: n["id"])
    edges.sort(key=lambda e: (e["from"], e["to"], e["type"]))

    unlock_list = []
    for tech_id in sorted(unlocks):
        unlock_entries = sorted(unlocks[tech_id], key=lambda u: (u["type"], u["id"]))
        unlock_list.append({"tech_id": tech_id, "unlocks": unlock_entries})

    graph = {"nodes": nodes, "edges": edges, "unlocks": unlock_list}
    OUTPUT_PATH.write_text(json.dumps(graph, indent=2, sort_keys=False) + "\n")
    print(f"Wrote {OUTPUT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    build_graph()
