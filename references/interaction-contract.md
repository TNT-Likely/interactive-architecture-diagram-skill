# Interaction contract

The diagram is an inspectable semantic graph rendered into one SVG scene. The visual layer may change, but these attributes and behaviors stay stable so a user can move between diagrams without relearning the controls.

## Graph shape

```js
const GRAPH = {
  nodes: [
    {
      id: "bff",
      kind: "backend",
      label: "Service gateway",
      role: "Routes requests into domain modules",
      detail: "Longer explanation shown in the detail panel.",
      evidence: "Design decision or source link"
    }
  ],
  edges: [
    { from: "client", to: "bff", label: "HTTPS" }
  ]
};
```

Required node fields are `id`, `kind`, `label`, and `role`. Required edge fields are `from`, `to`, and `label`. IDs must be unique and edges must reference existing nodes. Optional `detail`, `evidence`, `status`, `href`, and `linkLabel` fields enrich the inspector without changing the graph. The starter renders `status` as a state badge and accepts only `http:`, `https:`, or `file:` links for `href`.

## SVG hooks

Each rendered node has:

```html
<g data-node-id="bff" data-node-kind="backend" data-node-label="Service gateway" tabindex="0" role="button" aria-label="Service gateway">
```

Each rendered relationship has:

```html
<g data-edge-from="client" data-edge-to="bff" data-edge-label="HTTPS">
```

The hooks are intentionally semantic. CSS should style kinds and state attributes such as `data-selected`, `data-related`, and `data-route-step`; JavaScript should not depend on generated coordinates or a node's visible text.

## Required states

- **idle:** all nodes and edges readable.
- **focused:** selected node has a strong outline; direct neighbors and edges remain visible.
- **searching:** the finder is modal to the keyboard, and selecting a result focuses the node.
- **routing:** the user chooses a directed start and end; a missing path reports a clear message.
- **camera:** zoom and pan affect only the scene; controls remain reachable.
- **presentation:** secondary controls are hidden or minimized while the graph fills the viewport.
- **reduced motion:** no pulse, trace, or camera animation is required to understand the graph.

## Accessibility and deep links

Nodes must be keyboard focusable and operable with Enter/Space. Buttons need an accessible name and visible focus ring. Dialog-like panels close with Escape and restore focus to their launcher when possible. Hash state is shareable and must be ignored safely when it contains an unknown ID.

## Evidence and uncertainty

Use `evidence` for a human-readable source label or local link. Do not put secrets or private repository paths into a public skill example. Use a dashed edge or a `future` kind for candidates; do not use color alone to communicate status.
