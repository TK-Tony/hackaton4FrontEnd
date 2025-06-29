import streamlit as st

def page_pdf_success():
    #여백 제거 및 container 최대 폭 확장
    st.markdown("""
        <style>
        .block-container {
            padding: 0rem;
            max-width: 100% !important;
        }
        </style>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])
    with col1:
        st.image("assets/images/step2.png", caption="PDF 미리보기 (예시)", use_container_width=True)
    with col2:
        st.markdown('<h3 class="main-title">PDF 출력이 완료되었습니다.<br>항상 환자를 위한 헌신에 감사드립니다.</h3>', unsafe_allow_html=True)
    if st.button("메인화면으로"):
        st.session_state.step = 0
        st.rerun()