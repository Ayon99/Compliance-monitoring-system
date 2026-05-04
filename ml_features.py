from collections import defaultdict
from datetime import datetime, timedelta
import re

def extract_features(logs, window_minutes=10):
    """
    Extract compliance-focused behavioral features
    """
    now = datetime.utcnow()
    cutoff = now - timedelta(minutes=window_minutes)
    
    # Filter recent logs
    recent_logs = [
        log for log in logs 
        if datetime.fromisoformat(str(log.get("ingested_at", now))) > cutoff
    ]
    
    if len(recent_logs) < 15:
        return [], []
    
    user_data = defaultdict(lambda: {
        "total": 0,
        "error_count": 0,
        "warning_count": 0,
        "services": set(),
        "timestamps": [],
        "failed_auth": 0,
        "admin_attempts": 0,
        "export_count": 0,
        "api_calls": 0,
        "unique_ips": set()
    })
    
    for log in recent_logs:
        u = log["user_id"]
        msg = log["message"].lower()
        
        user_data[u]["total"] += 1
        
        if log["level"] == "ERROR":
            user_data[u]["error_count"] += 1
        elif log["level"] == "WARNING":
            user_data[u]["warning_count"] += 1
        
        user_data[u]["services"].add(log["service"])
        
        if "ingested_at" in log:
            user_data[u]["timestamps"].append(log["ingested_at"])
        
        # Compliance-specific patterns
        if "authentication failed" in msg or "invalid credentials" in msg:
            user_data[u]["failed_auth"] += 1
        
        if "admin" in msg or "unauthorized" in msg:
            user_data[u]["admin_attempts"] += 1
        
        if "export" in msg or "download" in msg:
            user_data[u]["export_count"] += 1
        
        if "api" in log["service"]:
            user_data[u]["api_calls"] += 1
        
        # Extract IPs from metadata
        ip_match = re.search(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', msg)
        if ip_match:
            user_data[u]["unique_ips"].add(ip_match.group())
    
    features = []
    users = []
    
    for user, data in user_data.items():
        # Skip system users and low activity
        if user in ["system", "compliance_bot", "health_check"] or data["total"] < 3:
            continue
        
        # Calculate rates
        log_rate = data["total"] / window_minutes
        error_ratio = data["error_count"] / data["total"] if data["total"] > 0 else 0
        
        # Burst detection (max logs in 1-minute window)
        burst_score = 0
        if len(data["timestamps"]) >= 5:
            timestamps = sorted(data["timestamps"])
            for i in range(len(timestamps) - 4):
                window_start = timestamps[i]
                window_end = window_start + timedelta(minutes=1)
                logs_in_window = sum(1 for ts in timestamps[i:] if ts <= window_end)
                burst_score = max(burst_score, logs_in_window)
        
        # Compliance risk score
        compliance_risk = (
            data["failed_auth"] * 3 +
            data["admin_attempts"] * 5 +
            data["export_count"] * 2
        )
        
        features.append([
            log_rate,                    # Overall activity rate
            data["error_count"],         # Total errors
            error_ratio,                 # Error percentage
            data["failed_auth"],         # Failed login attempts
            data["admin_attempts"],      # Unauthorized admin actions
            data["export_count"],        # Data export activity
            burst_score,                 # Max logs per minute
            len(data["services"]),       # Service diversity
            compliance_risk,             # Weighted risk score
            len(data["unique_ips"])      # IP diversity (multi-location access)
        ])
        users.append(user)
    
    return features, users