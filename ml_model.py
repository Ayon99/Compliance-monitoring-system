from sklearn.ensemble import IsolationForest

model = IsolationForest(contamination=0.2, random_state=42)

def train_model(features):
    model.fit(features)

def predict_anomalies(features):
    preds = model.predict(features)
    scores = model.decision_function(features)

    results = []

    for i in range(len(features)):
        results.append({
            "features": features[i],
            "anomaly": True if preds[i] == -1 else False,
            "score": scores[i]
        })

    return results