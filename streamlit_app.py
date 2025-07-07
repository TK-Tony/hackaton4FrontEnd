import streamlit as st

from components.header import render_header
from page_main import page_main
from page_basic_info import page_basic_info
from page_surgery_info import page_surgery_info
from page_confirmation import page_confirmation
from page_pdf_progress import page_pdf_progress
import extra_streamlit_components as stx

from page_basic_info import page_basic_info
from possum_calculator import main as possum_main

if "show_possum" not in st.session_state:
    st.session_state.show_possum = False
STEP_LABELS = [
    "Basic Information",
    "Surgery Information",
    "Confirmation",
    "Change to PDF",
]

PAGE_FUNCS = [
    page_basic_info,
    page_surgery_info,
    page_confirmation,
    #lambda: page_confirmation(st.session_state.get("consent_data", {})),
    page_pdf_progress,
]

# Initialize session state
if "step" not in st.session_state:
    st.session_state.step = -1  # -1 for main page

# Header
st.set_page_config(layout="wide")
render_header()

if st.session_state.show_possum:
    possum_main()  # Show the POSSUM calculator
# elif st.session_state.step == 3:  # PDF 생성 단계
#     page_pdf_progress()
else:
    # Your existing stepper logic
    if st.session_state.step == -1:
        if page_main():
            st.session_state.step = 0
            st.markdown("<script>window.scrollTo(0, 0);</script>", unsafe_allow_html=True)
            st.rerun()
    else:
        val = stx.stepper_bar(steps=STEP_LABELS, lock_sequence=False)
        if val != st.session_state.step:
            st.session_state.step = val
            st.markdown("<script>window.scrollTo(0, 0);</script>", unsafe_allow_html=True)
            st.rerun()
        PAGE_FUNCS[st.session_state.step]()