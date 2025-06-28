import streamlit as st
import extra_streamlit_components as stx

from components.header import render_header
from pages.page_main import page_main
from pages.page_basic_info import page_basic_info
from pages.page_surgery_info import page_surgery_info
from pages.page_confirmation import page_confirmation
from pages.page_pdf_progress import page_pdf_progress
from pages.page_pdf_success import page_pdf_success

STEP_LABELS = [
    "Basic Information",
    "Surgery Information",
    "Confirmation",
    "Change to PDF",
    "Success"
]
PAGE_FUNCS = [
    page_basic_info,
    page_surgery_info,
    page_confirmation,
    page_pdf_progress,
    page_pdf_success
]

# Initialize session state
if "step" not in st.session_state:
    st.session_state.step = -1  # -1 for main page

# Header
render_header()

if st.session_state.step == -1:
    # Show main page first
    if page_main():
        st.session_state.step = 0
        st.rerun()
else:
    # Stepper navigation bar (no 'default' argument!)
    val = stx.stepper_bar(steps=STEP_LABELS, lock_sequence=False)
    if val != st.session_state.step:
        st.session_state.step = val
        st.rerun()
    # Show the current page
    PAGE_FUNCS[st.session_state.step]()
