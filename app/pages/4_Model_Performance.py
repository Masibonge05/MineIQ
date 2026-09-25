import streamlit as st
import json
import os
import pandas as pd
from app.components.header import render_header

render_header()
st.title("Model Performance")

st.header("Processability Model (Quantile Regression)")
metrics_path = "outputs/metrics/processability_metrics.json"

if os.path.exists(metrics_path):
    with open(metrics_path, "r") as f:
        metrics = json.load(f)
        
    df = pd.DataFrame.from_dict(metrics, orient='index')
    
    st.write("### Evaluation Metrics on HIDSAG GEOMET Test Set")
    st.dataframe(
        df.style.highlight_max(subset=['PI_Coverage'], color='rgba(0, 255, 0, 0.2)')
                .highlight_min(subset=['MAE', 'RMSE'], color='rgba(0, 255, 0, 0.2)'),
        use_container_width=True
    )
else:
    st.warning("Processability metrics not found. Please run the training script.")

st.header("Mineral Classifier (ResNet50)")
st.info("Waiting for Person 2 to finish training and export classification_report.json.")
