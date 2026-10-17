import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import joblib
from pathlib import Path

FEATURES = [
    "Temperature_C_deviation",
    "Vibration_Hz_deviation",
    "Power_Consumption_kW_deviation",
    "Network_Latency_ms_deviation",
    "Packet_Loss_%_deviation",
    "Quality_Control_Defect_Rate_%_deviation",
    "Production_Speed_units_per_hr_deviation",
    "Error_Rate_%_deviation",
    "Error_Rate_trend",
    "Vibration_Power_Ratio",
]


def train_model(df):
    X = df[FEATURES].replace([float("inf"), float("-inf")], 0).fillna(0)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = IsolationForest(
        n_estimators=100,
        contamination=0.05,
        random_state=42,
        n_jobs=-1,
    )
    model.fit(X_scaled)

    # Higher score means more anomalous
    df = df.copy()
    df["Anomaly_Score"] = -model.decision_function(X_scaled)
    df["Is_Anomaly"] = model.predict(X_scaled) == -1

    Path("models").mkdir(exist_ok=True)
    joblib.dump(model, "models/isolation_forest.pkl")
    joblib.dump(scaler, "models/scaler.pkl")

    return df


if __name__ == "__main__":
    from src.preprocessing import load_data
    from src.feature_engineering import engineer_features

    df = engineer_features(load_data())
    result = train_model(df)

    print("Model trained successfully!")
    print("Total records:", len(result))
    print("Anomalies:", int(result["Is_Anomaly"].sum()))
    print("Anomaly percentage:", round(result["Is_Anomaly"].mean() * 100, 2), "%")
    print("\nMachine anomaly counts:")
    print(result.groupby("Machine_ID")["Is_Anomaly"].sum().sort_values(ascending=False).head(10))