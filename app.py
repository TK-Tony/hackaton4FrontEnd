import streamlit as st

from components.header import render_header
from page_main import page_main
from page_basic_info import page_basic_info
from page_surgery_info import page_surgery_info
from page_confirmation import page_confirmation
from page_pdf_progress import page_pdf_progress
import extra_streamlit_components as stx

from possum_calculator import main as possum_main

if "show_possum" not in st.session_state:
    st.session_state.show_possum = False
# Initialize session state
if "step" not in st.session_state:
    st.session_state.step = 0  # -1 for main page

STEP_LABELS = [
    "Main",
    "Basic Information",
    "Surgery Information",
    "Confirmation",
    "Change to PDF",
]

PAGE_FUNCS = [
    page_main,
    page_basic_info,
    page_surgery_info,
    page_confirmation,
    page_pdf_progress,
]


# Header
st.set_page_config(layout="wide")
render_header()

if st.session_state.show_possum:
    possum_main()  # Show the POSSUM calculator
    st.stop()
elif st.session_state.step == 4:  # PDF 생성 단계
    page_pdf_progress()
    st.stop()
elif st.session_state.step == 0:
    if page_main():
        st.session_state.step = 1
        st.rerun()            
    st.stop()                 
else:
    st.markdown("<div style='margin-bottom: 10px;'></div>", unsafe_allow_html=True)
    val = stx.stepper_bar(
        steps=STEP_LABELS[1:], 
        lock_sequence=False
    )
    val += 1
    if val != st.session_state.step:
        st.session_state.step = val
        st.rerun()

    PAGE_FUNCS[st.session_state.step]()
