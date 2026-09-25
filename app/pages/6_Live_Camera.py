import streamlit as st
import cv2
import time
from app.components.header import render_header
from src.inference.pipeline import analyze
from app.components.prediction_card import render_prediction
from app.components.decision_panel import render_decisions
from app.components.mineral_card import render_minerals

st.set_page_config(page_title="Live Camera | MineIQ", layout="wide")
render_header()
st.title("🎥 Live Camera Inference (RGB Mode)")

st.write("Test the MineIQ pipeline in real time using your webcam. Hold up different colored objects (e.g. yellow for Chalcopyrite, grey for Silica) to see the AI dynamically respond!")

col1, col2 = st.columns([2, 1])

with col1:
    camera_placeholder = st.empty()

with col2:
    st.subheader("Live Predictions")
    min_placeholder = st.empty()
    proc_placeholder = st.empty()
    dec_placeholder = st.empty()

start_btn = st.button("Start Camera")
stop_btn = st.button("Stop Camera")

if "camera_active" not in st.session_state:
    st.session_state.camera_active = False

if start_btn:
    st.session_state.camera_active = True

if stop_btn:
    st.session_state.camera_active = False

if st.session_state.camera_active:
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        st.error("Error: Could not access the webcam.")
    else:
        while st.session_state.camera_active:
            ret, frame = cap.read()
            if not ret:
                st.error("Error: Failed to grab frame.")
                break
                
            # Draw a bounding box for the sample
            h, w = frame.shape[:2]
            box_size = 200
            x1, y1 = w//2 - box_size//2, h//2 - box_size//2
            x2, y2 = w//2 + box_size//2, h//2 + box_size//2
            
            # Extract the region of interest to pass to the model
            roi = frame[y1:y2, x1:x2]
            
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, "Align Sample Here", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            camera_placeholder.image(frame_rgb, use_column_width=True)
            
            # --- RUN FULL PIPELINE ON THE WEBCAM ROI ---
            if roi.size == 0:
                roi = None
                
            res = analyze(roi)
            
            with min_placeholder.container():
                st.write("### Mineral Composition")
                render_minerals(res['minerals'])
                
            with proc_placeholder.container():
                st.write("### Processability Predictions")
                render_prediction(res['processability'])
                
            with dec_placeholder.container():
                st.write("### Decision Support")
                if res['confidence'] == "LOW":
                    st.error("🚨 **MANUAL / LABORATORY VERIFICATION REQUIRED**\n\nIncoming RGB signature falls outside well-characterised training distribution.")
                else:
                    render_decisions(res['decisions'])
            
            # Sleep slightly to prevent maxing CPU
            cv2.waitKey(100)
            
        cap.release()
else:
    camera_placeholder.info("Camera is currently stopped. Click 'Start Camera' to begin.")
