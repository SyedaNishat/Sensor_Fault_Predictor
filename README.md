# ⚙️ Sensor Fault Detection and Prediction Dashboard

An interactive Streamlit web app that allows users to upload sensor data, classify faults using defined thresholds, and visualize trends, severities, and distributions — making it ideal for fault monitoring in industrial IoT systems.

---

## 🚀 Features

- 📁 Upload CSV sensor data
- 🧹 Preprocess and reshape sensor data
- 📊 Detect and classify sensor faults:
  - Very Low, Low, Normal, High, Very High
- 🔎 Filter by date range
- 📈 Visualize trends using line charts
- 📉 Sensor fault distribution charts
- 🧯 Fault severity breakdown
- ⬇️ Export processed results as CSV

---

## 📂 File Structure

Sensor_Fault_Predictor/
│
├── data/ # Sample datasets
│ ├── sensor_fault_dataset.csv
│ └── ...
│
├── streamlit_app/
│ └── app.py # 📌 Main Streamlit App
│
├── tests/
│ └── test_data_processing.py # ✅ Pytest Unit Tests
│
├── utils/
│ ├── data_processing.py # 🔧 Preprocessing & Classification Functions
│
├── README.md # 📘 Project Overview
└── requirements.txt # 📦 Required Python Libraries



## 🛠️ Installation & Run

```bash
# Clone this repository
git clone https://github.com/SyedaNishat/sensor_fault_predictor.git
cd sensor_fault_predictor

# Create virtual environment (optional but recommended)
python -m venv venv
venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run streamlit_app/app.py
