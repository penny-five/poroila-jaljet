"""Move the former interactive evidence map into a maintainable JSON source."""
from __future__ import annotations

import ast
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "app.js"
TARGET = ROOT / "src/_data/graph.json"


def array_value(source: str, declaration: str):
    start = source.index(declaration) + len(declaration) - 1
    depth = 0
    quote = None
    escaped = False
    for end in range(start, len(source)):
        char = source[end]
        if quote:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                quote = None
            continue
        if char in {"'", '"'}:
            quote = char
        elif char == "[":
            depth += 1
        elif char == "]":
            depth -= 1
            if depth == 0:
                return ast.literal_eval(source[start:end + 1])
    raise ValueError(f"Unclosed array in {declaration}")


def main() -> None:
    source = SOURCE.read_text(encoding="utf-8")
    nodes_raw = array_value(source, "const nodeData=[")
    edges_raw = array_value(source, "const edges=[")
    nodes = [
        {
            "id": row[0],
            "name": row[1],
            "label": row[2],
            "subtitle": row[3],
            "position": {"x": row[4], "y": row[5]},
            "type": row[6],
            "refs": row[7],
            "description": row[8],
            "evidenceStatus": row[9],
        }
        for row in nodes_raw
    ]
    edges = [{"from": row[0], "to": row[1], "status": row[2]} for row in edges_raw]
    TARGET.write_text(json.dumps({"nodes": nodes, "edges": edges}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Legacy evidence map transferred: {len(nodes)} entries and {len(edges)} links.")


if __name__ == "__main__":
    main()
