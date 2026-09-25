import streamlit as st
import cv2
import numpy as np
from app.components.header import render_header

st.set_page_config(page_title="Live Camera | MineIQ", layout="wide")
render_header()
st.title("🎥 Live Camera Inference")

st.write("""
Test the MineIQ pipeline in real time using your webcam. 
Hold up a rock sample to the camera to see live mineral classification and processability predictions.
""")

col1, col2 = st.columns([3, 1])

with col1:
    camera_placeholder = st.empty()

with col2:
    st.subheader("Live Predictions")
    status_placeholder = st.empty()
    mineral_placeholder = st.empty()
    process_placeholder = st.empty()
    decision_placeholder = st.empty()

start_btn = st.button("Start Camera")
stop_btn = st.button("Stop Camera")

import time
import random
import yaml
from src.decision.engine import DecisionEngine

# Initialize the Decision Engine
try:
    decision_engine = DecisionEngine('configs/rules.yaml')
except Exception as e:
    st.error(f"Failed to load Decision Engine: {e}")
    decision_engine = None

if "camera_active" not in st.session_state:
    st.session_state.camera_active = False

if start_btn:
    st.session_state.camera_active = True

if stop_btn:
    st.session_state.camera_active = False

if st.session_state.camera_active:
    # Open default camera
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        st.error("Error: Could not access the webcam.")
    else:
        while st.session_state.camera_active:
            ret, frame = cap.read()
            if not ret:
                st.error("Error: Failed to grab frame.")
                break
                
            # --- DYNAMIC MOCK INFERENCE LOGIC ---
            # In production, you would pass the frame to classifier.predict(frame)
            
            # Simulate changing mineral compositions over time to trigger different rules
            t = time.time()
            pyrite_val = 12 + 10 * np.sin(t / 2) # Fluctuates between 2 and 22
            alunite_val = max(0, 5 * np.sin(t / 3)) # Fluctuates between 0 and 5
            silica_val = 8 + 5 * np.cos(t / 2.5) # Fluctuates between 3 and 13
            k_feldspar_val = 8 + 4 * np.sin(t / 4)
            cu_rec = 80 + 10 * np.cos(t / 3)
            
            minerals = {
                'pyrite': float(pyrite_val),
                'alunite': float(alunite_val),
                'silica': float(silica_val),
                'k-feldspar': float(k_feldspar_val),
                'chalcopyrite': 8.3
            }
            predictions = {
                'cu_recovery': {'value': float(cu_rec)},
                'bwi': {'value': 14.0}
            }
            
            # Draw a bounding box in the center for targeting
            h, w = frame.shape[:2]
            box_size = 200
            x1 = w//2 - box_size//2
            y1 = h//2 - box_size//2
            x2 = w//2 + box_size//2
            y2 = h//2 + box_size//2
            
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, "Align Sample Here", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            
            # Convert BGR to RGB for Streamlit
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Display frame
            camera_placeholder.image(frame_rgb, use_column_width=True)
            
            # Update prediction dashboard
            status_placeholder.success("Active - Scanning...")
            
            mineral_placeholder.markdown(f"""
            **Minerals Identified:**
            * Pyrite: {pyrite_val:.1f}%
            * Silica: {silica_val:.1f}%
            * K-Feldspar: {k_feldspar_val:.1f}%
            * Alunite: {alunite_val:.1f}%
            * Chalcopyrite: 8.3%
            """)
            
            process_placeholder.markdown(f"""
            **Processability Predictions:**
            * Cu Recovery: {cu_rec:.1f}% (Medium Confidence)
            * Bond WI: 14.0
            """)
            
            if decision_engine:
                decisions = decision_engine.evaluate(minerals, predictions, confidence=0.7)
                if decisions:
                    alert_md = ""
                    for d in decisions:
                        icon = "🔴" if d['priority'] == 'HIGH' else "🟠"
                        alert_md += f"{icon} **{d['priority']} PRIORITY:** {d['message']}\n\n"
                    decision_placeholder.warning(alert_md)
                else:
                    decision_placeholder.info("🟢 No immediate alert. Normal processing.")
            
            # We add a small sleep to avoid maxing out CPU
            cv2.waitKey(100)
            
        cap.release()
else:
    camera_placeholder.info("Camera is currently stopped. Click 'Start Camera' to begin.")
