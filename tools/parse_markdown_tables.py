import re
from pathlib import Path
from typing import Dict, List, Tuple


def _coalesce_rows(lines: List[str]) -> List[str]:
    rows: List[str] = []
    current: List[str] = []
    for line in lines:
        stripped = line.rstrip('\n')
        if not stripped:
            if current:
                rows.append(' '.join(current).strip())
                current = []
            continue
        if stripped.lstrip().startswith('|'):
            if current:
                rows.append(' '.join(current).strip())
                current = []
            current.append(stripped.strip())
        elif current:
            current.append(stripped.strip())
    if current:
        rows.append(' '.join(current).strip())
    return rows


def parse_markdown_tables(path: Path) -> List[Tuple[List[str], List[Dict[str, str]]]]:
    """Parse all GitHub-flavored markdown tables in a file.

    Returns a list of (headers, rows) tuples. Rows are dictionaries keyed by header.
    """
    content = Path(path).read_text().splitlines()
    tables: List[Tuple[List[str], List[Dict[str, str]]]] = []
    idx = 0
    while idx < len(content):
        line = content[idx].strip()
        if line.startswith('|') and idx + 1 < len(content):
            separator = content[idx + 1].strip()
            if re.match(r'^\|\s*-+', separator):
                # capture table block until a blank line or non-table start
                block: List[str] = []
                j = idx
                while j < len(content):
                    probe = content[j].rstrip('\n')
                    if probe.strip() == '':
                        break
                    if probe.lstrip().startswith('|') or (block and probe.startswith(' ')):
                        block.append(probe)
                        j += 1
                        continue
                    if block and not probe.strip().startswith('|'):
                        break
                    block.append(probe)
                    j += 1
                rows = _coalesce_rows(block)
                if len(rows) >= 2:
                    header = [cell.strip() for cell in rows[0].strip('|').split('|')]
                    data_rows = rows[2:]  # skip separator row
                    parsed_rows: List[Dict[str, str]] = []
                    for row in data_rows:
                        cells = [cell.strip() for cell in row.strip('|').split('|')]
                        if len(cells) != len(header):
                            # pad missing cells
                            cells += [''] * (len(header) - len(cells))
                        parsed_rows.append({h: c for h, c in zip(header, cells)})
                    tables.append((header, parsed_rows))
                idx = j
                continue
        idx += 1
    return tables


if __name__ == "__main__":
    import argparse
    import json

    parser = argparse.ArgumentParser(description="Parse markdown tables into JSON")
    parser.add_argument("path", type=Path, help="Path to markdown file")
    args = parser.parse_args()
    parsed = parse_markdown_tables(args.path)
    print(json.dumps(parsed, indent=2))
