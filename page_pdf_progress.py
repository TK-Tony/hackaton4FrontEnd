import streamlit as st

def page_pdf_progress():
    col1, col2 = st.columns([1, 1])
    with col1:
        st.image("assets/images/pdf_preview.png", caption="PDF 미리보기 (예시)", use_container_width=True)
    with col2:
        st.markdown('<h3 class="main-title">PDF 출력중입니다.<br>잠시만 기다려주세요.</h3>', unsafe_allow_html=True)
    if st.button("다음"):
        st.session_state.step = 4
        st.experimental_rerun()
    if st.button("이전 단계로"):
        st.session_state.step = 2
        st.experimental_rerun()
