import pandas as pd
import numpy as np
import logging

# Setup logging
# Logging Initialization:
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ----------- Preprocessing Function -----------

def preprocess_sensor_data(df):
    logging.info("Preprocessing started...")

    # Identify sensor columns dynamically (exclude non-sensor fields)
    sensor_cols = [col for col in df.columns if col not in ['Timestamp', 'Fault']]

    long_df = df.melt(id_vars=['Timestamp'], value_vars=sensor_cols, var_name='Sensor', value_name='Value')
    logging.info(f"Preprocessing complete. Data shape: {long_df.shape}")

    return long_df

# ----------- Fault Detection Function -----------

def detect_faults(df):
    def classify_fault(value):
        if value < 20:
            return "Very Low", "Critical"
        elif 20 <= value < 40:
            return "Low", "Warning"
        elif 40 <= value <= 80:
            return "Normal", "None"
        elif 80 < value <= 99:
            return "High", "Warning"
        else:
            return "Very High", "Critical"

    try:
        df[['FaultType', 'Severity']] = df['Value'].apply(lambda x: pd.Series(classify_fault(x)))
        logging.info("✅ Fault classification completed successfully.")
        return df
    except Exception as e:
        logging.error("❌ Error during fault classification.", exc_info=True)
        raise e  

