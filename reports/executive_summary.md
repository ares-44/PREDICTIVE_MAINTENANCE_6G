\# Executive Summary

\## Predictive Maintenance in 6G-Integrated Smart Manufacturing



\### Objective

Develop an AI-based system to detect unusual machine behavior and prioritize maintenance inspections.



\### Dataset

\- 99,972 records

\- 50 machines

\- 14 original data columns

\- Data period: January–March 2025



\### Methodology

\- Sensor data preprocessing and temporal feature engineering

\- Isolation Forest anomaly detection

\- Anomaly-based maintenance risk classification

\- Streamlit dashboard for monitoring and inspection prioritization



\### Results

\- Anomalies detected: 4,999 (5.00%)

\- Low-risk records: 94,973

\- Medium-risk records: 2,999

\- High-risk records: 2,000



\### Limitations

The dataset does not contain verified machine-failure outcomes. Therefore, the system identifies unusual behavior and relative inspection priorities, not confirmed future failures or remaining useful life.



\### Recommendations

\- Investigate machines with repeated high-risk events.

\- Review sensor trends and operating conditions before maintenance decisions.

\- Collect verified failure and maintenance logs for future model validation.

\- Evaluate false alarms and detection lead time when labeled events become available.



\### Conclusion

The prototype demonstrates an AI-driven approach to industrial anomaly monitoring. Real-world deployment requires validation with operational data and testing on actual industrial communication infrastructure.

