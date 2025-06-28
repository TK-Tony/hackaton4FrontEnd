import streamlit as st

def page_pdf_success():
    col1, col2 = st.columns([1, 1])
    with col1:
        st.image("assets/images/pdf_preview.png", caption="PDF 미리보기 (예시)", use_column_width=True)
    with col2:
        st.markdown('<h3 class="main-title">PDF 출력이 완료되었습니다.<br>항상 환자를 위한 헌신에 감사드립니다.</h3>', unsafe_allow_html=True)
    if st.button("메인화면으로"):
        st.session_state.step = 0
        st.experimental_rerun()
