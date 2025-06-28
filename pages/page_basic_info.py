import streamlit as st
import json
from components.buttons import big_green_button

def page_basic_info():
    st.markdown("<h2>Reference Textbook 조회를 위한 기본 정보를 입력해주세요.</h2>", unsafe_allow_html=True)
    
    with st.form("basic_info_form"):
        reg_num = st.text_input("등록번호")
        surgery_name = st.selectbox(
            "수술명",
            [
                "복강경 담낭절제", "복강경 충수절제", "십이지장궤양 천공의 일차봉합",
                "위궤양 천공으로 인한 위절제술", "소장 절제 및 문합", "회장맹장절제",
                "결장우반절제술", "하트만 수술", "탐색개복술", "서혜부 탈장 수술", "절개탈장 수술"
            ]
        )
        
        col1, col2, col3 = st.columns(3)
        with col1:
            patient_name = st.text_input("환자명")
        with col2:
            scheduled_date = st.text_input("시행예정일")
        with col3:
            age_gender = st.text_input("나이/성별")
        
        diagnosis = st.text_input("진단명", value="Acute cholecystitis (급성담낭염)")
        surgery_site = st.radio("수술부위표시", ["R", "L", "Both", "해당없음"], horizontal=True)
        
        st.markdown("**※ 참여 의료진 (집도의가 다수인 경우 모두 기재해 주시기 바랍니다.)**")
        operator = st.text_input("집도의")
        department = st.text_input("진료과목")
        specialist = st.radio("전문의여부", ["전문의", "일반의"], horizontal=True)
        
        st.markdown("**1. 환자 상태 및 특이사항**")
        past_history = st.radio("과거병력(질병/상해/수술)", ["유", "무"], horizontal=True)
        diabetes = st.radio("당뇨병", ["유", "무"], horizontal=True)
        smoking = st.radio("흡연유무", ["유", "무"], horizontal=True)
        hypertension = st.radio("고혈압", ["유", "무"], horizontal=True)
        allergy = st.radio("알레르기 등의 특이체질", ["유", "무"], horizontal=True)
        hypotension = st.radio("저혈압", ["유", "무"], horizontal=True)
        airway_abnormality = st.radio("기도이상", ["유", "무"], horizontal=True)
        cardiovascular = st.radio("심혈관질환", ["유", "무"], horizontal=True)
        respiratory = st.radio("호흡기질환", ["유", "무"], horizontal=True)
        coagulation = st.radio("혈액응고 관련 질환", ["유", "무"], horizontal=True)
        medication = st.radio("복용약물", ["유", "무"], horizontal=True)
        kidney = st.radio("신장질환", ["유", "무"], horizontal=True)
        drug_abuse = st.radio("마약복용 혹은 약물사고", ["유", "무"], horizontal=True)
        etc = st.text_input("기타")
        
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
        
        submitted = big_green_button("수술 동의서 생성하기")
        if submitted:
            data = {
                "등록번호": reg_num,
                "수술명": surgery_name,
                "환자명": patient_name,
                "시행예정일": scheduled_date,
                "나이/성별": age_gender,
                "진단명": diagnosis,
                "수술부위표시": surgery_site,
                "집도의": operator,
                "진료과목": department,
                "전문의여부": specialist,
                "과거병력": past_history,
                "당뇨병": diabetes,
                "흡연유무": smoking,
                "고혈압": hypertension,
                "알레르기": allergy,
                "저혈압": hypotension,
                "기도이상": airway_abnormality,
                "심혈관질환": cardiovascular,
                "호흡기질환": respiratory,
                "혈액응고 관련 질환": coagulation,
                "복용약물": medication,
                "신장질환": kidney,
                "마약복용 혹은 약물사고": drug_abuse,
                "기타": etc,
                "예정된 수술을 하지 않을 경우의 예후": no_surgery_prognosis,
                "예정된 수술 이외의 시행 가능한 다른 방법": alternative_methods,
                "수술의 목적/필요성/효과": purpose,
                "수술의 방법 및 내용": method,
                "발생 가능한 합병증/후유증/부작용": complications,
                "문제 발생시 조치사항": actions_on_problems,
                "진단/수술 관련 사망 위험성": mortality_risk
            }
            # Save as JSON file for LLM prompt
            with open("patient_data.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            st.success("데이터가 patient_data.json 파일로 저장되었습니다.")
            st.session_state.step = 1
            st.experimental_rerun()
