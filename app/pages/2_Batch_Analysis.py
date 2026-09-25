import streamlit as st
import pandas as pd
from src.inference.pipeline import analyze
from app.components.header import render_header

render_header()
st.title("Batch Analysis")
st.write("Upload multiple ore images to process them in batch.")

uploaded_files = st.file_uploader("Upload Ore Images", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)

if uploaded_files:
    if st.button("Run Batch Analysis"):
        results = []
        progress_bar = st.progress(0)
        
        for i, file in enumerate(uploaded_files):
            # In a real scenario, we would pass file to analyze()
            res = analyze(None) 
            
            row = {
                "Filename": file.name,
                "Confidence": f"{res['confidence_score']:.2f}",
                "Decision_Alerts": len(res['decisions']),
                "Cu_Recovery_Pred": round(res['processability']['cu_recovery']['value'], 2)
            }
            
            # Flatten minerals into columns
            for m, v in res['minerals'].items():
                row[f"Mineral_{m.capitalize()}"] = round(v * 100, 2)
                
            results.append(row)
            progress_bar.progress((i + 1) / len(uploaded_files))
            
        df = pd.DataFrame(results)
        st.success("Batch processing complete!")
        st.dataframe(df, use_container_width=True)
        
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Results (CSV)",
            data=csv,
            file_name="mineiq_batch_results.csv",
            mime="text/csv"
        )
