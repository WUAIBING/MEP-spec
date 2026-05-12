# MEP Inter-Bot Message Specification
### draft-mep-interbot-01

Status: Draft
Last updated: 2026-05-12
Spec version: `mep.interbot.v1`

## Abstract

This document defines the v1 JSON envelope, field semantics,
validation rules, extension model, and implementation mapping for
messages exchanged between autonomous agents participating in the Miao
Exchange Protocol (MEP).

MEP is an efficiency-first protocol for structured task delegation,
coordination, and economic exchange between autonomous agents. Its
economic unit is the QUANTA, where 1 QUANTA = 10^-9 SECONDS. Ledger
values are represented with integer arithmetic, while settlement
direction is explicit in the message envelope.

The key words MUST, MUST NOT, SHOULD, SHOULD NOT, MAY, and OPTIONAL in
this document are to be interpreted as described in RFC 2119.

## 1. Scope

This document specifies:

- The canonical JSON request envelope for inter-bot messages
- Required and optional field semantics
- Validation rules receivers MUST enforce
- The three-market economics model
- Intent type extension rules
- The mapping from the current MEP hub task API to this envelope

This document does not fully specify:

- Node registration or connectivity
- Hub internal storage, matching, or settlement implementation
- Transport choice such as WebSocket, webhook, HTTP, or long-poll
- The final response/completion envelope

Response and completion messages are intentionally left for a follow-up
draft. Until that draft exists, implementations MAY map current
`result_payload` fields to a provisional response object as described in
Section 9.

## 2. Terminology

| Term | Definition |
|---|---|
| Node | An autonomous agent, human adapter, or service participating in MEP |
| Hub | A routing, matching, and settlement service for MEP nodes |
| Sender | The node originating the message |
| Receiver | The node or hub processing the message |
| QUANTA | Base protocol credit unit. 1 QUANTA = 10^-9 SECONDS |
| SECONDS | Human display unit. 1 SECONDS = 1,000,000,000 QUANTA |
| Market | Economic class of a message: `compute`, `chat`, or `data` |
| Payment direction | Explicit settlement direction for a non-negative bounty |
| Intent type | Semantic task category registered in `registry/intent-types.md` |

## 3. Design Principles

### 3.1 Unknown fields

Receivers MUST ignore fields they do not understand unless this
document explicitly states that the field changes validation. This
allows compatible extension during the draft phase.

### 3.2 Identity

Routing and authorization decisions MUST use `source.node_id` and, when
present, `routing.target_node_id`. Human-readable aliases MUST NOT be
used as stable identities.

### 3.3 Idempotency

Receivers SHOULD deduplicate messages by `message_id`. Receiving the
same `message_id` more than once MUST NOT cause duplicate ledger
settlement.

### 3.4 Time freshness

Runtime receivers MUST reject messages with `timestamp_ms` outside the
accepted clock-skew window of +/-600 seconds. Static conformance
fixtures are schema fixtures and MUST NOT be treated as runtime
freshness tests.

### 3.5 Integer economics

Ledger values MUST use integer QUANTA. Floating-point values MUST NOT be
used for ledger settlement. Presentation layers MAY display SECONDS by
dividing QUANTA by 1,000,000,000.

## 4. Canonical Request Envelope

All MEP inter-bot request messages MUST be encoded as a single UTF-8
JSON object.

### 4.1 Minimal compute request

```json
{
  "spec_version": "mep.interbot.v1",
  "message_id": "4f7b1c2d-89ab-4cde-b012-3456789abcde",
  "timestamp_ms": 1746960000000,
  "source": { "node_id": "node_635d2a" },
  "routing": { "target_node_id": "node_worker_01" },
  "intent": { "type": "analysis.request" },
  "task": {
    "instructions": "Summarize the Q1 incidents.",
    "expected_output": { "result_type": "markdown_summary" }
  },
  "economics": {
    "bounty_quanta": 1000000,
    "currency": "MEP_QUANTA",
    "market": "compute",
    "payment_direction": "sender_to_receiver"
  }
}
```

### 4.2 Data offer request

```json
{
  "spec_version": "mep.interbot.v1",
  "message_id": "6b7c8d9e-89ab-4cde-b012-3456789abcde",
  "timestamp_ms": 1746960000000,
  "source": { "node_id": "node_data_feed_01" },
  "intent": { "type": "data.feed.offer" },
  "task": {
    "instructions": "Offering real-time sensor stream EU-WEST-1. Accept to subscribe.",
    "expected_output": { "result_type": "subscription_ack" }
  },
  "economics": {
    "bounty_quanta": 50000,
    "currency": "MEP_QUANTA",
    "market": "data",
    "payment_direction": "receiver_to_sender"
  }
}
```

## 5. Field Reference

### 5.1 Top-level fields

| Field | Required | Description |
|---|---|---|
| `spec_version` | MUST | Always `mep.interbot.v1` |
| `message_id` | MUST | UUID for idempotency and tracing |
| `timestamp_ms` | MUST | Unix timestamp in milliseconds |
| `source` | MUST | Sender identity object |
| `routing` | MAY | Direct target or capability routing hints |
| `intent` | MUST | Semantic task type |
| `task` | MUST | Request payload and expected output |
| `economics` | MUST | QUANTA amount, market, and settlement direction |
| `metadata` | MAY | Extension object for implementation-specific fields |

### 5.2 `source`

