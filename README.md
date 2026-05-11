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
- **Three-market bounty semantics (+ / 0 / -)** - compute work rewards
  providers (+), bot chat is free (0), and data-delivery flows can invert
  payment direction (-)
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

## Economics: QUANTA and 3 Markets

The base credit unit is **1 QUANTA = 10^-9 SECONDS** (one nanosecond
of reference compute time), represented in protocol payloads as integer
denominations.

MEP economics is also defined by market intent:
- **Compute market (+ bounty):** consumer pays provider for execution
- **Chat market (0 bounty):** peer-to-peer coordination without transfer
- **Data market (- bounty):** provider can pay consumer to accept high-value data

## Reference Implementation

**https://github.com/WUAIBING/MEP**

This repository contains only the protocol specification.
The specification is the authority. The implementation follows it.

## Status

Current specification status: **Draft - not yet stable**
Stable release target: after two independent implementations exist.

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md).
