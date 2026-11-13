#!/usr/bin/env python3
"""Validate the small, dependency-free interaction contract."""
from __future__ import annotations

import re
import sys
from pathlib import Path

REQUIRED_IDS = {
    "diagram", "scene", "viewport", "detail-panel", "find-button", "route-button",
    "reset-button", "theme-toggle", "presentation-toggle", "print-button",
    "search-dialog", "search-input", "search-results", "overview",
}
REQUIRED_HOOKS = {
    "node ID": ("data-node-id", "dataset.nodeId"),
    "node kind": ("data-node-kind", "dataset.nodeKind"),
    "node label": ("data-node-label", "dataset.nodeLabel"),
    "edge from": ("data-edge-from", "dataset.edgeFrom"),
    "edge to": ("data-edge-to", "dataset.edgeTo"),
}
REQUIRED_TOKENS = ("prefers-reduced-motion", "addEventListener", "location.hash")


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_diagram.py <html-file>", file=sys.stderr)
        return 2
    path = Path(sys.argv[1])
    if not path.is_file():
        fail(f"file does not exist: {path}")
    raw = path.read_text(encoding="utf-8")
    lowered = raw.lower()
    if "<script src=" in lowered or re.search(r'<link[^>]+href=["\']https?://', lowered):
        fail("external runtime dependency found")
    if "innerhtml" in lowered or re.search(r'@import\s+url\(\s*["\']?https?://', lowered):
        fail("unsafe HTML injection or external CSS import found")
    missing = [name for name, aliases in REQUIRED_HOOKS.items() if not any(alias in raw for alias in aliases)]
    missing.extend(token for token in REQUIRED_TOKENS if token not in raw)
    if missing:
        fail("missing required contract tokens: " + ", ".join(missing))
    ids = set(re.findall(r'\bid=["\']([^"\']+)', raw))
    missing_ids = sorted(REQUIRED_IDS - ids)
    if missing_ids:
        fail("missing required element IDs: " + ", ".join(missing_ids))
    graph_node_ids = re.findall(r'\bid:\s*["\']([^"\']+)', raw)
    if len(graph_node_ids) != len(set(graph_node_ids)):
        fail("duplicate graph node IDs found")
    node_ids = graph_node_ids + re.findall(r'data-node-id=["\']([^"\']+)', raw)
    node_ids = list(dict.fromkeys(node_ids))
    if len(graph_node_ids) < 2:
        fail("at least two stable node IDs are required")
    edge_pairs = re.findall(r'\bfrom:\s*["\']([^"\']+)["\'][\s\S]{0,120}?\bto:\s*["\']([^"\']+)', raw)
    edge_pairs.extend(re.findall(r'data-edge-from=["\']([^"\']+)["\'][^>]*data-edge-to=["\']([^"\']+)', raw))
    if not edge_pairs:
        fail("at least one directed edge is required")
    unknown = sorted({value for pair in edge_pairs for value in pair} - set(node_ids))
    if unknown:
        fail("edge references unknown node IDs: " + ", ".join(unknown))
    if ('role="button"' not in raw and "role='button'" not in raw
            and 'setAttribute("role","button")' not in raw
            and "setAttribute('role','button')" not in raw):
        fail("nodes need keyboard-operable button semantics")
    if "tabindex" not in lowered:
        fail("nodes need a keyboard focus path")
    print(f"OK: {path} ({len(node_ids)} nodes, {len(edge_pairs)} edge declarations)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
