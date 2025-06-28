import streamlit as st

def render_stepper(current_step):
    steps = [
        "Basic Information",
        "Surgery Information",
        "Confirmation",
        "Change to PDF",
        "Success"
    ]
    st.markdown('<div class="stepper">', unsafe_allow_html=True)
    for i, step in enumerate(steps):
        icon = "✅" if i <= current_step else "○"
        st.markdown(
            f'<span class="step {"active" if i == current_step else ""}">{icon}<br><span>{step}</span></span>',
            unsafe_allow_html=True
        )
    st.markdown('</div>', unsafe_allow_html=True)
