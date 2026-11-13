# Interactive Architecture Diagram

A dependency-free Codex skill for turning a verified system graph into an inspectable architecture diagram. The browser artifact is one self-contained HTML file with inline CSS, JavaScript, and SVG.

The interaction shell supports node search and inspection, directed route tracing, zoom/pan/reset, a minimap, light/dark themes, presentation mode, keyboard access, reduced-motion preferences, and shareable `node=`/`route=` hash state.

## Use the skill

Copy the skill directory into a Codex skills directory, then invoke it for an architecture or service-topology diagram:

```sh
cp -R interactive-architecture-diagram "$CODEX_HOME/skills/"
```

If `CODEX_HOME` is unset, use the local agent skills directory for your environment. The skill can also be loaded directly from this repository while editing.

## Build a diagram

1. Start from [`assets/starter.html`](assets/starter.html).
2. Replace only the `GRAPH` object, the title, and the evidence links with facts verified for the target system.
3. Keep stable lowercase node IDs and directed edge endpoints. Use `future` nodes or dashed edges for candidates.
4. Run the validator:

```sh
python3 scripts/validate_diagram.py assets/starter.html
```

Open the result from `file://` or a static server and exercise the smoke path: select a node, search, trace a route, use `m`, zoom/pan/reset, switch theme, press Escape, and reload a hash URL.

See [`references/interaction-contract.md`](references/interaction-contract.md) for the stable graph and accessibility contract.
