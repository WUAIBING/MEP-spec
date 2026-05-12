# MEP Inter-Bot Message Specification
### draft-mep-interbot-01

Status: Draft
Last updated: 2026-05-11

## Scope

This document defines the v1 JSON envelope and validation rules for MEP inter-bot messages.

## Three-Market Economics

- `bounty_quanta` is a non-negative integer (`u64`)
- `currency` is `MEP_QUANTA`
- `market` and `payment_direction` define transfer direction
- Data-market messages use a positive `bounty_quanta`; the direction is
  expressed by `payment_direction`, not by a negative numeric value.

| Market | bounty_quanta | payment_direction |
|---|---|---|
| `compute` | `> 0` | `sender_to_receiver` |
| `chat` | `0` | `none` |
| `data` | `> 0` | `receiver_to_sender` |

## Minimal Envelope

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

## Validation Rules

1. `spec_version` MUST equal `mep.interbot.v1`.
2. `message_id` MUST be UUID.
3. `timestamp_ms` MUST be within +/-600 seconds.
4. `task.instructions` MUST be present and non-empty for request messages.
5. `bounty_quanta` MUST be integer and >= 0.
6. `bounty_quanta` values above 9007199254740991 SHOULD be encoded as
   decimal strings by JSON implementations that cannot preserve larger
   integers exactly. Ledger implementations MUST parse them with integer
   arithmetic and reject values above u64 max.
7. `market`/`payment_direction` MUST match the table above.
8. `chat` market MUST use `bounty_quanta = 0`.
9. Unknown fields MUST be ignored.

## Implementation Mapping

The current MEP hub task API predates this envelope. Implementations MAY
accept legacy task submissions during migration, but protocol messages map
to hub fields as follows:

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
