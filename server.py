from fastapi import FastAPI
from datetime import datetime
from typing import List
import psycopg2
from pydantic import BaseModel
from auth import create_token, USERS, require_admin
from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm




api = FastAPI()

conn = psycopg2.connect(
    dbname="compliance_db",
    user="postgres",
    password="2006",
    host="localhost",
    port="5432"
)

conn.autocommit = True

@api.get("/health")
def health():
    return {"status": "ok"}


class LogIngestPayload(BaseModel):
    service: str
    level: str
    message: str
    user_id: str

logs_store: List[dict] = []

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
    cursor.close()

    return {
        "status": "accepted"
    }

@api.get("/logs")
def get_logs():
    return {
        "count": len(logs_store),
        "logs": logs_store
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

    return rows
