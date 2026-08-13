import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALID_DIR = ROOT / "conformance" / "federation_semantic" / "valid"
INVALID_DIR = ROOT / "conformance" / "federation_semantic" / "invalid"

RESPONSE_DECISIONS = {
    "collaboration.invitation.accept": "accept",
    "collaboration.invitation.reject": "reject",
    "collaboration.invitation.counter": "counter",
    "collaboration.invitation.revoke": "revoke",
}


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def semantic_errors(message: dict) -> list[str]:
    errors: list[str] = []
    timestamp = message.get("timestamp_ms")
    expires_at = message.get("expires_at_ms")
    if isinstance(timestamp, int) and isinstance(expires_at, int) and expires_at <= timestamp:
        errors.append("expires_at_ms must be later than timestamp_ms")

    source_id = (message.get("source") or {}).get("node_id")
    target_id = (message.get("target") or {}).get("node_id")
    event_type = message.get("event_type")

    profile = message.get("profile")
    if isinstance(profile, dict) and profile.get("node_id") != source_id:
        errors.append("profile.node_id must equal source.node_id")

    presence = message.get("presence")
    if isinstance(presence, dict) and presence.get("node_id") != source_id:
        errors.append("presence.node_id must equal source.node_id")

    invitation = message.get("invitation")
    if isinstance(invitation, dict):
        if invitation.get("requester_node_id") != source_id:
            errors.append("invitation.requester_node_id must equal source.node_id")
        if invitation.get("target_node_id") != target_id:
            errors.append("invitation.target_node_id must equal target.node_id")
        if invitation.get("requester_node_id") == invitation.get("target_node_id"):
            errors.append("an invitation cannot target its requester")

    response = message.get("response")
    expected_decision = RESPONSE_DECISIONS.get(event_type)
    if isinstance(response, dict) and expected_decision and response.get("decision") != expected_decision:
        errors.append(f"{event_type} requires decision={expected_decision}")

    grant = message.get("grant")
    if isinstance(grant, dict):
        if source_id == target_id:
            errors.append("a preview grant must target the counterparty")
        if grant.get("execution_allowed") is not False:
            errors.append("preview grants cannot authorize execution")

    return errors


def main() -> int:
    failures: list[str] = []
    for path in sorted(VALID_DIR.glob("*.json")):
        errors = semantic_errors(load_json(path))
        if errors:
            failures.append(f"{path}: expected semantically valid, got {errors[0]}")
    for path in sorted(INVALID_DIR.glob("*.json")):
        errors = semantic_errors(load_json(path))
        if not errors:
            failures.append(f"{path}: expected semantic failure, got valid")

    if failures:
        for failure in failures:
            print(failure)
        return 1
    print("federation semantic fixtures passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
