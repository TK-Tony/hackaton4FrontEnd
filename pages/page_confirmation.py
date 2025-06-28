import streamlit as st
from components.buttons import big_green_button

def page_confirmation():
    st.markdown('<h2 class="main-title">수술 동의서 확정을 위한 마지막 정보입니다.</h2>', unsafe_allow_html=True)
    with st.form("final_consent_form"):
        st.text_input("환자/보호자 성명")
        st.text_input("수술동의서 작성일")
        st.text_input("환자연락처")
        st.text_input("보호자연락처")
        st.text_area("환자/보호자가 보는 사항")
        st.radio("설명동의서", ["설명동의서를 직접 읽고 이해함", "설명동의서를 듣고 이해함", "기타"])
        submitted = big_green_button("수술 동의서 PDF 출력하기")
        if submitted:
            st.session_state.step = 3
            st.experimental_rerun()
    if st.button("이전 단계로"):
        st.session_state.step = 1
        st.experimental_rerun()
