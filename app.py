import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Predictive Maintenance AI",
    page_icon="🏭",
    layout="wide"
)

st.title("🏭 Predictive Maintenance Intelligence")
st.caption("6G-Integrated Smart Manufacturing System")


@st.cache_data
def load_results():
    return pd.read_csv(
        "data/processed/analyzed_data.csv",
        parse_dates=["Datetime"]
    )


df = load_results()

st.sidebar.header("Filters")

machines = sorted(df["Machine_ID"].unique())
selected_machine = st.sidebar.selectbox(
    "Machine ID", ["All"] + machines
)

modes = sorted(df["Operation_Mode"].dropna().unique())
selected_mode = st.sidebar.selectbox(
    "Operation Mode", ["All"] + modes
)

days = st.sidebar.selectbox(
    "Time Window",
    [1, 7, 30, 60, 90],
    index=2,
    format_func=lambda x: f"Last {x} days"
)

cutoff = df["Datetime"].max() - pd.Timedelta(days=days)
df = df[df["Datetime"] >= cutoff]

if selected_machine != "All":
    df = df[df["Machine_ID"] == selected_machine]

if selected_mode != "All":
    df = df[df["Operation_Mode"] == selected_mode]
st.subheader("Maintenance Risk Distribution")
st.bar_chart(df["Maintenance_Risk"].value_counts())

st.subheader("Machine Sensor Trends")

sensor = st.selectbox(
    "Choose sensor",
    [
        "Temperature_C",
        "Vibration_Hz",
        "Power_Consumption_kW",
        "Error_Rate_%"
    ]
)

chart_df = df.sort_values("Datetime")

if selected_machine == "All":
    chart_df = chart_df.groupby(
        "Datetime", as_index=False
    )[sensor].mean()

chart_df = chart_df.tail(2000)

st.line_chart(chart_df.set_index("Datetime")[sensor])

st.subheader("Recent Anomaly Records")

st.dataframe(
    df[df["Is_Anomaly"]][
        [
            "Datetime",
            "Machine_ID",
            "Operation_Mode",
            "Anomaly_Score",
            "Maintenance_Risk"
        ]
    ].sort_values(
        "Anomaly_Score", ascending=False
    ).head(100),
    use_container_width=True
)

st.subheader("🚨 Machine Maintenance Alerts")

high_risk = df[df["Maintenance_Risk"] == "High"]

if high_risk.empty:
    st.success("No high-risk records found.")
else:
    alerts = (
        high_risk.groupby("Machine_ID")
        .agg(
            High_Risk_Events=("Machine_ID", "size"),
            Latest_Anomaly=("Datetime", "max"),
            Average_Score=("Anomaly_Score", "mean")
        )
        .sort_values("High_Risk_Events", ascending=False)
        .reset_index()
    )

    st.dataframe(alerts.head(10), use_container_width=True)

    st.caption(
        "Prioritize inspection using repeated high-risk events. "
        "These are anomaly-based alerts, not confirmed machine failures."
    )

    st.subheader("🏭 Top 10 Machines Requiring Inspection")

report = pd.read_csv(
    "data/processed/machine_maintenance_report.csv"
)

st.dataframe(
    report.head(10),
    use_container_width=True,
    hide_index=True
)

st.download_button(
    "Download Maintenance Report",
    data=report.to_csv(index=False),
    file_name="machine_maintenance_report.csv",
    mime="text/csv"
)
st.subheader("📈 Risk Escalation Timeline")

timeline_df = pd.read_csv(
    "data/processed/analyzed_data.csv",
    parse_dates=["Datetime"]
)

machine_id = st.selectbox(
    "Select machine for timeline",
    sorted(timeline_df["Machine_ID"].unique()),
    key="timeline_machine"
)

timeline_df = (
    timeline_df[timeline_df["Machine_ID"] == machine_id]
    .sort_values("Datetime")
    .tail(500)
    .copy()
)

timeline_df["Rolling_Risk"] = (
    timeline_df["Anomaly_Score"]
    .rolling(window=20, min_periods=1)
    .mean()
)

st.line_chart(
    timeline_df.set_index("Datetime")[
        ["Anomaly_Score", "Rolling_Risk"]
    ]
)

st.caption(
    "Rolling average smooths short-term fluctuations. "
    "Increasing scores indicate unusual behavior, not confirmed future failure."
)