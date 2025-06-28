import streamlit as st

def big_green_button(label: str):
    return st.form_submit_button(
        label,
        use_container_width=True
    )
