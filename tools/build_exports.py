import json
import re
from pathlib import Path
from typing import Callable, Dict, List

from parse_markdown_tables import parse_markdown_tables

ROOT = Path(__file__).resolve().parent.parent
REFERENCE = ROOT / "reference"
EXPORTS = REFERENCE / "exports"


def _split_tokens(cell: str) -> List[str]:
    tokens: List[str] = []
    for part in re.split(r"[;,]", cell or ""):
        token = part.strip()
        if token:
            tokens.append(token)
    return tokens


def _parse_numeric(value: str):
    try:
        return float(value) if '.' in value else int(value)
    except ValueError:
        return value


def _parse_stats(raw: str, is_module: bool) -> Dict[str, object]:
    stats: Dict[str, object] = {}
    if not raw:
        return stats
    pairs = [p.strip() for p in raw.split(';') if p.strip()]
    delta = False
    for pair in pairs:
        if '=' not in pair:
            continue
        key, value = [p.strip() for p in pair.split('=', 1)]
        if key == 'tags':
            stats['tags'] = [t.strip() for t in value.split(',') if t.strip()]
            continue
        has_prefix = value.startswith('+') or value.startswith('-')
        clean_value = value[1:] if value.startswith('+') else value.lstrip('+')
        parsed = _parse_numeric(clean_value)
        stats[key] = parsed
        if has_prefix:
            delta = True
    if delta or is_module:
        stats['delta'] = True
    return stats


def build_structures_export() -> List[Dict[str, object]]:
    _, rows = parse_markdown_tables(REFERENCE / "structures.md")[0]
    structures: List[Dict[str, object]] = []
    for row in rows:
        stats = _parse_stats(row.get('Stats', ''), 'Upgrade/Module' in row.get('Type', ''))
        structures.append({
            "id": row.get('ID', ''),
            "name": row.get('Name', ''),
            "type": row.get('Type', ''),
            "purpose": row.get('Purpose', ''),
            "requirements": _split_tokens(row.get('Requirements (IDs)', '')),
            "enabled_actions": _split_tokens(row.get('Enabled actions (IDs)', '')),
            "required_tech": _split_tokens(row.get('Required tech (TEC)', '')),
            "notes": row.get('Notes', ''),
            "stats": stats,
            "upgrade_path": _split_tokens(row.get('Upgrade path', '')),
        })
    structures.sort(key=lambda r: int(re.search(r"(\d+)$", r["id"]).group(1)))
    return structures


def build_technology_export() -> Dict[str, object]:
    _, rows = parse_markdown_tables(REFERENCE / "technology.md")[0]
    nodes: List[Dict[str, object]] = []
    prereq_edges: List[Dict[str, str]] = []
    unlock_edges: List[Dict[str, str]] = []
    for row in rows:
        tid = row.get('ID', '')
        prerequisites = _split_tokens(row.get('Prerequisites (IDs)', ''))
        unlocks = _split_tokens(row.get('Unlocks (IDs)', ''))
        nodes.append({
            "id": tid,
            "name": row.get('Name', ''),
            "tier": row.get('Tier', ''),
            "prerequisites": prerequisites,
            "unlocks": unlocks,
            "time_cost": row.get('Time/Cost', ''),
            "notes": row.get('Notes', ''),
        })
        for pre in prerequisites:
            prereq_edges.append({"from": pre, "to": tid})
        for unlock in unlocks:
            unlock_edges.append({"from": tid, "to": unlock})
    nodes.sort(key=lambda n: int(re.search(r"(\d+)$", n["id"]).group(1)))
    prereq_edges.sort(key=lambda e: (e["to"], e["from"]))
    unlock_edges.sort(key=lambda e: (e["from"], e["to"]))
    return {"nodes": nodes, "prerequisite_edges": prereq_edges, "unlock_edges": unlock_edges}


def _build_simple_system(path: Path, transforms: Dict[str, Callable[[str], object]]) -> List[Dict[str, object]]:
    _, rows = parse_markdown_tables(path)[0]
    entries: List[Dict[str, object]] = []
    for row in rows:
        entry: Dict[str, object] = {}
        for key, value in row.items():
            canonical = key.lower().replace(' ', '_')
            transform = transforms.get(canonical)
            entry_field = canonical.replace('(ids)', '').replace('(', '').replace(')', '')
            entry[entry_field] = transform(value) if transform else value
        entries.append(entry)
    entries.sort(key=lambda e: e.get('key', ''))
    return entries


def build_calendar_export() -> List[Dict[str, object]]:
    return _build_simple_system(REFERENCE / "systems_calendar.md", {
        'value': lambda v: float(v) if re.match(r"^-?\d+(\.\d+)?$", v) else v
    })


def build_districts_export() -> List[Dict[str, object]]:
    return _build_simple_system(REFERENCE / "systems_districts.md", {
        'qualifying_tags': lambda v: [t.strip() for t in v.split(',') if t.strip()],
        'min_buildings': lambda v: int(v) if v else 0,
        'radius': lambda v: int(v) if v else 0,
    })


def build_events_export() -> List[Dict[str, object]]:
    return _build_simple_system(REFERENCE / "systems_events.md", {
        'base_chance': lambda v: float(v) if v else 0.0,
    })


def build_difficulty_export() -> List[Dict[str, object]]:
    return _build_simple_system(REFERENCE / "systems_difficulty.md", {
        'research_time_mult': lambda v: float(v) if v else 0.0,
        'event_freq_mult': lambda v: float(v) if v else 0.0,
        'event_severity_mult': lambda v: float(v) if v else 0.0,
        'upkeep_mult': lambda v: float(v) if v else 0.0,
        'recovery_cost_mult': lambda v: float(v) if v else 0.0,
    })


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2))


def build_all() -> Dict[str, object]:
    structures = build_structures_export()
    technology = build_technology_export()
    calendar = build_calendar_export()
    districts = build_districts_export()
    events = build_events_export()
    difficulty = build_difficulty_export()
    return {
        "structures": structures,
        "technology": technology,
        "calendar": calendar,
        "districts": districts,
        "events": events,
        "difficulty": difficulty,
    }


def main() -> None:
    exports = build_all()
    write_json(EXPORTS / "structures.json", exports["structures"])
    write_json(EXPORTS / "tech_graph.json", exports["technology"])
    write_json(EXPORTS / "systems_calendar.json", exports["calendar"])
    write_json(EXPORTS / "systems_districts.json", exports["districts"])
    write_json(EXPORTS / "systems_events.json", exports["events"])
    write_json(EXPORTS / "systems_difficulty.json", exports["difficulty"])


if __name__ == "__main__":
    main()
