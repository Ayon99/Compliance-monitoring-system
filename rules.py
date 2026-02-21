from collections import defaultdict
from datetime import datetime

AUTH_FAILURE_THRESHOLD = 3


def auth_failure_rule(events: list[dict]) -> list[dict]:
    """
    Rule:
    If a user has more than AUTH_FAILURE_THRESHOLD auth failures,
    create a violation.
    """

    failures_by_user = defaultdict(int)

    # Step 1: count failures per user
    for event in events:
        if event.get("event_type") == "AUTH_FAILURE":
            user_id = event.get("user_id")
            if user_id:
                failures_by_user[user_id] += 1

    violations = []

    # Step 2: generate violations
    for user_id, count in failures_by_user.items():
        if count > AUTH_FAILURE_THRESHOLD:
            violations.append({
                "rule_name": "AUTH_FAILURE_THRESHOLD",
                "user_id": user_id,
                "details": f"{count} authentication failures detected",
                "detected_at": datetime.utcnow()
            })

    return violations
