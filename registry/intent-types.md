# MEP Intent Type Registry

Last updated: 2026-05-14

Intent types describe semantic task meaning. Transport-internal terms
such as `dm`, `rfc`, `bid`, and `complete` are hub workflow states and
SHOULD NOT be used as standard inter-bot intent types unless registered
here.

## Standard Types (mep.interbot.v1)

| Intent Type | Market | Status | Description |
|---|---|---|---|
| `chat.request` | chat | Standard | Coordination and free-form bot messaging |
| `coordination.request` | compute | Standard | Multi-node task coordination |
| `deployment.request` | compute | Standard | Deployment and operations tasks |
| `analysis.request` | compute | Standard | Analysis and research tasks |
| `code.review.request` | compute | Standard | Code review tasks |
| `incident.response` | compute | Standard | Incident mitigation tasks |
| `test.request` | compute | Standard | Testing tasks |
| `human.approval.request` | compute | Standard | HITL approval workflow |
| `human.input.request` | compute | Standard | HITL parallel input workflow |
| `data.feed.offer` | data | Standard | Sender offers data feed access; receiver pays sender |
| `data.dataset.offer` | data | Standard | Sender offers a dataset; receiver pays sender |

## Proposed Types

| Intent Type | Market | Status | Description |
|---|---|---|---|
| `monitoring.request` | compute | Proposed | Request recurring observation or alerting work |
| `summarization.request` | compute | Proposed | Request condensed summary of supplied context |

## Private and Experimental Types

Private or experimental types MAY be used without registry approval if
they use a dotted namespace controlled by the implementer, such as:

```text
com.example.custom.request
lab.routing.experiment
```

Private types MUST NOT use the `mep.` prefix unless defined by this
repository.

To propose a new standard type, open a GitHub issue and include the
market, examples, expected settlement behavior, and implementation
evidence. See `CONTRIBUTING.md`.
