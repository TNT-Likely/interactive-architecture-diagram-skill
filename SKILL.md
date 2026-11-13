---
name: interactive-architecture-diagram
description: "Use when a user wants an architecture, service-topology, data-flow, or deployment diagram that can be explored in a browser with node inspection, search, route tracing, camera controls, themes, and keyboard access."
---

# Interactive architecture diagrams

Use this skill when a user wants an architecture, service topology, data-flow, or deployment diagram that can be explored in a browser. It is for diagrams that need inspection and navigation; use a static Mermaid/SVG diagram for a one-shot picture or a small flow.

## Workflow

1. Extract a factual semantic graph before writing markup. Give every node a stable lowercase `id`, a `kind`, a short label, a one-line role, and optional evidence/detail copy. Give every directed edge stable `from`/`to` IDs and a concise label.
2. Copy `assets/starter.html` into the target document. Replace only the `GRAPH`, title, subtitle, legend copy, and local evidence links. Keep the interaction shell intact unless the user explicitly needs another behavior.
3. Keep the file self-contained: inline CSS, inline JavaScript, and inline SVG. Do not add a CDN, font request, framework bundle, or runtime API. Keep private URLs, credentials, repository paths, and project-only facts in the local consumer rather than the public skill.
4. Run `scripts/validate_diagram.py <file>` and open the file from `file://` or a static server. Exercise the smoke path: focus a node, search, trace a route, zoom/pan/reset, switch theme, press Escape, and reload a hash URL.

## Interaction contract

The starter provides these behaviors:

- click, Enter, and Space focus a node and show its details plus directly connected edges;
- `/` opens node search; `r` starts route selection; `m` opens the overview map; `+`, `-`, and `0` control the camera; `t` toggles theme; `f` toggles presentation mode; Escape clears transient state;
- a route uses directed edges and reports each step; the URL hash restores `node=<id>` or `route=<from>,<to>`;
- reduced-motion preferences disable ambient and route animations without disabling information;
- controls and nodes have accessible labels, visible focus states, and pointer-independent keyboard paths.

Read [references/interaction-contract.md](references/interaction-contract.md) before changing the shell or adding a new semantic kind. The starter is the canonical small implementation; do not copy a large project-specific HTML as the skill template.

## Data and privacy rules

Use semantic kinds such as `frontend`, `backend`, `database`, `messagebus`, `cloud`, `external`, `security`, and `future`. A kind controls visual treatment and legend grouping; it must not imply a security guarantee. Put uncertainty in the detail copy (`planned`, `candidate`, `verified`) instead of drawing an unqualified solid edge.

Keep the graph readable: prefer 8–20 meaningful nodes, split very large systems into linked views, and use a detail panel for long descriptions. Preserve the source system's ownership and trust boundaries. Never invent a data store, protocol, deployment, or success state just to make the picture symmetrical.

## Validation

Run:

```sh
python3 scripts/validate_diagram.py assets/starter.html
```

The validator checks the required controls, graph attributes, keyboard hooks, reduced-motion CSS, and absence of external runtime dependencies. For a consumer diagram, run the same command against the consumer file and perform a browser smoke test. A passing validator does not prove the architecture facts; those still require review against the source design.
