import requests
import random
import time
from datetime import datetime, timedelta

URL = "http://127.0.0.1:8000/ingest-log"

services = ["auth-service", "api-gateway", "data-service", "admin-panel", "export-service"]
normal_users = ["alice", "bob", "charlie", "diana", "edward"]
compliance_officer = "compliance_bot"

def send_log(service, level, message, user, metadata=""):
    payload = {
        "service": service,
        "level": level,
        "message": f"{message} {metadata}".strip(),
        "user_id": user
    }
    
    try:
        requests.post(URL, json=payload, timeout=2)
    except:
        pass

def normal_activity():
    """Regular business operations"""
    user = random.choice(normal_users)
    service = random.choice(services[:3])  # Normal services only
    
    send_log(
        service=service,
        level=random.choice(["INFO"] * 8 + ["WARNING"]),  # Mostly INFO
        message=random.choice([
            "User logged in successfully",
            "API request processed",
            "Data query executed",
            "Session validated",
            "Cache hit"
        ]),
        user=user
    )

def failed_login_attack():
    """Brute force login attempt - COMPLIANCE VIOLATION"""
    print("🚨 COMPLIANCE VIOLATION: Brute force attack detected")
    
    attacker = random.choice(["attacker1", "suspicious_user", "bot_123"])
    
    for _ in range(15):  # Rapid failed logins
        send_log(
            service="auth-service",
            level="ERROR",
            message="Authentication failed - Invalid credentials",
            user=attacker,
            metadata=f"IP: 203.0.113.{random.randint(1, 255)}"
        )
        time.sleep(0.1)

def data_exfiltration():
    """Unusual bulk data download - COMPLIANCE VIOLATION"""
    print("🚨 COMPLIANCE VIOLATION: Data exfiltration attempt")
    
    insider = random.choice(normal_users)
    
    for _ in range(20):  # Bulk downloads
        send_log(
            service="export-service",
            level="WARNING",
            message="Large dataset exported",
            user=insider,
            metadata=f"Records: {random.randint(5000, 50000)}"
        )
        time.sleep(0.05)

def privilege_escalation():
    """Unauthorized admin access - COMPLIANCE VIOLATION"""
    print("🚨 COMPLIANCE VIOLATION: Privilege escalation detected")
    
    user = random.choice(normal_users)
    
    for _ in range(8):
        send_log(
            service="admin-panel",
            level="ERROR",
            message="Unauthorized admin action attempted",
            user=user,
            metadata=f"Action: {random.choice(['user_delete', 'role_modify', 'config_change'])}"
        )
        time.sleep(0.2)

def after_hours_access():
    """Access during non-business hours - COMPLIANCE VIOLATION"""
    print("🚨 COMPLIANCE VIOLATION: After-hours access")
    
    user = random.choice(normal_users)
    
    for _ in range(12):
        send_log(
            service="data-service",
            level="WARNING",
            message="Data access outside business hours",
            user=user,
            metadata=f"Time: {datetime.now().strftime('%H:%M:%S')}"
        )
        time.sleep(0.15)

def api_abuse():
    """Rate limit violation - COMPLIANCE VIOLATION"""
    print("🚨 COMPLIANCE VIOLATION: API rate limit exceeded")
    
    abuser = random.choice(normal_users + ["script_bot", "api_scraper"])
    
    for _ in range(25):  # Rapid API calls
        send_log(
            service="api-gateway",
            level="WARNING",
            message="Rate limit exceeded",
            user=abuser,
            metadata=f"Endpoint: /api/v1/{random.choice(['users', 'data', 'reports'])}"
        )
        time.sleep(0.05)

# Compliance monitoring heartbeat
def compliance_heartbeat():
    send_log(
        service="compliance-monitor",
        level="INFO",
        message="Compliance check completed",
        user=compliance_officer
    )

print("🚀 Starting Compliance Monitoring Simulator")
print("=" * 50)

iteration = 0

while True:
    iteration += 1
    print(f"\n📊 Iteration {iteration} - {datetime.now().strftime('%H:%M:%S')}")
    
    # 🟢 Normal traffic (80% of activity)
    for _ in range(random.randint(8, 15)):
        normal_activity()
    
    # 🔴 Compliance violations (periodic, realistic)
    
    if random.random() < 0.15:  # 15% chance
        failed_login_attack()
    
    if random.random() < 0.10:  # 10% chance
        data_exfiltration()
    
    if random.random() < 0.08:  # 8% chance
        privilege_escalation()
    
    if random.random() < 0.12:  # 12% chance
        after_hours_access()
    
    if random.random() < 0.10:  # 10% chance
        api_abuse()
    
    # Compliance heartbeat
    if iteration % 5 == 0:
        compliance_heartbeat()
    
    print(f"✅ Batch sent ({datetime.now().strftime('%H:%M:%S')})")
    time.sleep(3)  # Wait 3 seconds between batches