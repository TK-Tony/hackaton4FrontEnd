import streamlit as st

def render_header():
    st.markdown("""
        <style>
        .header-bar {
            background-color: #146c2f;
            color: white;
            padding: 12px 24px;
            font-size: 18px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 2px solid #0f4e20;
        }
        .logo {
            font-weight: bold;
            font-size: 20px;
        }
        .user-info {
            font-size: 16px;
        }
        </style>

        <div class="header-bar">
            <span class="logo">SurgiForm</span>
            <span class="user-info">
                장재율 교수님, 안녕하세요
                🛠️ 👤
            </span>
        </div>
    """, unsafe_allow_html=True)