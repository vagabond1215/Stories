from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Dict, List

from parse_markdown_tables import first_table

ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / "reference"
EXPORT_DIR = REFERENCE / "exports"
ID_PATTERN = re.compile(r"[A-Z]{3}-\d{3}")


def extract_ids(raw: str, prefix: str | None = None) -> List[str]:
    tokens = []
    for match in ID_PATTERN.finditer(raw or ""):
        token = match.group(0)
        if prefix is None or token.startswith(prefix):
            tokens.append(token)
    return tokens


def parse_number(value: str) -> float:
    try:
        return float(value)
    except ValueError:
        return 0.0


def parse_stats(cell: str) -> Dict[str, object]:
    stats = {"is_delta": False, "bo": 0, "l": 0, "em": 1.0, "r": 0.0, "qt": 0, "cap": 0, "up": 0, "tags": []}
    if not cell or not cell.strip():
        return stats
    parts = [part.strip() for part in cell.split(";") if part.strip()]
    for part in parts:
        if "=" not in part:
            continue
        key, raw_val = [p.strip() for p in part.split("=", 1)]
        if key == "tags":
            tags = [tag.strip() for tag in raw_val.split(",") if tag.strip()]
            stats["tags"] = tags
            continue
        is_delta = raw_val.startswith("+")
        if is_delta:
            raw_val = raw_val[1:]
            stats["is_delta"] = True
        if key in {"bo", "l", "qt", "cap", "up"}:
            stats[key] = int(raw_val) if raw_val else 0
        elif key in {"em", "r"}:
            stats[key] = float(raw_val) if raw_val else 0.0
    return stats


def parse_structures() -> List[Dict[str, object]]:
    headers, rows = first_table(REFERENCE / "structures.md")
    structures: List[Dict[str, object]] = []
    for row in rows:
        struct = {
            "id": row.get("ID", ""),
            "name": row.get("Name", ""),
            "type": row.get("Type", ""),
            "purpose": row.get("Purpose", ""),
            "requirements": row.get("Requirements (IDs)", ""),
            "enabled_actions": extract_ids(row.get("Enabled actions (IDs)", "")),
            "required_tech": extract_ids(row.get("Required tech (TEC)", ""), prefix="TEC"),
            "notes": row.get("Notes", ""),
            "stats": parse_stats(row.get("Stats", "")),
            "upgrade_path": extract_ids(row.get("Upgrade path", ""), prefix="STR"),
        }
        structures.append(struct)
    structures.sort(key=lambda s: int(s["id"].split("-", 1)[1]))
    return structures


def tier_to_int(tier: str) -> int:
    match = re.search(r"(\d+)", tier or "")
    return int(match.group(1)) if match else 0


def parse_technology() -> Dict[str, object]:
    headers, rows = first_table(REFERENCE / "technology.md")
    nodes = []
    edges = []
    unlock_map: Dict[str, List[Dict[str, str]]] = {}
    for row in rows:
        tech_id = row.get("ID", "")
        prereqs = extract_ids(row.get("Prerequisites (IDs)", ""), prefix="TEC")
        unlocks = extract_ids(row.get("Unlocks (IDs)", ""))
        nodes.append(
            {
                "id": tech_id,
                "name": row.get("Name", ""),
                "tier": tier_to_int(row.get("Tier", "")),
                "prerequisites": prereqs,
                "unlocks": unlocks,
                "time_cost": row.get("Time/Cost", ""),
                "notes": row.get("Notes", ""),
            }
        )
        for prereq in prereqs:
            edges.append({"from": prereq, "to": tech_id, "type": "prereq"})
        if unlocks:
            unlock_map[tech_id] = [{"id": target, "type": target.split("-", 1)[0].lower()} for target in unlocks]
    nodes.sort(key=lambda n: int(n["id"].split("-", 1)[1]))
    edges.sort(key=lambda e: (e["from"], e["to"], e["type"]))
    unlocks_sorted = []
    for tech_id in sorted(unlock_map):
        unlocks_sorted.append({"tech_id": tech_id, "unlocks": sorted(unlock_map[tech_id], key=lambda u: (u["type"], u["id"]))})
    return {"nodes": nodes, "edges": edges, "unlocks": unlocks_sorted}


