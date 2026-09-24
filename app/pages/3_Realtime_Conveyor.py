import streamlit as st
import time
from app.components.header import render_header

render_header()
st.title("Realtime Conveyor Stream")

if st.button("Start Conveyor Simulation"):
    st.write("Simulating realtime feed...")
    placeholder = st.empty()
    for i in range(1, 10):
        # TODO(person-3): Read from outputs/predictions/realtime_log.csv
        placeholder.info(f"Processed sample {i}...")
        time.sleep(1)
