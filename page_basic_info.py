import streamlit as st
import json
from components.buttons import big_green_button

def page_basic_info():
    st.set_page_config(layout="wide")
    st.markdown("""
        <h2 style='text-align:center; color:#176d36; margin: 0 0 20px 0'>Reference Textbook 조회를 위한 기본 정보를 입력해주세요.</h2>
    """, unsafe_allow_html=True)

    with st.form("basic_info_form"):
        surgery_name = st.selectbox(
            "수술명",
            [
                "복강경 담낭절제", "복강경 충수절제", "십이지장궤양 천공의 일차봉합",
                "위궤양 천공으로 인한 위절제술", "소장 절제 및 문합", "회장맹장절제",
                "결장우반절제술", "하트만 수술", "탐색개복술", "서혜부 탈장 수술", "절개탈장 수술"
            ]
        )

        # 첫 줄에 등록번호 / 환자명, 둘째 줄에 나이/성별 / 시행예정일
        col1, col2 = st.columns(2)
        with col1:
            reg_num = st.text_input("등록번호")
        with col2:
            patient_name = st.text_input("환자명")

        col3, col4 = st.columns(2)
        with col3:
            age_gender = st.text_input("나이/성별")
        with col4:
            scheduled_date = st.text_input("시행예정일")

        # 진단명 드롭다운
        diagnosis = st.selectbox(
            "진단명",
            [
                "Acute cholecystitis (급성담낭염)",
                "Acute appendicitis (급성충수염)",
                "Duodenal ulcer perforation (십이지장궤양 천공)",
                "Gastric ulcer perforation (위궤양 천공)",
                "Small intestine obstruction (소장 폐쇄)",
                "Small intestine perforation (소장 천공)",
                "Ascending colon perforation (상행결장 천공)",
                "Transverse colon perforation (횡행결장 천공)",
                "Sigmoid colon perforation (에스상결장 천공)",
                "Pneumoperitoneum (기복증)",
                "Inguinal hernia (서혜부 탈장)",
                "Incisional hernia (절개탈장)"
            ]
        )

        col5, col6 = st.columns(2)
        with col5: #수술부위표시
            surgery_site = st.radio("수술부위표시", ["R", "L", "Both", "해당없음"], horizontal=True)
        with col6: #수술부위
            surgery_site_detail = st.text_input("수술부위", placeholder="예: 좌측 하복부 등")
        
        # 집도의, 전문의 여부, 진료과목
        st.markdown("**※ 참여 의료진 (집도의가 다수인 경우 모두 기재해 주시기 바랍니다.)**")
        for i in range(1, 4):  # 최대 3명까지 반복
            col1, col2, col3 = st.columns([2, 2, 3])
            with col1:
                st.text_input(f"집도의 {i}", key=f"operator_{i}")
            with col2:
                st.radio(
                    label="전문의 여부",
                    options=["전문의", "일반의"],
                    horizontal=True,
                    index=0,
                    key=f"specialist_{i}"
                )
            with col3:
                st.text_input("진료과목", key=f"department_{i}")

        st.markdown("**1. 환자 상태 및 특이사항**")

        col1, col2 = st.columns(2)
        with col1:
            past_history = st.radio("과거병력(질병/상해/수술)", ["유", "무"], index=1, horizontal=True)
            smoking = st.radio("흡연유무", ["유", "무"], index=1, horizontal=True)
            allergy = st.radio("알레르기 등의 특이체질", ["유", "무"], index=1, horizontal=True)
            airway_abnormality = st.radio("기도이상", ["유", "무"], index=1, horizontal=True)
            respiratory = st.radio("호흡기질환", ["유", "무"], index=1, horizontal=True)
            medication = st.radio("복용약물", ["유", "무"], index=1, horizontal=True)
            drug_abuse = st.radio("마약복용 혹은 약물사고", ["유", "무"], index=1, horizontal=True)

        with col2:
            diabetes = st.radio("당뇨병", ["유", "무"], index=1, horizontal=True)
            hypertension = st.radio("고혈압", ["유", "무"], index=1, horizontal=True)
            hypotension = st.radio("저혈압", ["유", "무"], index=1, horizontal=True)
            cardiovascular = st.radio("심혈관질환", ["유", "무"], index=1, horizontal=True)
            coagulation = st.radio("혈액응고 관련 질환", ["유", "무"], index=1, horizontal=True)
            kidney = st.radio("신장질환", ["유", "무"], index=1, horizontal=True)
            possum = st.form_submit_button("POSSUM 점수 계산", help="수술의 위험도를 평가하기 위한 POSSUM 점수를 계산합니다.")
        
        etc = st.text_area("기타", placeholder="환자의 상태나 기타 특이사항이 있다면 기재해 주세요. 자세할수록 레퍼런스 조회가 용이합니다.\n단, 환자명 등의 개인 식별 정보는 기재하지 말아주세요.")

        submitted = big_green_button("수술 동의서 생성하기")
        if submitted:
            # 집도의 목록 수집
            doctors = []
            for i in range(1, 4):
                operator = st.session_state.get(f"operator_{i}", "")
                specialist = st.session_state.get(f"specialist_{i}", "")
                department = st.session_state.get(f"department_{i}", "")
                if operator:
                    doctors.append({
                        "집도의": operator,
                        "전문의여부": specialist,
                        "진료과목": department
                    })
            data = {
                "등록번호": reg_num,
                "수술명": surgery_name,
                "환자명": patient_name,
                "시행예정일": scheduled_date,
                "나이/성별": age_gender,
                "진단명": diagnosis,
                "수술부위표시": surgery_site,
                "수술부위": surgery_site_detail, #추가함
                "의료진": doctors, #리스트로 받아야 해서 변경됨
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
                "기타": etc
            }
            # Save as JSON file for LLM prompt
            with open("patient_data.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            st.success("데이터가 patient_data.json 파일로 저장되었습니다.")
            st.session_state.step = 1
            st.rerun()
        elif possum:
            # Perform your calculations or actions here
            st.write("Calculating POSSUM score...")
