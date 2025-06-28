import streamlit as st
from components.buttons import big_green_button

def page_surgery_info():
    st.markdown('<h2 class="main-title">Reference Textbook을 기반으로 작성된 수술 관련 정보입니다.<br>확인 후 수정사항이 있으면 반영한 후 확정해주세요.</h2>', unsafe_allow_html=True)
    with st.form("surgery_info_form"):
        for i in range(1, 9):
            st.text_area(f"{i}. 항목", value="GPT가 생성한 여러 정보가 줄글로 적히고\n수정을 할 수 있는 여지를 두면 좋을 것 같습니다!")
        submitted = big_green_button("수술 내용 확정하기")
        if submitted:
            st.session_state.step = 2
            st.experimental_rerun()
    if st.button("이전 단계로"):
        st.session_state.step = 0
        st.experimental_rerun()
