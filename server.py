from fastapi import FastAPI
from datetime import datetime
from typing import List
import psycopg2
from pydantic import BaseModel
from auth import create_token, USERS, require_admin
from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from ml_features import extract_features
from ml_model import train_model, predict_anomalies


api = FastAPI()

api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

conn = psycopg2.connect(
    dbname="compliance_db",
    user="postgres",
    password="2006",
    host="localhost",
    port="5432"
)

conn.autocommit = True

def get_all_logs():
    cursor = conn.cursor()
    cursor.execute("SELECT service, level, message, user_id FROM raw_logs")
    rows = cursor.fetchall()
    cursor.close()

    logs = []
    for r in rows:
        logs.append({
            "service": r[0],
            "level": r[1],
            "message": r[2],
            "user_id": r[3],
        })

    return logs

def run_ml_detection():
    logs = get_all_logs()

    if len(logs) < 5:
        return

    features = extract_features(logs)
    train_model(features)
    results = predict_anomalies(features)

    users = [log["user_id"] for log in logs]

    cursor = conn.cursor()

    for i, res in enumerate(results):
        if res["anomaly"] and res["score"] < -0.1:

            cursor.execute("""
                SELECT 1 FROM violations
                WHERE user_id = %s
                AND rule_name = 'ml_anomaly'
                ORDER BY detected_at DESC
                LIMIT 1
            """, (users[i],))

            exists = cursor.fetchone()

            if not exists:
                cursor.execute(
                    """
                    INSERT INTO violations (rule_name, user_id, details, detected_at)
                    VALUES (%s, %s, %s, NOW())
                    """,
                    (
                        "ml_anomaly",
                        users[i],
                        f"Anomalous behavior detected. Score: {res['score']}"
                    )
                )

    cursor.close()

@api.get("/health")
def health():
    return {"status": "ok"}


class LogIngestPayload(BaseModel):
    service: str
    level: str
    message: str
    user_id: str



@api.post("/ingest-log")
def ingest_log(payload: LogIngestPayload):

    log_entry = {
        "service": payload.service,
        "level": payload.level,
        "message": payload.message,
        "user_id": payload.user_id,
        "ingested_at": datetime.utcnow()
    }

    cursor = conn.cursor()

    # Store raw log
    cursor.execute(
        """
        INSERT INTO raw_logs (service, level, message, user_id, ingested_at)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (
            log_entry["service"],
            log_entry["level"],
            log_entry["message"],
            log_entry["user_id"],
            log_entry["ingested_at"]
        )
    )

    # RULE ENGINE (detect violations)
    if log_entry["level"] == "ERROR":
        cursor.execute(
            """
            INSERT INTO violations (rule_name, user_id, details, detected_at)
            VALUES (%s, %s, %s, %s)
            """,
            (
                "Error Log Detected",
                log_entry["user_id"],
                log_entry["message"],
                datetime.utcnow()
            )
        )

    cursor.close()

    run_ml_detection()

    return {
        "status": "accepted"
    }

@api.get("/logs")
def get_logs():
    cursor = conn.cursor()

    cursor.execute("""
        SELECT service, level, message, user_id, ingested_at
        FROM raw_logs
        ORDER BY ingested_at DESC
    """)

    rows = cursor.fetchall()
    cursor.close()

    logs = []
    for row in rows:
        logs.append({
            "service": row[0],
            "level": row[1],
            "message": row[2],
            "user_id": row[3],
            "time": str(row[4])
        })

    return {
        "logs": logs
    }

@api.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = USERS.get(form_data.username)

    if not user or user["password"] != form_data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token({
        "sub": form_data.username,
        "role": user["role"]
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@api.get("/violations")
def get_violations(admin=Depends(require_admin)):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT rule_name, user_id, details, detected_at
        FROM violations
        ORDER BY detected_at DESC
    """)
    rows = cursor.fetchall()
    cursor.close()

    return [
    {
        "rule": row[0],
        "user": row[1],
        "details": row[2],
        "time": str(row[3])
    }
    for row in rows
]
