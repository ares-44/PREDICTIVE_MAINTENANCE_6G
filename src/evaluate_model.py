import pandas as pd
from sklearn.metrics import silhouette_score

from src.preprocessing import load_data
from src.feature_engineering import engineer_features
from src.anomaly_detection import FEATURES
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

df = engineer_features(load_data())
X = df[FEATURES].replace([float("inf"), float("-inf")], 0).fillna(0)

X = StandardScaler().fit_transform(X)

model = IsolationForest(
    n_estimators=100,
    contamination=0.05,
    random_state=42,
    n_jobs=-1
)

predictions = model.fit_predict(X)

print("Records:", len(df))
print("Anomalies:", (predictions == -1).sum())
print("Anomaly rate:", round((predictions == -1).mean() * 100, 2), "%")
print("Silhouette score (sample):",
      round(silhouette_score(X[:2000], predictions[:2000]), 4))