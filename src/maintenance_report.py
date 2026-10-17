import pandas as pd

df = pd.read_csv("data/processed/analyzed_data.csv")
df["Datetime"] = pd.to_datetime(df["Datetime"])

report = (
    df.groupby("Machine_ID")
    .agg(
        Total_Readings=("Machine_ID", "size"),
        Anomalies=("Is_Anomaly", "sum"),
        High_Risk_Events=(
            "Maintenance_Risk",
            lambda s: (s == "High").sum()
        ),
        Avg_Temperature=("Temperature_C", "mean"),
        Avg_Vibration=("Vibration_Hz", "mean"),
        Avg_Error_Rate=("Error_Rate_%", "mean"),
        Last_Reading=("Datetime", "max")
    )
    .reset_index()
)

report["Anomaly_Rate_%"] = (
    report["Anomalies"] / report["Total_Readings"] * 100
).round(2)

report = report.sort_values(
    ["High_Risk_Events", "Anomaly_Rate_%"],
    ascending=False
)

report.to_csv(
    "data/processed/machine_maintenance_report.csv",
    index=False
)

print("Maintenance report generated!")
print("\nTop 10 machines to inspect:")
print(report.head(10).to_string(index=False))
print("\nSaved: data/processed/machine_maintenance_report.csv")