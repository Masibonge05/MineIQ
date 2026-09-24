import streamlit as st
import base64
from PIL import Image
from src.inference.pipeline import analyze
from app.components.header import render_header
from app.components.prediction_card import render_prediction
from app.components.decision_panel import render_decisions
from app.components.mineral_card import render_minerals

render_header()

st.title("Single Image Analysis")

uploaded_file = st.file_uploader("Upload Ore Image", type=['png', 'jpg', 'jpeg', 'h5'])

if uploaded_file is not None:
    # Display image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    
    if st.button("Analyse"):
        with st.spinner("Analyzing..."):
            res = analyze(None) # Mocking for now, in prod pass image
            
            if res['confidence'] == "LOW":
                st.error("⚠️ LOW CONFIDENCE — Recommend laboratory verification")
                
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Mineral Composition")
                render_minerals(res['minerals'])
                
                st.subheader("Explainability")
                with st.expander("Why? (Spectral Feature Contributions)"):
                    st.write("Placeholder for spectral importance chart.")
            
            with col2:
                st.subheader("Processability Predictions")
                render_prediction(res['processability'])
                
                st.subheader("Decision Support")
                render_decisions(res['decisions'])
                
            st.caption(f"Inference Latency: {res['latency_ms']} ms")
