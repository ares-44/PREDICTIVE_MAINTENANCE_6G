from src.preprocessing import load_data
from src.feature_engineering import engineer_features
from src.anomaly_detection import train_model
from src.risk_engine import assign_risk

df = engineer_features(load_data())
df = train_model(df)
df = assign_risk(df)

df.to_csv("data/processed/analyzed_data.csv", index=False)
print("Analysis saved successfully!")