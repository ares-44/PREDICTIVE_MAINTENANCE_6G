import pandas as pd


def assign_risk(df):
    df = df.copy()

    df["Maintenance_Risk"] = "Low"

    anomaly_scores = df.loc[df["Is_Anomaly"], "Anomaly_Score"]

    if not anomaly_scores.empty:
        threshold = anomaly_scores.quantile(0.60)

        df.loc[
            df["Is_Anomaly"] & (df["Anomaly_Score"] < threshold),
            "Maintenance_Risk"
        ] = "Medium"

        df.loc[
            df["Is_Anomaly"] & (df["Anomaly_Score"] >= threshold),
            "Maintenance_Risk"
        ] = "High"

    return df