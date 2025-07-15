# Sensor Fault Detection and Prediction Dashboard

A **Streamlit-based interactive dashboard** to detect, classify, visualize, and export sensor faults using real-time data analysis, fault severity classification, and database integration.

---

## Project Overview

This dashboard allows users to:

* Upload sensor CSV files
* Preprocess and reshape data for analysis
* Detect and classify sensor faults
* Visualize sensor trends and fault patterns
* Understand fault severity breakdown
* Store and retrieve data in a SQLite database
* Export filtered, processed data

---

##  Features

👉 File upload with validation
👉 Preprocessing (wide-to-long format)
👉 Fault classification (`Very Low`, `Low`, `Normal`, `High`, `Very High`)
👉 Severity tagging (`None`, `Warning`, `Critical`)
👉 Date range filtering (default: last 7 days)
👉 Sensor-wise fault summary
👉 Line plots for sensor readings
👉 Bar charts for fault distribution
👉 SQLite database integration
👉 Filtered CSV export
👉 Clean, recruiter-friendly UI

---

##  Sample Output

| Component    | Example                           |
| ------------ | --------------------------------- |
|  Fault Type | `Very Low`, `Normal`, `Very High` |
|  Severity   | `Critical`, `None`, `Warning`     |
|  Line Plot | Sensor readings over time         |
|  Bar Chart | Fault counts per sensor           |

---

##  How It Works

1. **Upload a CSV** with sensor readings (`Timestamp`, `Sensor_1`, `Sensor_2`, ...).
2. **Preprocessing** transforms it to long format and parses timestamps.
3. **Fault Classification** is applied using defined thresholds.
4. **Data Filtering** by date range enables focused analysis.
5. **Visualization** using Matplotlib and Seaborn.
6. **SQLite Integration** saves processed data.
7. **Export** the filtered result to a new CSV.

---

## Example Input Format

```csv
Timestamp,Sensor_1,Sensor_2,Sensor_3
2025-01-01 00:00,50.0,30.0,90.0
2025-01-01 00:01,55.0,35.0,100.0
```

---

## Tech Stack

* Python 3.10+
* Streamlit
* Pandas
* Seaborn & Matplotlib
* SQLite (via `sqlite3`)
* Logging
* Pytest (for unit testing)

---

##  Use Cases

* Sensor Fault Monitoring in Industrial IoT
* Fault Severity Alert Systems
* Exploratory Data Analysis (EDA) on Time-Series Sensor Logs
* Data Engineering Portfolio Projects

---

## Future Enhancements

* Email alerts for critical faults
* Historical trends from stored DB
* ML-based anomaly detection
* Role-based login for field engineers
