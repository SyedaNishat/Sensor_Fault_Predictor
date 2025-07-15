import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.data_processing import preprocess_sensor_data, detect_faults
from utils.db_manager import init_db, insert_sensor_data

from datetime import timedelta
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize DB
init_db()

# Streamlit page config
st.set_page_config(page_title="Sensor Fault Detector", layout="wide")
st.title("⚙️ Sensor Fault Detection and Prediction Dashboard")

# Sidebar - File uploader
st.sidebar.header("📂 Upload Sensor Data")
uploaded_file = st.sidebar.file_uploader("Upload CSV file", type=["csv"])

# Main logic
if uploaded_file:
    try:
        df_raw = pd.read_csv(uploaded_file)

        # Check for required columns
        required_cols = {'Timestamp', 'Sensor_1', 'Sensor_2', 'Sensor_3'}
        if not required_cols.issubset(df_raw.columns):
            st.error(f"❌ Uploaded file is missing required columns: {required_cols - set(df_raw.columns)}")
            st.stop()

        if df_raw.empty:
            st.error("❌ Uploaded file is empty.")
            st.stop()

        st.success("✅ File uploaded successfully!")

        # Optional raw data preview
        with st.expander("🔍 Show Raw Uploaded Data"):
            st.dataframe(df_raw.head(100))

        # Preprocess & detect faults
        df_raw = preprocess_sensor_data(df_raw)
        df = detect_faults(df_raw)

        df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
        df.dropna(subset=['Timestamp'], inplace=True)

        # ✅ Store Processed Data in DB
        insert_sensor_data(df)

        # 📅 Filter by Date Range
        st.subheader("📅 Filter by Date Range")
        min_date = df['Timestamp'].min().date()
        max_date = df['Timestamp'].max().date()
        default_start = max_date - timedelta(days=7) if (max_date - min_date).days >= 7 else min_date

        start_date, end_date = st.date_input(
            "Select date range:",
            [default_start, max_date],
            min_value=min_date,
            max_value=max_date
        )

        if start_date == end_date:
            st.error("⚠️ Please select a valid date range (Start and End dates must be different).")
            st.stop()

        mask = (df['Timestamp'].dt.date >= start_date) & (df['Timestamp'].dt.date <= end_date)
        df = df[mask]

        # Sensor-Level Summary
        st.subheader("📋 Sensor-Level Summary")
        summary = df.groupby("Sensor").agg(
            Total_Readings=("Value", "count"),
            Critical_Faults=("Severity", lambda x: (x == "Critical").sum()),
            Warnings=("Severity", lambda x: (x == "Warning").sum()),
            Normal=("Severity", lambda x: (x == "None").sum())
        ).reset_index()
        st.dataframe(summary)

        # Sensor Readings Trend
        st.subheader("📈 Sensor Readings Over Time")
        available_sensors = df['Sensor'].unique().tolist()
        selected_sensors = st.multiselect("Select Sensors to Plot:", options=available_sensors, default=available_sensors)

        if selected_sensors:
            trend_data = df[df['Sensor'].isin(selected_sensors)]
            fig, ax = plt.subplots(figsize=(10, 4))
            sns.lineplot(data=trend_data, x="Timestamp", y="Value", hue="Sensor", ax=ax)
            ax.set_title("Sensor Readings Over Time")
            st.pyplot(fig)
        else:
            st.warning("Please select at least one sensor to display the chart.")

        # Fault Distribution per Sensor
        st.subheader("📊 Fault Distribution per Sensor")
        fault_counts = df.groupby(['Sensor', 'FaultType']).size().reset_index(name='Count')
        fig2, ax2 = plt.subplots(figsize=(10, 5))
        sns.barplot(data=fault_counts, x='Sensor', y='Count', hue='FaultType', palette='Set2')
        ax2.set_title("Fault Counts per Sensor by Fault Type")
        st.pyplot(fig2)

        # Most Faulty Sensor
        total_faults = fault_counts.groupby('Sensor')['Count'].sum()
        most_faulty_sensor = total_faults.idxmax()
        st.markdown(f"### 🔎 Sensor with Most Faults: **{most_faulty_sensor}** ({total_faults.max()} faults)")

        # Processed Data View
        st.subheader("🔍 Processed Sensor Data with Fault Classification")
        st.dataframe(df.head(100))

        # Export Filtered Data
        st.subheader("📥 Export Filtered Data")
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Download CSV", data=csv, file_name='filtered_sensor_faults.csv', mime='text/csv')

        # Fault Severity Breakdown
        st.subheader("🧯 Fault Severity Breakdown")
        severity_counts = df['Severity'].value_counts()
        st.bar_chart(severity_counts)

    except pd.errors.EmptyDataError:
        st.error("❌ File is empty or has no parsable columns.")
    except pd.errors.ParserError:
        st.error("❌ File could not be parsed. Please upload a valid CSV.")
    except Exception as e:
        logging.error("An error occurred while processing the file.", exc_info=True)
        st.error(f"❌ Error: {e}")

else:
    st.info("📅 Please upload a CSV file.")
