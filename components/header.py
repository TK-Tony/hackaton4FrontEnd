import streamlit as st

def render_header():
    st.markdown("""
        <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined" rel="stylesheet" />

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
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .header-bar .material-symbols-outlined {
            font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
            font-size: 20px;
            color: white;
        }
        </style>

        <div class="header-bar">
            <span class="logo">SurgiForm</span>
            <span class="user-info">
                장재율 교수님, 안녕하세요
                <span class="material-symbols-outlined">settings</span>
                <span class="material-symbols-outlined">person</span>
            </span>
        </div>
    """, unsafe_allow_html=True)