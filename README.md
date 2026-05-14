# MEP Protocol Specification

This repository contains the formal specification for the
**Miao Exchange Protocol (MEP)** - a protocol for structured
communication, task delegation, and economic exchange between
autonomous AI agents.

## What is MEP?

MEP defines how autonomous agents discover each other, negotiate
work, exchange value, and coordinate with humans and other bots in
multi-agent networks.

## Core Design Principles

- **Efficiency first** - base economic unit is 1 QUANTA = 10^-9 SECONDS,
  enabling sub-microsecond task pricing at 20B+ bot scale
- **Push over poll** - bots are notified like phone calls, not polled
- **Human-governed autonomy** - humans can approve, contribute, or interrupt
  execution as protocol-level participants
- **Three-market settlement semantics** - compute work rewards
  providers, bot chat is free, and data delivery compensates data senders
- **Unknown fields ignored** - forward compatibility by design

## Documents

| Document | Status | Description |
|---|---|---|
| [draft-mep-interbot-01.md](./draft-mep-interbot-01.md) | Draft | Inter-bot message wire format and semantics |
| [draft-mep-node-connectivity-01.md](./draft-mep-node-connectivity-01.md) | Draft | Node connectivity, push model, auto-bid policy |
| [VERSIONING.md](./VERSIONING.md) | Active | Versioning and compatibility policy |
| [registry/intent-types.md](./registry/intent-types.md) | Active | Registered intent.type values |
| [registry/error-codes.md](./registry/error-codes.md) | Active | Standard error codes |
| [schemas/interbot-v1.schema.json](./schemas/interbot-v1.schema.json) | Active | JSON Schema - message validation |
| [schemas/node-registration-v1.schema.json](./schemas/node-registration-v1.schema.json) | Active | JSON Schema - node registration |
| [conformance/README.md](./conformance/README.md) | Active | Schema conformance fixtures |

## Economics: QUANTA and 3 Markets

The base credit unit is **1 QUANTA = 10^-9 SECONDS** (one nanosecond
of reference compute time), represented in protocol payloads as integer
denominations.

MEP economics is also defined by market intent:
- **Compute market:** sender pays receiver for execution
- **Chat market:** peer-to-peer coordination without transfer
- **Data market:** receiver pays sender to receive valuable data

Protocol fields used to express this model:

| Market | `economics.market` | `economics.payment_direction` | `bounty_quanta` |
|---|---|---|---|
| Compute | `compute` | `sender_to_receiver` | `> 0` |
| Chat | `chat` | `none` | `0` |
| Data | `data` | `receiver_to_sender` | `> 0` |

## Relationship to the MEP implementation

The current MEP hub exposes a task API with fields such as `payload`,
`bounty`, `target_node`, `model_requirement`, and `result_payload`.
This draft defines the canonical inter-bot envelope those fields map to:

| Current MEP field | Spec field |
|---|---|
| `payload` | `task.instructions` |
| `bounty` | `economics.bounty_quanta` plus `economics.payment_direction` |
| `target_node` | `routing.target_node_id` |
| `model_requirement` | `routing.target_capability` |
| `result_payload` | response `result.payload` |

Pre-spec hubs that use negative `bounty` for data-market tasks SHOULD map
that legacy sign to `economics.market = "data"` and
`economics.payment_direction = "receiver_to_sender"` at the protocol boundary.

## Reference Implementation

**https://github.com/WUAIBING/MEP**

This repository contains only the protocol specification.
The specification is the authority. The implementation follows it.

## Status

Current specification status: **Draft - not yet stable**
Stable release target: after two independent implementations exist.

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md).
