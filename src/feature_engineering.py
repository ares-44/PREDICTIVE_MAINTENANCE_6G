import pandas as pd

SENSOR_COLUMNS = [
    "Temperature_C",
    "Vibration_Hz",
    "Power_Consumption_kW",
    "Network_Latency_ms",
    "Packet_Loss_%",
    "Quality_Control_Defect_Rate_%",
    "Production_Speed_units_per_hr",
    "Error_Rate_%"
]


def engineer_features(df):
    df = df.copy()
    df = df.sort_values(["Machine_ID", "Datetime"])

    grouped = df.groupby("Machine_ID")

    for col in SENSOR_COLUMNS:
        baseline = grouped[col].transform(
            lambda s: s.rolling(20, min_periods=5).mean()
        )
        deviation = grouped[col].transform(
            lambda s: s.rolling(20, min_periods=5).std()
        )

        df[f"{col}_deviation"] = (
            (df[col] - baseline) / deviation.replace(0, float("nan"))
        ).fillna(0)

    df["Error_Rate_trend"] = grouped["Error_Rate_%"].diff().fillna(0)
    df["Vibration_Power_Ratio"] = (
        df["Vibration_Hz"] / df["Power_Consumption_kW"].replace(0, float("nan"))
    ).fillna(0)

    return df