from fastapi import FastAPI, BackgroundTasks
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
from fastapi.responses import Response
import threading
import time

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
    """Fetch all logs with timestamps"""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT service, level, message, user_id, ingested_at 
        FROM raw_logs
        ORDER BY ingested_at DESC
        LIMIT 10000
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

def run_ml_detection():
    """Run ML anomaly detection with detailed logging"""
    print("\n" + "="*60)
    print("🤖 Running ML detection...")
    print("="*60)
    
    logs = get_all_logs()
    print(f"📊 Total logs retrieved: {len(logs)}")

    if len(logs) < 20:
        print("⚠️ Not enough logs for ML (need at least 20)")
        return

    features, users = extract_features(logs, window_minutes=5)
    
    print(f"👥 Active users found: {len(users)}")
    if len(users) > 0:
        print(f"   Users: {users}")
    
    if len(features) < 3:
        print("⚠️ Not enough active users for ML (need at least 3)")
        return
    
    # Show what each user is doing
    print("\n📈 User Activity:")
    for i, (user, feat) in enumerate(zip(users, features)):
        print(f"   {user}:")
        print(f"      - Log rate: {feat[0]:.2f}/min")
        print(f"      - Errors: {feat[1]}")
        print(f"      - Failed auth: {feat[3]}")
        print(f"      - Burst score: {feat[6]}")
        print(f"      - Risk score: {feat[8]}")

    success = train_model(features)
    
    if not success:
        print("⚠️ Model training failed")
        return
    
    print("\n🔍 Running anomaly detection...")
    results = predict_anomalies(features, threshold=-0.6)
    
    # Show ALL scores
    print("\n📊 Anomaly Scores:")
    for i, res in enumerate(results):
        status = "🚨 ANOMALY" if res["anomaly"] else "✅ Normal"
        print(f"   {users[i]}: {res['score']:.3f} {status}")

    cursor = conn.cursor()
    anomaly_count = 0

    for i, res in enumerate(results):
        if res["anomaly"]:
            anomaly_count += 1
            
            cursor.execute("""
                SELECT 1 FROM violations
                WHERE user_id = %s
                AND rule_name = 'ml_anomaly'
                AND detected_at > NOW() - INTERVAL '5 minutes'
                LIMIT 1
            """, (users[i],))

            exists = cursor.fetchone()

            if not exists:
                print(f"\n💾 INSERTING ML Anomaly: {users[i]} (score: {res['score']:.3f})")
                
                cursor.execute(
                    """
                    INSERT INTO violations (rule_name, user_id, details, detected_at)
                    VALUES (%s, %s, %s, NOW())
                    """,
                    (
                        "ml_anomaly",
                        users[i],
                        f"Anomalous behavior detected. Score: {res['score']:.3f}"
                    )
                )
            else:
                print(f"⏭️ Skipping {users[i]} - already flagged in last 5 min")

    cursor.close()
    print(f"\n✅ ML detection complete. Inserted {anomaly_count} new anomalies")
    print("="*60 + "\n")

# Background thread for periodic ML detection
def ml_detection_loop():
    """Run ML detection every 60 seconds"""
    while True:
        try:
            run_ml_detection()
        except Exception as e:
            print(f"❌ ML detection error: {e}")
            import traceback
            traceback.print_exc()
        
        time.sleep(60)  # Run every 60 seconds

# Start background thread
ml_thread = threading.Thread(target=ml_detection_loop, daemon=True)
ml_thread.start()

@api.on_event("startup")
async def startup_event():
    """Run ML detection 10 seconds after startup"""
    print("🚀 Server started, waiting 10 seconds before first ML run...")
    time.sleep(10)
    run_ml_detection()

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
    """Ingest log - NO ML DETECTION HERE"""
    
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

    return {"status": "accepted"}

@api.get("/logs")
def get_logs():
    cursor = conn.cursor()

    cursor.execute("""
        SELECT service, level, message, user_id, ingested_at
        FROM raw_logs
        ORDER BY ingested_at DESC
        LIMIT 1000
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

    return {"logs": logs}

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
        LIMIT 1000
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

@api.get("/report")
def get_report(admin=Depends(require_admin)):
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM violations")
    total = cursor.fetchone()[0]

    cursor.execute("""
        SELECT rule_name, COUNT(*)
        FROM violations
        GROUP BY rule_name
    """)
    breakdown_rows = cursor.fetchall()

    breakdown = [
        {"rule": row[0], "count": row[1]}
        for row in breakdown_rows
    ]

    cursor.close()

    return {
        "total_violations": total,
        "breakdown": breakdown
    }

@api.get("/report/download")
def download_report(admin=Depends(require_admin)):
    cursor = conn.cursor()

    cursor.execute("""
        SELECT rule_name, user_id, details, detected_at
        FROM violations
        ORDER BY detected_at DESC
    """)

    rows = cursor.fetchall()
    cursor.close()

    report_text = "Compliance Report\n\n"

    for r in rows:
        report_text += f"""
Rule: {r[0]}
User: {r[1]}
Details: {r[2]}
Time: {r[3]}
-------------------------
"""

    return Response(
        content=report_text,
        media_type="text/plain",
        headers={"Content-Disposition": "attachment; filename=report.txt"}
    )

@api.post("/trigger-ml")
def trigger_ml(admin=Depends(require_admin)):
    """Manually trigger ML detection (for testing)"""
    run_ml_detection()
    return {"status": "ML detection triggered"}