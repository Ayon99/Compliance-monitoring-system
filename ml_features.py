from collections import defaultdict

def extract_features(logs):
    user_activity = defaultdict(lambda: {
        "failed_logins": 0,
        "api_calls": 0,
    })

    for log in logs:
        user = log["user_id"]
        message = log["message"].lower()

        user_activity[user]["api_calls"] += 1

        if "invalid" in message or "failed" in message:
            user_activity[user]["failed_logins"] += 1

    features = []

    for user, data in user_activity.items():
        features.append([
            data["failed_logins"],
            data["api_calls"]
        ])

    return features