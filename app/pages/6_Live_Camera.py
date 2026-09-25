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
                
            # --- MOCK INFERENCE LOGIC ---
            # In production, you would pass the frame to:
            # minerals = classifier.predict(frame)
            # targets = processability.predict(features)
            
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
            
            mineral_placeholder.markdown("""
            **Minerals Identified:**
            * Quartz: 41.2%
            * Pyrite: 17.6%
            * Chalcopyrite: 8.3%
            """)
            
            process_placeholder.markdown("""
            **Processability Predictions:**
            * Cu Recovery: 82.1% (High Confidence)
            * Bond WI: 15.2
            """)
            
            decision_placeholder.info("🟢 No immediate alert. Normal processing.")
            
            # We add a small sleep to avoid maxing out CPU (Streamlit loops can be aggressive)
            cv2.waitKey(100)
            
        cap.release()
else:
    camera_placeholder.info("Camera is currently stopped. Click 'Start Camera' to begin.")
