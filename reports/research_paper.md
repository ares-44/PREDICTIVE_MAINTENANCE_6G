Predictive Maintenance and Anomaly Detection in 6G-Integrated Smart Manufacturing Systems
Project Research Paper — Internship Submission
Abstract
Unexpected machine behavior can disrupt manufacturing operations, increase maintenance costs, and reduce production efficiency. This paper presents an AI-based anomaly detection and maintenance prioritization system designed for smart manufacturing environments. The proposed prototype combines industrial sensor preprocessing, temporal feature engineering, Isolation Forest anomaly detection, relative-risk classification, and an interactive Streamlit dashboard.
The system was evaluated on a manufacturing dataset containing 100,000 original records and 14 columns. After removing duplicate machine-timestamp records, 99,972 records representing 50 machines remained. With the Isolation Forest contamination parameter set to 0.05, the model identified 4,999 records as anomalous. A preliminary evaluation produced a silhouette score of 0.2092 on a sample of 2,000 records; this score does not establish anomaly-detection accuracy. The system also generates machine-level inspection rankings and visualizes historical anomaly scores.
The results demonstrate a working anomaly monitoring prototype. However, verified machine-failure labels and real 6G infrastructure measurements were not available for validating future-failure prediction, maintenance lead time, or actual 6G performance. These limitations define important directions for future research.
Keywords: Predictive Maintenance, Anomaly Detection, Isolation Forest, Smart Manufacturing, Industrial AI, Sensor Analytics, 6G Networks.
1. Introduction
Modern manufacturing systems use sensors and connected equipment to monitor machine operating conditions. These sensors generate information about temperature, vibration, electrical power consumption, production speed, network performance, and operational errors. Changes in these measurements can provide useful signals for investigating abnormal machine behavior.
Traditional maintenance approaches may rely on fixed thresholds or respond only after a machine has degraded or failed. Such approaches may not adequately capture relationships between multiple sensor variables or differences in machine operating conditions.
Machine learning provides techniques for identifying unusual observations in multidimensional datasets. Anomaly detection is particularly useful when verified failure examples are unavailable or rare. However, identifying unusual behavior is not equivalent to predicting a confirmed future failure.
This project develops a prototype for anomaly monitoring and maintenance inspection prioritization. It combines data preprocessing, feature engineering, Isolation Forest, anomaly-based risk classification, machine-level reporting, and a web-based dashboard.
The system is designed around a smart manufacturing use case in which low-latency industrial connectivity could support timely data collection and monitoring. The implementation does not claim to have experimentally tested a real 6G network.
2. Objectives
The objectives of this project are:
Analyze industrial sensor data from multiple machines.
Prepare timestamped data for machine-level analysis.
Engineer features representing sensor deviations and changes in operating behavior.
Detect unusual observations using Isolation Forest.
Assign relative maintenance risk categories to records.
Rank machines for further inspection using historical anomaly events.
Visualize sensor trends, anomaly scores, and maintenance alerts through Streamlit.
Identify the additional data and experiments required for validated failure prediction.
3. Dataset Description
The dataset used in this project is Thales_Group_Manufacturing.csv. It contains 100,000 original records and 14 columns. After duplicate machine-timestamp records were removed, 99,972 records remained.
The observations cover the period from January 1, 2025, to March 10, 2025, and represent 50 machine identifiers.
3.1 Dataset variables
The dataset includes the following variables:
Date and Timestamp: recording date and time.
Machine_ID: machine identifier.
Operation_Mode: Active, Idle, or Maintenance.
Temperature_C: operating temperature.
Vibration_Hz: vibration measurement.
Power_Consumption_kW: electrical power consumption.
Network_Latency_ms: network latency.
Packet_Loss_%: percentage of lost packets.
Quality_Control_Defect_Rate_%: quality-control defect rate.
Production_Speed_units_per_hr: production speed.
Predictive_Maintenance_Score: an existing maintenance-related score.
Error_Rate_%: operational error rate.
Efficiency_Status: categorical efficiency label.
3.2 Data quality
Initial inspection reported no missing values in the original dataset. Date and time were combined into a datetime field for temporal analysis.
Duplicate machine-timestamp records were removed during preprocessing, reducing the dataset from 100,000 to 99,972 rows.
The dataset does not provide verified failure-event labels or documented remaining-useful-life targets. Consequently, supervised failure-prediction metrics cannot be calculated reliably from the available information.
4. Exploratory Data Analysis
Exploratory data analysis was conducted using Pandas, Matplotlib, and Seaborn.
4.1 Operating-mode distribution
The processed dataset contains:
| Operating mode | Records |
|---|---:|
| Active | 70,036 |
| Idle | 20,050 |
| Maintenance | 9,886 |
| Total | 99,972 |
Active operation accounts for approximately 70.1% of the records, while Idle and Maintenance account for approximately 20.1% and 9.9%, respectively.
4.2 Efficiency-status distribution
| Efficiency status | Records |
|---|---:|
| Low | 77,804 |
| Medium | 19,182 |
| High | 2,986 |
| Total | 99,972 |
Low efficiency is the most frequent category in the supplied dataset. This distribution describes the recorded efficiency labels; it does not independently establish machine health or future failure probability.
4.3 Sensor statistics
Selected descriptive statistics are shown below.
| Sensor variable | Mean | Minimum | Maximum |
|---|---:|---:|---:|
| Temperature (°C) | 60.04 | 30.00 | 90.00 |
| Vibration (Hz) | 2.55 | 0.10 | 5.00 |
| Power consumption (kW) | 5.75 | 1.50 | 10.00 |
| Network latency (ms) | 25.56 | 1.00 | 50.00 |
| Packet loss (%) | 2.49 | 0.00 | 5.00 |
| Quality defect rate (%) | 5.01 | 0.00 | 10.00 |
| Production speed (units/hour) | 275.91 | 50.00 | 500.00 |
| Error rate (%) | 7.50 | 0.00 | 15.00 |
These statistics describe the supplied dataset. They should not be interpreted as universal operating limits for industrial machinery.
4.4 Visualizations
Three exploratory charts were generated:
Distribution of mean machine temperatures.
Correlation heatmap of numeric variables.
Efficiency-status distribution.
The charts are saved in the data/processed/ directory. Correlations may reveal associations between variables, but they do not establish causal relationships.
5. Proposed Methodology
The implementation consists of five main stages: preprocessing, feature engineering, anomaly detection, risk classification, and dashboard-based inspection prioritization.
5.1 Data preprocessing
The dataset is loaded using Pandas. Date and time fields are combined into a datetime variable, and records are sorted by machine identifier and timestamp.
Duplicate records sharing the same machine identifier and timestamp are removed. The resulting data is used for subsequent feature engineering and modeling.
5.2 Feature engineering
The prototype derives additional variables from the original sensor measurements.
Rolling sensor deviation: For each machine, rolling means and standard deviations are calculated using a 20-observation window. Standardized deviations are then computed to represent how far a measurement lies from its rolling baseline.
For a measurement x_t, rolling mean \μ_t, and rolling standard deviation \σ_t, the deviation feature is:
z_t=x_t-\μ_t) / (\σ_t)
]
When the rolling standard deviation is zero or unavailable, the current implementation substitutes zero for the resulting undefined value. This is a simplifying implementation choice and should be refined during further validation.
Error-rate trend: The difference between consecutive error-rate measurements for the same machine is calculated:
\Δ E_t=E_t-E_{t-1}
]
Vibration-to-power ratio: Vibration is divided by power consumption to introduce a feature representing their relative behavior. Zero denominators are handled to avoid invalid numerical values.
These engineered features are intended to help the anomaly detector identify unusual combinations of sensor behavior. Their usefulness must be evaluated empirically rather than assumed.
5.3 Isolation Forest
Isolation Forest was selected because it can identify unusual observations without requiring labeled failure examples.
The implementation uses the following configuration:
| Parameter | Value |
|---|---|
| Algorithm | Isolation Forest |
| Number of estimators | 100 |
| Contamination | 0.05 |
| Random seed | 42 |
| Parallel processing | Enabled |
The engineered features are standardized before model fitting. The contamination parameter specifies an expected outlier proportion for the model; it is not a measured failure rate.
The model generates a decision score for each observation. The sign is reversed in the implementation so that higher anomaly scores represent more unusual observations.
5.4 Maintenance risk classification
The prototype assigns three relative-risk categories:
Low: The observation was not flagged as an anomaly.
Medium: The observation was flagged as an anomaly but its anomaly score is below the 60th percentile of anomaly scores.
High: The observation was flagged as an anomaly and its anomaly score is at or above the 60th percentile of anomaly scores.
These categories support inspection prioritization. They are not calibrated probabilities of machine failure, and they do not establish the time remaining before a breakdown.
5.5 Machine-level inspection prioritization
The system groups records by machine and calculates the number of readings, detected anomalies, high-risk events, average temperature, average vibration, average error rate, and most recent observation.
Machines are ranked primarily by the number of high-risk events, with anomaly rate used as a secondary sorting criterion.
This approach highlights machines that may deserve further inspection. It does not prove that a machine is defective or will fail.
5.6 Streamlit dashboard
A Streamlit dashboard provides the following functions:
Summary metrics for records, anomalies, and high-risk events.
Machine selection.
Operation-mode and time-window filters.
Maintenance risk distribution.
Sensor trend visualization.
Recent anomaly records.
Machine-level maintenance alerts.
Top-ten inspection-priority table.
Downloadable maintenance report.
Historical anomaly-score timeline with a rolling average.
The dashboard loads saved model-analysis results from a processed CSV file rather than retraining the model on each application refresh.
6. Experimental Results
6.1 Anomaly detection results
The Isolation Forest model was configured with a contamination parameter of 0.05.
| Metric | Result |
|---|---:|
| Processed records | 99,972 |
| Machines represented | 50 |
| Detected anomalies | 4,999 |
| Detected anomaly rate | 5.00% |
The detected anomaly rate is consistent with the chosen contamination parameter. This consistency confirms the expected behavior of the configured detector, but it does not establish that every flagged observation is a genuine anomaly.
6.2 Risk classification results
The implemented risk engine produced the following distribution:
| Risk category | Records | Approximate proportion |
|---|---:|---:|
| Low | 94,973 | 95.00% |
| Medium | 2,999 | 3.00% |
| High | 2,000 | 2.00% |
| Total | 99,972 | 100.00% |
All Medium- and High-risk observations belong to the detected-anomaly group in the current implementation. The difference between the anomaly count and the combined Medium- and High-risk counts reflects the risk classification logic.
These proportions describe the prototype's output, not the actual distribution of machine-failure risk in a factory.
6.3 Preliminary silhouette score
An exploratory evaluation calculated a silhouette score of 0.2092 using a sample of 2,000 standardized feature vectors and the model's anomaly labels.
The silhouette score measures how well observations fit their assigned groups relative to other groups. A value of 0.2092 indicates modest separation under this particular representation and sample.
However, the silhouette score is not an anomaly-detection accuracy metric. Isolation Forest is not inherently a clustering algorithm, and its labels do not provide ground truth. This result must therefore be interpreted cautiously.
6.4 Machine-level results
The inspection-priority report ranked machines using high-risk event counts and anomaly rates.
The ten leading machines in the generated report were:
| Machine ID | Anomalies | High-risk events | Anomaly rate |
|---|---:|---:|---:|
| 9 | 114 | 49 | 5.73% |
| 2 | 115 | 49 | 5.63% |
| 3 | 117 | 48 | 5.85% |
| 17 | 104 | 48 | 5.05% |
| 1 | 104 | 47 | 5.43% |
| 36 | 112 | 47 | 5.37% |
| 26 | 101 | 47 | 4.91% |
| 32 | 109 | 46 | 5.37% |
| 44 | 110 | 46 | 5.36% |
| 45 | 91 | 46 | 4.38% |
These machines are candidates for further investigation based on the current scoring system. The rankings do not confirm that they have experienced failures.
6.5 Summary of implementation outcomes
The prototype successfully processes the dataset, generates engineered features, fits an Isolation Forest model, assigns relative-risk categories, produces machine-level reports, and displays the outputs through Streamlit.
No verified ground-truth evaluation was conducted because confirmed failure labels were unavailable.
7. Discussion
The implementation demonstrates how unsupervised anomaly detection can be combined with machine-level reporting and an interactive dashboard. Its main practical contribution is a unified workflow for examining unusual sensor observations and organizing machines for further inspection.
However, several considerations affect the interpretation of the results.
First, a configured contamination rate of 5% directly influences the number of observations identified as anomalous. The resulting anomaly count should not be presented as the observed rate of actual equipment faults.
Second, machine-level differences and operating modes may influence sensor behavior. A robust industrial implementation should account for the distinction between Active, Idle, and Maintenance operation and should evaluate whether the baseline appropriately reflects each mode.
Third, the current rolling features use observations within each machine's ordered history. In a future real-time implementation, the feature-generation process must be designed to use only information available at the time of prediction. Evaluation should use chronological splits to avoid overly optimistic estimates caused by temporal information leakage.
Fourth, machine rankings depend on how often a machine is observed. Event counts should be interpreted alongside anomaly rates, exposure duration, and the recency of observations.
Finally, network latency and packet loss are included as data features, but the project does not experimentally evaluate a 6G communication network. The current work is therefore a smart-manufacturing analytics prototype designed for a 6G-integrated use case rather than a validated 6G deployment.
8. Limitations and Future Work
8.1 Limitations
The main limitations are:
No verified machine-failure labels are available for supervised evaluation.
The contamination parameter influences the number of detected anomalies.
Risk categories are relative anomaly-based labels, not calibrated failure probabilities.
Actual early-warning lead time and prevented downtime have not been measured.
The silhouette score does not establish predictive accuracy.
The supplied data has not been demonstrated to originate from a deployed 6G network.
The current baseline and rolling-feature logic require further testing across operating modes and chronological data splits.
8.2 Future work
Future development should focus on:
Collecting verified failure, repair, and maintenance-event records.
Evaluating the model using precision, recall, F1-score, and false-alarm rate where ground-truth labels are available.
Comparing Isolation Forest with alternative anomaly-detection algorithms and suitable baseline methods.
Evaluating performance on held-out machines and later time periods.
Refining machine- and operation-mode-specific baseline models.
Improving explainability by identifying the sensor variables most responsible for each alert.
Testing the pipeline using simulated streaming data and measuring processing latency.
Integrating real industrial communication equipment before making claims about 6G network performance.
Measuring warning lead time and operational benefits against documented failure events and maintenance records.
9. Conclusion
This paper presents an AI-based prototype for anomaly detection and maintenance inspection prioritization in a smart manufacturing scenario. The implementation combines industrial sensor preprocessing, rolling-deviation features, Isolation Forest, relative-risk classification, machine-level reports, and an interactive Streamlit dashboard.
The system processed 99,972 records from 50 machines and identified 4,999 observations as anomalous under a 5% contamination configuration. It also generated risk distributions, machine inspection rankings, and historical anomaly-score visualizations.
These results demonstrate a functioning anomaly-monitoring workflow. They do not establish actual future-failure prediction, remaining useful life, avoided downtime, or real 6G performance. Those capabilities require additional data, rigorous evaluation, and real-world validation.
The project provides a foundation for further investigation into machine learning for industrial condition monitoring and predictive maintenance.
References
[1] F. T. Liu, K. M. Ting, and Z.-H. Zhou, “Isolation Forest,” in Proceedings of the 2008 Eighth IEEE International Conference on Data Mining, 2008, pp. 413–422.
[2] V. Chandola, A. Banerjee, and V. Kumar, “Anomaly Detection: A Survey,” ACM Computing Surveys, vol. 41, no. 3, Article 15, 2009.
[3] A. K. S. Jardine, D. Lin, and D. Banjevic, “A Review on Machinery Diagnostics and Prognostics Implementing Condition-Based Maintenance,” Mechanical Systems and Signal Processing, vol. 20, no. 7, pp. 1483–1510, 2006.
[4] A. K. Susto, A. Schirru, S. Pampuri, S. McLoone, and A. Beghi, “Machine Learning for Predictive Maintenance: A Multiple Classifier Approach,” IEEE Transactions on Industrial Informatics, vol. 11, no. 3, pp. 812–820, 2015.
[5] Scikit-learn Developers, “IsolationForest,” Scikit-learn Documentation. Available: https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html
[6] Streamlit, “Streamlit Documentation.” Available: https://docs.streamlit.io/
Reproducibility note: Dataset statistics and model outputs reported in this paper are based on the current project implementation. Before external submission, verify the bibliography against the original publications, document the software versions and exact experimental configuration, and preserve the dataset and generated reports used for the results.