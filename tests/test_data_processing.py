import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.data_processing import preprocess_sensor_data, detect_faults
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

st.set_page_config(page_title="Sensor Fault Detector", layout="wide")
st.title("⚙️ Sensor Fault Detection and Prediction Dashboard")

st.sidebar.header("📂 Upload Sensor Data")
uploaded_file = st.sidebar.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file:
    try:
        df_raw = pd.read_csv(uploaded_file)
        st.success("✅ File uploaded successfully!")

        df_raw = preprocess_sensor_data(df_raw)
        df = detect_faults(df_raw)

        df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
        df.dropna(subset=['Timestamp'], inplace=True)

        st.subheader("📅 Filter by Date Range")
        min_date = df['Timestamp'].min().date()
        max_date = df['Timestamp'].max().date()

        start_date, end_date = st.date_input(
            "Select date range:",
            [min_date, max_date],
            min_value=min_date,
            max_value=max_date
        )

        if start_date == end_date:
            st.error("⚠️ Please select a valid date range (Start and End dates must be different).")
            st.stop()

        mask = (df['Timestamp'].dt.date >= start_date) & (df['Timestamp'].dt.date <= end_date)
        df = df[mask]

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

        st.subheader("🔍 Processed Sensor Data with Fault Classification")
        st.dataframe(df.head(100))

        st.subheader("📊 Fault Distribution per Sensor")
        fault_counts = df.groupby(['Sensor', 'FaultType']).size().reset_index(name='Count')
        fig2, ax2 = plt.subplots(figsize=(10, 5))
        sns.barplot(data=fault_counts, x='Sensor', y='Count', hue='FaultType', palette='Set2')
        ax2.set_title("Fault Counts per Sensor by Fault Type")
        st.pyplot(fig2)

        total_faults = fault_counts.groupby('Sensor')['Count'].sum()
        most_faulty_sensor = total_faults.idxmax()
        st.markdown(f"### 🔎 Sensor with Most Faults: **{most_faulty_sensor}** ({total_faults.max()} faults)")

        st.subheader("📥 Export Processed Data")
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Download CSV", data=csv, file_name='sensor_faults.csv', mime='text/csv')

        st.subheader("🧯 Fault Severity Breakdown")
        severity_counts = df['Severity'].value_counts()
        st.bar_chart(severity_counts)

    except Exception as e:
        logging.error("An error occurred while processing the file.", exc_info=True)
        st.error(f"❌ Error: {e}")

else:
    st.info("📅 Please upload a CSV file with `Timestamp`, `Sensor_1`, `Sensor_2`, `Sensor_3`.")

def test_preprocess_sensor_data_basic():
    mock_df = pd.DataFrame({
        'Timestamp': ['2025-01-01 00:00', '2025-01-01 00:01'],
        'Sensor_1': [50.0, 55.0],
        'Sensor_2': [30.0, 35.0],
        'Sensor_3': [70.0, 65.0],
        'Fault': [0, 1]
    })

    processed_df = preprocess_sensor_data(mock_df)

    expected_columns = ['Timestamp', 'Sensor', 'Value']
    for col in expected_columns:
        assert col in processed_df.columns, f"{col} is missing in processed DataFrame"

    # Optional: Check if 'Fault' is present as a value in 'Sensor'
    assert 'Fault' in processed_df['Sensor'].unique(), "'Fault' not found in Sensor column after melting"

def test_detect_faults_classification():
    # Create mock input DataFrame
    mock_df = pd.DataFrame({
        'Timestamp': ['2025-01-01 00:00'] * 3,
        'Sensor': ['Sensor_1', 'Sensor_2', 'Sensor_3'],
        'Value': [10.0, 60.0, 100.0]  # Low, Normal, High
    })

    # Expected thresholds:
    # - Sensor_1 = 10 → Very Low
    # - Sensor_2 = 60 → Normal
    # - Sensor_3 = 100 → Very High

    # Call detect_faults
    result_df = detect_faults(mock_df)

    # Check if FaultType and Severity columns exist
    assert 'FaultType' in result_df.columns
    assert 'Severity' in result_df.columns

    # Check Fault Types
    expected_faults = ['Very Low', 'Normal', 'Very High']
    expected_severity = ['Critical', 'None', 'Critical']

    assert result_df['FaultType'].tolist() == expected_faults
    assert result_df['Severity'].tolist() == expected_severity
