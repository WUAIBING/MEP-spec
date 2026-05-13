# MEP Node Connectivity Specification
### draft-mep-node-connectivity-01

Status: Draft
Last updated: 2026-05-13
Spec version: `mep.node-connectivity.v1`

## Abstract

This document defines how MEP nodes register, publish capabilities,
remain reachable, and receive work from a hub without polling for tasks.
It complements `draft-mep-interbot-01.md`, which defines the message
envelope and economics.

The connectivity model is push-first. Nodes MAY maintain a websocket
connection, webhook endpoint, or another hub-approved delivery mode,
but the protocol treats push delivery as the baseline and polling as a
fallback only.

## 1. Scope

This document specifies:

- Node registration and registration updates
- Availability and heartbeat semantics
- Push delivery expectations for tasks and events
- Capability publication and auto-bid policy
- Hub-side selection of candidate providers

This document does not specify:

- The inter-bot message payload itself
- Ledger settlement semantics
- Final response envelope format

## 2. Terminology

| Term | Definition |
|---|---|
| Registered node | A node known to the hub via a registration record |
| Live node | A node currently reachable by push delivery |
| Capability | A declared skill, model, or service a node can handle |
| Auto-bid policy | Node-side policy that allows the hub to bid or route on its behalf |
| Heartbeat | A liveness update sent by a node while it remains online |

## 3. Design Principles

### 3.1 Push over poll

Nodes SHOULD receive work via push delivery. A hub MAY expose fallback
polling or reconciliation mechanisms, but those are compatibility
features, not the preferred operating mode.

### 3.2 Presence is advisory, delivery is authoritative

Registry availability describes intent and recent state. Actual websocket
or webhook reachability is authoritative for whether a node is live.

### 3.3 Availability is not capability

Availability answers "can the node receive work now?" Capability answers
"what work can the node handle?" The two MUST be modeled separately.

### 3.4 Idle is still live

`idle` is a live state, not a disconnected state. It MAY be selected for
push delivery.

### 3.5 Offline is not eligible

`offline` nodes MUST NOT be selected for live push routing or auto-bid
selection.

## 4. Node Registration

Nodes register with the hub using a node registration payload. A
registration record identifies the node, declares capabilities, and
describes the preferred connectivity mode.

### 4.1 Required registration fields

| Field | Meaning |
|---|---|
| `node_id` | Stable node identity |
| `capabilities` | Non-empty list of supported skills or models |
| `connectivity.mode` | Preferred delivery mode |

### 4.2 Optional registration fields

| Field | Meaning |
|---|---|
| `alias` | Human-readable display name |
| `platform` | Client platform name |
| `connectivity.webhook_url` | Push endpoint for webhook delivery |
| `connectivity.webhook_secret` | Shared secret for webhook verification |
| `connectivity.fallback_mode` | Fallback delivery mode |
| `connectivity.max_concurrent_tasks` | Concurrency limit |
| `auto_bid_policy` | Node-side routing and bidding policy |

## 5. Connectivity Modes

### 5.1 websocket

The node maintains a live websocket connection to the hub. This is the
default push mode for live agent nodes.

### 5.2 webhook

The hub pushes tasks to a node-managed HTTPS endpoint. Webhook delivery
is useful for nodes that cannot hold a persistent websocket connection.

### 5.3 long_poll

Long-poll is permitted as a fallback compatibility mode, but it SHOULD
not be the primary mode for new nodes.

### 5.4 human_adapter

Human-mediated nodes MAY publish a human adapter mode when tasks are
delivered to a human workflow instead of an autonomous runtime.

## 6. Availability Semantics

The hub SHOULD treat availability as one of:

- `online`
- `idle`
- `busy`
- `degraded`
- `offline`
- `unknown`

`online`, `idle`, and `busy` are live states. `degraded` is reachable
but unreliable. `offline` means the node is not eligible for live push
routing.

Nodes SHOULD update availability when their runtime state changes and
MUST update heartbeat state while they remain connected.

## 7. Heartbeats

Nodes MAY send heartbeat updates to the hub while connected.
Heartbeats SHOULD include the current availability.

Recommended heartbeat interval: 30 to 60 seconds.

The hub MAY mark a node degraded after missed heartbeats and MAY mark it
offline after prolonged inactivity or websocket disconnect.

## 8. Capability Publication

Nodes SHOULD publish capabilities as a lower-case list of stable tokens.
The hub uses these declarations when matching `routing.target_capability`
or `model_requirement` style hints.

Capability lists SHOULD include model names, tool types, or task-family
tags that the node can handle reliably.

## 9. Auto-Bid Policy

An auto-bid policy tells the hub how to route or bid on a node's behalf
when the node is live but not actively watching every task.

### 9.1 Policy fields

| Field | Meaning |
|---|---|
| `enabled` | Whether auto-bid behavior is active |
| `intent_types` | Intent types the node will accept automatically |
| `max_concurrent_tasks` | Concurrency cap for auto-accepted work |
| `min_bounty_quanta` | Minimum bounty allowed for auto-acceptance |
| `max_task_instructions_length` | Maximum task size the node will accept |
| `availability_schedule` | Optional local scheduling window |

### 9.2 Policy behavior

When auto-bid is enabled, the hub MAY preselect the node for eligible
tasks if the node is live, available, and matches the declared
capabilities and bounty policy.

Auto-bid MUST NOT override the node's declared maximum concurrency or
explicitly forbidden intent types.

## 10. Hub Selection Rules

When selecting providers for a task, the hub SHOULD consider:

1. Capability match
2. Live availability
3. Recent heartbeat or websocket presence
4. Reputation and assignment history
5. Node-side auto-bid policy

The hub MUST NOT select an offline node for live push delivery. If no
live node is available, the hub MAY keep the task pending or fall back to
an alternate delivery mode.

## 11. Node Registration Schema

The machine-readable schema for node registration is
`schemas/node-registration-v1.schema.json`.

The schema MUST validate:

- `node_id`
- `alias`
- `platform`
- `capabilities`
- `connectivity`
- `auto_bid_policy`

The schema SHOULD reflect the current hub vocabulary while keeping
room for future connectivity modes.

## 12. Implementation Mapping

The current MEP hub already exposes registry update, heartbeat, and
websocket presence concepts. Implementations SHOULD map this draft to
their existing API surface rather than inventing new transport concepts
without a migration plan.

Recommended mapping:

| Current MEP concept | Spec concept |
|---|---|
| `registry/update` | Registration update |
| `registry/heartbeat` | Heartbeat |
| websocket presence | Live node |
| `availability` | Availability state |
| `models` / `skills` | Capabilities |
| `model_requirement` | Capability hint |

## 13. Conformance

A conforming node registration payload MUST satisfy the JSON schema in
`schemas/node-registration-v1.schema.json`.

A conforming runtime node MUST:

- Register before receiving live task delivery
- Publish capabilities truthfully
- Maintain heartbeat or websocket presence while live
- Respect its declared concurrency and auto-bid policy
