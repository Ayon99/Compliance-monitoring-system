from datetime import datetime

LEVEL_TO_SEVERITY = {
    "INFO": 1,
    "WARN": 2,
    "ERROR": 3
}

def normalize_log(raw_log: dict) -> dict:
    """
    Convert raw log into normalized event
    """

    level = raw_log.get("level", "").upper()

    normalized = {
        "service": raw_log.get("service", "unknown"),
        "severity": LEVEL_TO_SEVERITY.get(level, 0),
        "event_type": classify_event(raw_log),
        "message": raw_log.get("message"),
        "user_id": raw_log.get("user_id"),
        "event_time": raw_log.get("ingested_at", datetime.utcnow())
    }

    return normalized


def classify_event(raw_log: dict) -> str:
    """
    Very naive event classifier (we improve later)
    """

    msg = (raw_log.get("message") or "").lower()

    if "token" in msg or "auth" in msg:
        return "AUTH_FAILURE"

    if "payment" in msg:
        return "PAYMENT_EVENT"

    return "GENERIC_EVENT"
