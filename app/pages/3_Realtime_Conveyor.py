import streamlit as st
import time
from src.inference.pipeline import analyze
from app.components.header import render_header
from app.components.prediction_card import render_prediction
from app.components.decision_panel import render_decisions
from app.components.mineral_card import render_minerals

render_header()
st.title("Realtime Conveyor Stream")

if st.button("Start Conveyor Simulation"):
    st.write("Simulating realtime feed...")
    
    col1, col2 = st.columns(2)
    with col1:
        min_placeholder = st.empty()
    with col2:
        proc_placeholder = st.empty()
    
    dec_placeholder = st.empty()
    
    for i in range(1, 20):
        # Trigger the full end-to-end pipeline (Classifier -> Processability -> Decision)
        res = analyze(None)
        
        with min_placeholder.container():
            st.subheader(f"Sample {i}: Mineral Composition")
            render_minerals(res['minerals'])
            
        with proc_placeholder.container():
            st.subheader("Processability Predictions")
            render_prediction(res['processability'])
            
        with dec_placeholder.container():
            st.subheader("Decision Support")
            if res['confidence'] == "LOW":
                st.error("🚨 MANUAL / LABORATORY VERIFICATION REQUIRED")
            else:
                render_decisions(res['decisions'])
                
        time.sleep(1)
