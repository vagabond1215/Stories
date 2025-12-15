from __future__ import annotations

from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Tuple


def parse_markdown_tables(path: Path) -> List[Dict[str, List[Dict[str, str]]]]:
    lines = path.read_text().splitlines()
    tables: List[Dict[str, List[Dict[str, str]]]] = []
    idx = 0
    while idx < len(lines):
        line = lines[idx]
        if line.lstrip().startswith("|") and idx + 1 < len(lines) and lines[idx + 1].lstrip().startswith("| ---"):
            headers = [cell.strip() for cell in line.strip().strip("|").split("|")]
            idx += 2
            rows: List[Dict[str, str]] = []
            while idx < len(lines) and lines[idx].lstrip().startswith("|"):
                cells = [cell.strip() for cell in lines[idx].strip().strip("|").split("|")]
                if len(cells) == len(headers):
                    rows.append(dict(zip(headers, cells)))
                idx += 1
            tables.append({"headers": headers, "rows": rows})
        else:
            idx += 1
    return tables


def first_table(path: Path) -> Tuple[List[str], List[Dict[str, str]]]:
    tables = parse_markdown_tables(path)
    if not tables:
        return [], []
    table = tables[0]
    return table["headers"], table["rows"]
