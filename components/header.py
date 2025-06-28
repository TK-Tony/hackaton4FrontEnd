import streamlit as st

def render_header():
    st.markdown("""
    <div class="header-bar">
        <span class="logo">TrustSurgy</span>
        <span class="user-info">
            장재율 교수님, 안녕하세요
            🛠️
            👤
        </span>
    </div>
    """, unsafe_allow_html=True)

