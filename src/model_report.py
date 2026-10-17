import pandas as pd
from pathlib import Path

df = pd.read_csv("data/processed/analyzed_data.csv")

report = {
    "Total records": len(df),
    "Machines": df["Machine_ID"].nunique(),
    "Anomalies": int(df["Is_Anomaly"].sum()),
    "Anomaly rate (%)": round(df["Is_Anomaly"].mean() * 100, 2),
    "Low-risk records": int((df["Maintenance_Risk"] == "Low").sum()),
    "Medium-risk records": int((df["Maintenance_Risk"] == "Medium").sum()),
    "High-risk records": int((df["Maintenance_Risk"] == "High").sum()),
}

print("\nMODEL EVALUATION SUMMARY")
print("-" * 35)

for key, value in report.items():
    print(f"{key}: {value}")

Path("reports").mkdir(exist_ok=True)

pd.DataFrame(
    report.items(), columns=["Metric", "Value"]
).to_csv("reports/model_evaluation.csv", index=False)

print("\nSaved: reports/model_evaluation.csv")