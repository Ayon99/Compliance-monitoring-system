from sklearn.ensemble import IsolationForest
import numpy as np

# Increase contamination - expect more anomalies
model = IsolationForest(
    contamination=0.2,  # ← Back to 20% (was 0.15)
    random_state=42,
    n_estimators=100,
    max_samples=256  # ← Add this for better sensitivity
)

def train_model(features):
    """Train the model on feature data"""
    if len(features) < 5:
        return False
    model.fit(features)
    return True

def predict_anomalies(features, threshold=0.0):  # ← Change to 0.0 (catch anything negative)
    """
    Predict anomalies with score threshold
    """
    if len(features) == 0:
        return []
    
    preds = model.predict(features)
    scores = model.decision_function(features)
    
    results = []
    
    for i in range(len(features)):
        # Flag if isolation forest says anomaly OR score is negative
        is_anomaly = (preds[i] == -1) or (scores[i] < threshold)
        
        results.append({
            "features": features[i],
            "anomaly": is_anomaly,
            "score": float(scores[i])
        })
    
    return results