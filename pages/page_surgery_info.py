import streamlit as st
from components.buttons import big_green_button

def page_surgery_info():
    st.set_page_config(layout="wide")

    st.markdown('<h2 class="main-title">Reference Textbook을 기반으로 작성된 수술 관련 정보입니다.<br>확인 후 수정사항이 있으면 반영한 후 확정해주세요.</h2>', unsafe_allow_html=True)
    with st.form("surgery_info_form"):
        st.markdown("**2. 예정된 수술을 하지 않을 경우의 예후**")
        no_surgery_prognosis = st.text_area("예정된 수술을 하지 않을 경우의 예후")
        
        st.markdown("**3. 예정된 수술 이외의 시행 가능한 다른 방법**")
        alternative_methods = st.text_area("예정된 수술 이외의 시행 가능한 다른 방법")
        
        st.markdown("**4. 수술의 목적/필요성/효과**")
        purpose = st.text_area("수술의 목적/필요성/효과")
        
        st.markdown("**5. 수술의 방법 및 내용**")
        method = st.text_area("수술의 방법 및 내용")
        
        st.markdown("**6. 발생 가능한 합병증/후유증/부작용**")
        complications = st.text_area("발생 가능한 합병증/후유증/부작용")
        
        st.markdown("**7. 문제 발생시 조치사항**")
        actions_on_problems = st.text_area("문제 발생시 조치사항")
        
        st.markdown("**8. 진단/수술 관련 사망 위험성**")
        mortality_risk = st.text_area("진단/수술 관련 사망 위험성")

        submitted = big_green_button("수술 내용 확정하기")
        if submitted:
            data = {
                "예정된 수술을 하지 않을 경우의 예후": no_surgery_prognosis,
                "예정된 수술 이외의 시행 가능한 다른 방법": alternative_methods,
                "수술의 목적/필요성/효과": purpose,
                "수술의 방법 및 내용": method,
                "발생 가능한 합병증/후유증/부작용": complications,
                "문제 발생시 조치사항": actions_on_problems,
                "진단/수술 관련 사망 위험성": mortality_risk
            }
            st.session_state.step = 2
            st.experimental_rerun()
    if st.button("이전 단계로"):
        st.session_state.step = 0
        st.experimental_rerun()