def parse_list(value: str, sep: str = ",") -> List[str]:
    return [token.strip() for token in (value or "").split(sep) if token.strip()]


def parse_districts() -> List[Dict[str, object]]:
    _, rows = first_table(REFERENCE / "systems_districts.md")
    districts: List[Dict[str, object]] = []
    for row in rows:
        districts.append(
            {
                "key": row.get("Key", ""),
                "name": row.get("Name", ""),
                "qualifying_tags": parse_list(row.get("Qualifying tags", "")),
                "min_buildings": int(row.get("Min buildings", "0") or 0),
                "radius": int(row.get("Radius", "0") or 0),
                "bonuses": parse_list(row.get("Bonuses", ""), sep=";"),
                "penalties": parse_list(row.get("Penalties", ""), sep=";"),
                "notable_adjacency_pairs": parse_list(row.get("Notable adjacency pairs", ""), sep=";"),
            }
        )
    districts.sort(key=lambda d: d["key"])
    return districts


def parse_events() -> List[Dict[str, object]]:
    _, rows = first_table(REFERENCE / "systems_events.md")
    events: List[Dict[str, object]] = []
    for row in rows:
        events.append(
            {
                "key": row.get("Key", ""),
                "name": row.get("Name", ""),
                "category": row.get("Category", ""),
                "base_chance": parse_number(row.get("Base chance", "0")),
                "triggers": parse_list(row.get("Triggers", ""), sep=";"),
                "effects": parse_list(row.get("Effects", ""), sep=";"),
                "mitigation": parse_list(row.get("Mitigation", ""), sep=";"),
            }
        )
    events.sort(key=lambda e: e["key"])
    return events


def parse_difficulty() -> List[Dict[str, object]]:
    _, rows = first_table(REFERENCE / "systems_difficulty.md")
    difficulties: List[Dict[str, object]] = []
    for row in rows:
        difficulties.append(
            {
                "key": row.get("Key", ""),
                "name": row.get("Name", ""),
                "research_time_mult": parse_number(row.get("Research time mult", "1")),
                "event_freq_mult": parse_number(row.get("Event freq mult", "1")),
                "event_severity_mult": parse_number(row.get("Event severity mult", "1")),
                "upkeep_mult": parse_number(row.get("Upkeep mult", "1")),
                "labor_tightness": row.get("Labor tightness", ""),
                "recovery_cost_mult": parse_number(row.get("Recovery cost mult", "1")),
                "notes": row.get("Notes", ""),
            }
        )
    difficulties.sort(key=lambda d: d["key"])
    return difficulties


def build_exports(write_files: bool = True) -> Dict[str, object]:
    structures = parse_structures()
    tech_graph = parse_technology()
    districts = parse_districts()
    events = parse_events()
    difficulty = parse_difficulty()

    payloads = {
        "structures": structures,
        "tech_graph": tech_graph,
        "systems_districts": districts,
        "systems_events": events,
        "systems_difficulty": difficulty,
    }

    if write_files:
        EXPORT_DIR.mkdir(parents=True, exist_ok=True)
        (EXPORT_DIR / "structures.json").write_text(json.dumps(structures, indent=2) + "\n")
        (EXPORT_DIR / "tech_graph.json").write_text(json.dumps(tech_graph, indent=2) + "\n")
        (EXPORT_DIR / "systems_districts.json").write_text(json.dumps(districts, indent=2) + "\n")
        (EXPORT_DIR / "systems_events.json").write_text(json.dumps(events, indent=2) + "\n")
        (EXPORT_DIR / "systems_difficulty.json").write_text(json.dumps(difficulty, indent=2) + "\n")
    return payloads


if __name__ == "__main__":
    build_exports()
    print("Exports written to", EXPORT_DIR)
