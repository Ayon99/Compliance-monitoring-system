import psycopg2
from normalizer import normalize_log

conn = psycopg2.connect(
    dbname="compliance_db",
    user="postgres",
    password="2006",
    host="localhost",
    port="5432"
)

conn.autocommit = True


def fetch_raw_logs():
    cursor = conn.cursor()
    cursor.execute("""
        SELECT service, level, message, user_id, ingested_at
        FROM raw_logs
    """)
    rows = cursor.fetchall()
    cursor.close()

    logs = []
    for r in rows:
        logs.append({
            "service": r[0],
            "level": r[1],
            "message": r[2],
            "user_id": r[3],
            "ingested_at": r[4]
        })

    return logs


def store_normalized(event: dict):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO normalized_events
        (service, severity, event_type, message, user_id, event_time)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        event["service"],
        event["severity"],
        event["event_type"],
        event["message"],
        event["user_id"],
        event["event_time"]
    ))
    cursor.close()


def run():
    raw_logs = fetch_raw_logs()

    for raw in raw_logs:
        normalized = normalize_log(raw)
        store_normalized(normalized)

    print(f"Normalized {len(raw_logs)} logs.")


if __name__ == "__main__":
    run()
