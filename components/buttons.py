import streamlit as st

def big_green_button(label: str):
    return st.form_submit_button(
        label,
    )
