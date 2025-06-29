import streamlit as st
import json
import requests
from components.buttons import big_green_button
import logging




# Initialize session state for POSSUM results and navigation
if 'possum_results' not in st.session_state:
    st.session_state.possum_results = None

if 'navigate_to_possum' not in st.session_state:
    st.session_state.navigate_to_possum = False

if 'show_possum' not in st.session_state:
    st.session_state.show_possum = False


def page_basic_info():
    st.set_page_config(layout="wide")


    #여백 제거 및 container 최대 폭 확장
    st.markdown("""
        <style>
        .block-container {
            padding: 0rem;
            max-width: 100% !important;
            margin-bottom: 1rem;
        }
        .form-wrapper {
            max-width: 800px;
            margin-left: 10px;
            margin-right: 10px;
            padding: 0rem;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <h2 style='text-align:center; color:#176d36; margin: 0 0 20px 0'>Reference Textbook 조회를 위한 기본 정보를 입력해주세요.</h2>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 6, 1]) 
    with col2:
        with st.form("basic_info_form"):
            st.markdown("### 0. 수술 기본 정보")
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
            with col5:
                surgery_site = st.radio("수술부위표시", ["R", "L", "Both", "해당없음"], horizontal=True)
            with col6:
                surgery_site_detail = st.text_input("수술부위", placeholder="예: 좌측 하복부 등")
            
            st.markdown("**※ 참여 의료진 (집도의가 다수인 경우 모두 기재해 주시기 바랍니다.)**")
            for i in range(1, 3+1):
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

            st.markdown("### 1. 환자 상태 및 특이사항")

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
                #can you make an additional table here so that we can put the two possum values in here? 
                possum = st.form_submit_button("POSSUM 점수 계산", help="수술의 위험도를 평가하기 위한 POSSUM 점수를 계산합니다.")
                if st.session_state.get("possum_results"):
                    st.markdown("**POSSUM 결과**")
                    colA, colB = st.columns(2)
                    with colA:
                        st.metric("Mortality Risk", f"{st.session_state.possum_results['mortality']:.2%}")
                    with colB:
                        st.metric("Morbidity Risk", f"{st.session_state.possum_results['morbidity']:.2%}")
            etc = st.text_area("기타", placeholder="환자의 상태나 기타 특이사항이 있다면 기재해 주세요. 자세할수록 레퍼런스 조회가 용이합니다.\n단, 환자명 등의 개인 식별 정보는 기재하지 말아주세요.")

            col1, col2, col3 = st.columns([1.5, 1, 1])
            with col2:
                submitted = st.form_submit_button("수술 동의서 생성하기")

            # POSSUM button: Navigate to calculator (no validation required)
            if possum:
                st.session_state.navigate_to_possum = True

            # 동의서 생성 로직
            if submitted:
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
                    "수술부위": surgery_site_detail,
                    "의료진": doctors,
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
                with open("patient_data.json", "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                st.success("데이터가 patient_data.json 파일로 저장되었습니다.")
                st.session_state.step = 1

                # --- API 전송 ---

                # 나이/성별 파싱
                age = None
                gender = None
                if "/" in age_gender:
                    age_part, gender_part = age_gender.strip().split("/")
                    age = int(age_part.strip())
                    gender = gender_part.strip().upper()
                    if gender not in ["M", "F"]:
                        st.error("성별은 M 또는 F로 입력해주세요.")
                        st.stop()
                else:
                    st.error("나이/성별 형식은 '45/M' 또는 '30/F'로 입력해야 합니다.")
                    st.stop()

                participants = []
                for doc in doctors:
                    participants.append({
                        "name": doc["집도의"],
                        "is_lead": True,
                        "is_specialist": doc["전문의여부"] == "전문의",
                        "department": doc["진료과목"]
                    })
                if not participants:
                    st.error("최소 1명의 집도의 정보를 입력해야 합니다.")
                    st.stop()

                special_conditions = {
                    "past_history": past_history,  # instead of past_history == "유"
                    "diabetes": diabetes,
                    "smoking": smoking,
                    "hypertension": hypertension,
                    "allergy": allergy,
                    "cardiovascular": cardiovascular,
                    "respiratory": respiratory,
                    "coagulation": coagulation,
                    "medications": medication,
                    "renal": kidney,
                    "drug_abuse": drug_abuse,
                    "other": etc
                }
                possum_score = {
                    "mortality_risk":st.session_state.possum_results.get("mortality", None) if st.session_state.possum_results else None,
                    "morbidity_risk":st.session_state.possum_results.get("morbidity", None) if st.session_state.possum_results else None

                }

                payload = {
                    "registration_no": reg_num,
                    "patient_name": patient_name,
                    "age": age,
                    "gender": gender,
                    "scheduled_date": scheduled_date,
                    "diagnosis": diagnosis,
                    "surgical_site_mark": surgery_site,
                    "participants": participants,
                    "patient_condition": "Stable",
                    "special_conditions": special_conditions,
                    "possum_score": possum_score
                }
                patient_data = {
                    "등록번호": reg_num,
                    "수술명": surgery_name,
                    "환자명": patient_name,
                    "시행예정일": scheduled_date,
                    "나이/성별": age_gender,
                    "진단명": diagnosis,
                    "수술부위표시": surgery_site,
                    "수술부위": surgery_site_detail,
                    "의료진": doctors,
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
                with open("patient_data.json", "w", encoding="utf-8") as f:
                    json.dump(patient_data, f, ensure_ascii=False, indent=2)
                # API 호출
                url = "http://10.104.198.155:8000/consent"
                headers = {"Content-Type": "application/json"}

                response = requests.post(url, json=payload, headers=headers, timeout=60)
                result = response.json()
                consents = result.get("consents", {})
                st.session_state["no_surgery_prognosis"] = consents.get("prognosis_without_surgery", "")
                st.session_state["alternative_methods"] = consents.get("alternative_treatments", "")
                st.session_state["purpose"] = consents.get("surgery_purpose_necessity_effect", "")
                st.session_state["method_1"] = consents.get("surgery_method_content", {}).get("overall_description", "")
                st.session_state["method_2"] = consents.get("surgery_method_content", {}).get("estimated_duration", "")
                st.session_state["method_3"] = consents.get("surgery_method_content", {}).get("method_change_or_addition", "")
                st.session_state["method_4"] = consents.get("surgery_method_content", {}).get("transfusion_possibility", "")
                st.session_state["method_5"] = consents.get("surgery_method_content", {}).get("surgeon_change_possibility", "")
                st.session_state["complications"] = consents.get("possible_complications_sequelae", "")
                st.session_state["preop_care"] = consents.get("emergency_measures", "")
                st.session_state["mortality_risk"] = consents.get("mortality_risk", "")
                if response.status_code == 200:
                    result = response.json()
                    st.success("수술 동의서가 성공적으로 생성되었습니다!")
                    st.markdown("#### 수술 동의서 본문")
                    st.text_area("동의서", result.get("consent_text", ""), height=400)
                    st.json(result)
                else:
                    st.error(f"수술 동의서 생성 실패: {response.status_code}\n{response.text}")




    

# Navigation handler for POSSUM calculator
    if possum:  
        st.session_state.show_possum = True
        st.rerun()