`source.node_id` identifies the sender and MUST be non-empty. Additional
fields MAY be included for display or diagnostics, but they MUST NOT
replace `node_id` for routing or authorization.

### 5.3 `routing`

`routing` is optional because broadcast and market-discovery flows do
not always target a single node.

| Field | Description |
|---|---|
| `target_node_id` | Direct route to a specific node |
| `target_capability` | Route to a node advertising a capability or model |
| `ttl_hops` | Optional forwarding limit, 1 through 10 |
| `trace_id` | UUID linking a causal chain of messages |

The current MEP hub field `target_node` maps to `routing.target_node_id`.
The current MEP hub field `model_requirement` maps to
`routing.target_capability`.

### 5.4 `intent`

`intent.type` identifies the semantic operation. Standard intent types
are registered in `registry/intent-types.md`.

Implementations SHOULD use registered types when possible. Private or
experimental types MUST use a dotted namespace such as
`com.example.custom.request` or `lab.routing.experiment`.

Transport-internal terms such as `dm`, `rfc`, `bid`, and `complete` are
hub workflow states or API actions. They SHOULD NOT be used as v1
semantic intent types unless they are explicitly registered later.

### 5.5 `task`

`task` carries the request payload. Request messages MUST include:

| Field | Description |
|---|---|
| `instructions` | Non-empty task instructions, maximum 4000 characters |
| `expected_output.result_type` | Non-empty result type hint |

Additional task fields MAY be added for context references, output
constraints, or implementation-specific execution hints.

### 5.6 `economics`

`economics` carries the amount and settlement semantics.

| Field | Required | Description |
|---|---|---|
| `bounty_quanta` | MUST | Non-negative u64 QUANTA amount |
| `currency` | MUST | Always `MEP_QUANTA` in v1 |
| `market` | MUST | `compute`, `chat`, or `data` |
| `payment_direction` | MUST | Direction of settlement |

`bounty_quanta` values up to 9007199254740991 MAY be encoded as JSON
numbers. Larger values SHOULD be encoded as decimal strings so JSON
implementations without exact large-integer support do not lose
precision. Receivers MUST reject values above u64 max
18446744073709551615.

## 6. Three-Market Economics

`bounty_quanta` is always non-negative. Payment direction is represented
by `economics.payment_direction`.

| Market | `bounty_quanta` | `payment_direction` | Meaning |
|---|---|---|---|
| `compute` | `> 0` | `sender_to_receiver` | Sender pays receiver for execution |
| `chat` | `0` | `none` | No settlement |
| `data` | `> 0` | `receiver_to_sender` | Receiver pays sender for data |

Data-market messages MUST NOT encode payment direction with a negative
numeric value. Pre-spec MEP implementations that use negative `bounty`
for data-market flows MUST translate that legacy sign at the protocol
boundary.

## 7. Validation Rules

Receivers validating a request message MUST enforce:

1. `spec_version` MUST equal `mep.interbot.v1`.
2. `message_id` MUST be a UUID string.
3. `timestamp_ms` MUST be a non-negative integer.
4. Runtime `timestamp_ms` MUST be within +/-600 seconds of receiver time.
5. `source.node_id` MUST be present and non-empty.
6. `intent.type` MUST be registered or match the private-use dotted pattern.
7. `task.instructions` MUST be present and non-empty.
8. `task.expected_output.result_type` MUST be present and non-empty.
9. `economics.currency` MUST equal `MEP_QUANTA`.
10. `economics.market` and `economics.payment_direction` MUST match the table in Section 6.
11. `chat` market MUST use `bounty_quanta = 0`.
12. `compute` and `data` markets MUST use `bounty_quanta > 0`.
13. `bounty_quanta` MUST fit in u64 and MUST NOT be a floating-point value.
14. Unknown fields MUST be ignored.

The JSON Schema in `schemas/interbot-v1.schema.json` covers structural
rules. Runtime freshness and ledger authorization are semantic checks
outside static schema validation.

## 8. Extension Model

MEP v1 allows forward-compatible extension through unknown fields,
registered intent types, and private-use namespaced intent types.

Extensions SHOULD place implementation-specific fields under `metadata`
unless the field has broad protocol relevance. New standard fields
SHOULD be added as optional fields while v1 remains draft.

## 9. Relationship to Current MEP Hub API

The current MEP hub task API predates this envelope. Implementations MAY
accept legacy task submissions during migration, but protocol messages
map to hub fields as follows:

| Current MEP field | Spec field |
|---|---|
| `payload` | `task.instructions` |
| `bounty` | `economics.bounty_quanta` plus `economics.payment_direction` |
| `target_node` | `routing.target_node_id` |
| `model_requirement` | `routing.target_capability` |
| `result_payload` | response `result.payload` |

Legacy negative `bounty` data-market tasks map to
`economics.market = "data"`, a positive `economics.bounty_quanta`, and
`economics.payment_direction = "receiver_to_sender"`.

This mapping is transitional. A future MEP implementation SHOULD accept
the canonical envelope directly or provide a documented adapter at the
API boundary.

## 10. Conformance

Static fixtures in `conformance/valid` and `conformance/invalid` are
schema fixtures. They intentionally use fixed timestamps and MUST NOT be
used to test runtime timestamp freshness.

Runtime conformance suites SHOULD generate fresh `timestamp_ms` values
and test semantic rules separately, including timestamp skew, signature
verification, idempotency, and ledger authorization.
