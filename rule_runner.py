import psycopg2
from rules import auth_failure_rule

conn = psycopg2.connect(
    dbname="compliance_db",
    user="postgres",
    password="2006",
    host="localhost",
    port="5432"
)

conn.autocommit = True


def fetch_normalized_events():
    cursor = conn.cursor()
    cursor.execute("""
        SELECT service, severity, event_type, message, user_id, event_time
        FROM normalized_events
    """)
    rows = cursor.fetchall()
    cursor.close()

    events = []
    for r in rows:
        events.append({
            "service": r[0],
            "severity": r[1],
            "event_type": r[2],
            "message": r[3],
            "user_id": r[4],
            "event_time": r[5]
        })

    return events


def store_violations(violations):
    cursor = conn.cursor()
    for v in violations:
        cursor.execute("""
            INSERT INTO violations (rule_name, user_id, details, detected_at)
            VALUES (%s, %s, %s, %s)
        """, (
            v["rule_name"],
            v["user_id"],
            v["details"],
            v["detected_at"]
        ))
    cursor.close()


def run():
    events = fetch_normalized_events()
    violations = auth_failure_rule(events)
    store_violations(violations)
    print(f"{len(violations)} violations stored.")


if __name__ == "__main__":
    run()
