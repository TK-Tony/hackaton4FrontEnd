import streamlit as st
from streamlit_drawable_canvas import st_canvas
import json
from datetime import datetime

def load_patient_data():
    try:
        with open("patient_data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"데이터 파일을 읽을 수 없습니다: {e}")
        return {}

def get_form_data():
    return st.session_state.get("form_data", {})

def get_display_value(session_key, json_key, consent_data, form_data):
    if session_key in st.session_state and st.session_state[session_key]:
        return st.session_state[session_key]
    if session_key in form_data and form_data[session_key]:
        return form_data[session_key]
    return consent_data.get(json_key, '')

def add_canvas(section_idx, sub_idx=None):
    key = f"canvas_count_{section_idx}_{sub_idx}" if sub_idx is not None else f"canvas_count_{section_idx}"
    if key not in st.session_state:
        st.session_state[key] = 0
    st.session_state[key] += 1

def delete_canvas(section_idx, canvas_idx, sub_idx=None):
    key = f"canvas_count_{section_idx}_{sub_idx}" if sub_idx is not None else f"canvas_count_{section_idx}"
    if key in st.session_state and st.session_state[key] > 0:
        st.session_state[key] -= 1

def format_medical_staff(form_data):
    medical_staff = []
    for i in range(1, 4):
        operator = form_data.get(f"operator_{i}", "").strip()
        specialist = form_data.get(f"specialist_{i}", "전문의")
        department = form_data.get(f"department_{i}", "").strip()
        if operator and department:
            medical_staff.append({
                '집도의': operator,
                '전문의여부': specialist,
                '진료과목': department
            })
    return medical_staff

def format_patient_conditions(form_data):
    conditions = {
        '과거병력': "있음" if form_data.get('past_history') == 'true' else "없음",
        '당뇨병': "있음" if form_data.get('diabetes') == 'true' else "없음",
        '흡연유무': "있음" if form_data.get('smoking') == 'true' else "없음",
        '고혈압': "있음" if form_data.get('hypertension') == 'true' else "없음",
        '알레르기': "있음" if form_data.get('allergy') == 'true' else "없음",
        '저혈압': "있음" if form_data.get('hypotension') == 'true' else "없음",
        '기도이상': "있음" if form_data.get('airway_abnormality') == 'true' else "없음",
        '심혈관질환': "있음" if form_data.get('cardiovascular') == 'true' else "없음",
        '호흡기질환': "있음" if form_data.get('respiratory') == 'true' else "없음",
        '혈액응고 관련 질환': "있음" if form_data.get('coagulation') == 'true' else "없음",
        '복용약물': "있음" if form_data.get('medications') == 'true' else "없음",
        '신장질환': "있음" if form_data.get('renal') == 'true' else "없음",
        '마약복용 혹은 약물사고': "있음" if form_data.get('drug_abuse') == 'true' else "없음",
        '기타': form_data.get('other', '')
    }
    return conditions

def save_all_canvas_data():
    canvas_data = {
        'patient_info': load_patient_data(),
        'form_data': get_form_data(),
        'session_consent_data': {
            'no_surgery_prognosis': st.session_state.get("no_surgery_prognosis", ""),
            'alternative_methods': st.session_state.get("alternative_methods", ""),
            'purpose': st.session_state.get("purpose", ""),
            'method_1': st.session_state.get("method_1", ""),
            'method_2': st.session_state.get("method_2", ""),
            'method_3': st.session_state.get("method_3", ""),
            'method_4': st.session_state.get("method_4", ""),
            'method_5': st.session_state.get("method_5", ""),
            'complications': st.session_state.get("complications", ""),
            'preop_care': st.session_state.get("preop_care", ""),
            'mortality_risk': st.session_state.get("mortality_risk", ""),
        },
        'canvas_counts': {},
        'canvas_drawings': {},
        'canvas_images': {},
        'timestamp': datetime.now().isoformat()
    }
    for key in st.session_state:
        if key.startswith("canvas_count_"):
            canvas_data['canvas_counts'][key] = st.session_state[key]
    for key in st.session_state:
        if key.startswith("canvas_") and not key.startswith("canvas_count_"):
            canvas_obj = st.session_state[key]
            if hasattr(canvas_obj, 'json_data') and canvas_obj.json_data:
                canvas_data['canvas_drawings'][key] = canvas_obj.json_data
            if hasattr(canvas_obj, 'image_data') and canvas_obj.image_data is not None:
                canvas_data['canvas_images'][key] = canvas_obj.image_data.tolist()
    if 'confirmation_big_canvas' in st.session_state:
        confirmation_canvas = st.session_state['confirmation_big_canvas']
        if hasattr(confirmation_canvas, 'json_data') and confirmation_canvas.json_data:
            canvas_data['canvas_drawings']['confirmation_signature'] = confirmation_canvas.json_data
        if hasattr(confirmation_canvas, 'image_data') and confirmation_canvas.image_data is not None:
            canvas_data['canvas_images']['confirmation_signature'] = confirmation_canvas.image_data.tolist()
    try:
        filename = f"consent_form_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(canvas_data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        st.error(f"데이터 저장 실패: {e}")
        return False

def get_latest_llm_output():
    messages = st.session_state.get("messages", [])
    for msg in reversed(messages):
        if msg.get("role") == "assistant":
            return msg.get("content", "")
    return ""

def page_confirmation():
    consent_data = load_patient_data()
    form_data = get_form_data()
    st.markdown("""
        <style>
        .block-container {
            padding: 0rem;
            max-width: 100% !important;
            padding-bottom: 2rem;
        }
        .form-wrapper {
            max-width: 800px;
            margin-left: 10px;
            margin-right: 10px;
            padding-bottom: 0rem;
        }
        </style>
    """, unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 4, 1])
    with col2:
        registration_no = get_display_value('registration_no', '등록번호', consent_data, form_data)
        patient_name = get_display_value('patient_name', '환자명', consent_data, form_data)
        surgery_name = get_display_value('surgery_name', '수술명', consent_data, form_data)
        age = form_data.get('age', consent_data.get('나이', ''))
        gender = form_data.get('gender', consent_data.get('성별', ''))
        age_gender = f"{age}/{gender}" if age and gender else consent_data.get('나이/성별', '')
        scheduled_date = form_data.get('scheduled_date', consent_data.get('시행예정일', ''))
        if hasattr(scheduled_date, 'strftime'):
            scheduled_date = scheduled_date.strftime('%Y-%m-%d')
        diagnosis = get_display_value('diagnosis', '진단명', consent_data, form_data)
        surgical_site_mark = get_display_value('surgical_site_mark', '수술부위표시', consent_data, form_data)
        surgical_site_detail = form_data.get('surgical_site_detail', consent_data.get('수술부위', ''))
        st.markdown(f"""
        <table style="width:100%; border-collapse:collapse; margin-bottom:12px;">
        <tr>
            <th style="border:1px solid #aaa; padding:7px;">등록번호</th>
            <td style="border:1px solid #aaa; padding:7px;">{registration_no}</td>
            <th style="border:1px solid #aaa; padding:7px;">환자명</th>
            <td style="border:1px solid #aaa; padding:7px;">{patient_name}</td>
        </tr>
        <tr>
            <th style="border:1px solid #aaa; padding:7px;">수술명</th>
            <td style="border:1px solid #aaa; padding:7px;" colspan="3">{surgery_name}</td>
        </tr>
        <tr>
            <th style="border:1px solid #aaa; padding:7px;">나이/성별</th>
            <td style="border:1px solid #aaa; padding:7px;">{age_gender}</td>
            <th style="border:1px solid #aaa; padding:7px;">시행예정일</th>
            <td style="border:1px solid #aaa; padding:7px;">{scheduled_date}</td>
        </tr>
        <tr>
            <th style="border:1px solid #aaa; padding:7px;">진단명</th>
            <td style="border:1px solid #aaa; padding:7px;" colspan="3">{diagnosis}</td>
        </tr>
        <tr>
            <th style="border:1px solid #aaa; padding:7px;">수술부위표시</th>
            <td style="border:1px solid #aaa; padding:7px;">{surgical_site_mark}</td>
            <th style="border:1px solid #aaa; padding:7px;">수술부위</th>
            <td style="border:1px solid #aaa; padding:7px;">{surgical_site_detail}</td>
        </tr>
        </table>
        """, unsafe_allow_html=True)
        st.markdown("<b>※ 참여 의료진</b>", unsafe_allow_html=True)
        medical_staff = format_medical_staff(form_data)
        if not medical_staff:
            medical_staff = consent_data.get('의료진', [])
        doctor_rows = ""
        for doc in medical_staff:
            doctor_rows += (
                f"<tr>"
                f"<td style='border:1px solid #aaa; padding:7px;'>{doc.get('집도의','')}</td>"
                f"<td style='border:1px solid #aaa; padding:7px;'>{doc.get('전문의여부','')}</td>"
                f"<td style='border:1px solid #aaa; padding:7px;'>{doc.get('진료과목','')}</td>"
                f"</tr>"
            )
        st.markdown(f"""
        <table style="width:100%; border-collapse:collapse; margin-bottom:12px;">
        <tr>
            <th style="border:1px solid #aaa; padding:7px;">집도의</th>
            <th style="border:1px solid #aaa; padding:7px;">전문의여부</th>
            <th style="border:1px solid #aaa; padding:7px;">진료과목</th>
        </tr>
        {doctor_rows}
        </table>
        """, unsafe_allow_html=True)
        st.markdown("<b>1. 환자 상태 및 특이사항</b>", unsafe_allow_html=True)
        patient_conditions = format_patient_conditions(form_data)
        for key in patient_conditions:
            if not patient_conditions[key] or patient_conditions[key] == "없음":
                patient_conditions[key] = consent_data.get(key, "없음")
        st.markdown(f"""
        <table style="width:100%; border-collapse:collapse; margin-bottom:12px;">
        <tr>
            <th style="border:1px solid #aaa; padding:7px;">과거병력</th>
            <td style="border:1px solid #aaa; padding:7px;">{patient_conditions['과거병력']}</td>
            <th style="border:1px solid #aaa; padding:7px;">당뇨병</th>
            <td style="border:1px solid #aaa; padding:7px;">{patient_conditions['당뇨병']}</td>
        </tr>
        <tr>
            <th style="border:1px solid #aaa; padding:7px;">흡연유무</th>
            <td style="border:1px solid #aaa; padding:7px;">{patient_conditions['흡연유무']}</td>
            <th style="border:1px solid #aaa; padding:7px;">고혈압</th>
            <td style="border:1px solid #aaa; padding:7px;">{patient_conditions['고혈압']}</td>
        </tr>
        <tr>
            <th style="border:1px solid #aaa; padding:7px;">알레르기</th>
            <td style="border:1px solid #aaa; padding:7px;">{patient_conditions['알레르기']}</td>
            <th style="border:1px solid #aaa; padding:7px;">저혈압</th>
            <td style="border:1px solid #aaa; padding:7px;">{patient_conditions['저혈압']}</td>
        </tr>
        <tr>
            <th style="border:1px solid #aaa; padding:7px;">기도이상</th>
            <td style="border:1px solid #aaa; padding:7px;">{patient_conditions['기도이상']}</td>
            <th style="border:1px solid #aaa; padding:7px;">심혈관질환</th>
            <td style="border:1px solid #aaa; padding:7px;">{patient_conditions['심혈관질환']}</td>
        </tr>
        <tr>
            <th style="border:1px solid #aaa; padding:7px;">호흡기질환</th>
            <td style="border:1px solid #aaa; padding:7px;">{patient_conditions['호흡기질환']}</td>
            <th style="border:1px solid #aaa; padding:7px;">혈액응고 관련 질환</th>
            <td style="border:1px solid #aaa; padding:7px;">{patient_conditions['혈액응고 관련 질환']}</td>
        </tr>
        <tr>
            <th style="border:1px solid #aaa; padding:7px;">복용약물</th>
            <td style="border:1px solid #aaa; padding:7px;">{patient_conditions['복용약물']}</td>
            <th style="border:1px solid #aaa; padding:7px;">신장질환</th>
            <td style="border:1px solid #aaa; padding:7px;">{patient_conditions['신장질환']}</td>
        </tr>
        <tr>
            <th style="border:1px solid #aaa; padding:7px;">마약복용 혹은 약물사고</th>
            <td style="border:1px solid #aaa; padding:7px;">{patient_conditions['마약복용 혹은 약물사고']}</td>
            <th style="border:1px solid #aaa; padding:7px;">기타</th>
            <td style="border:1px solid #aaa; padding:7px;">{patient_conditions['기타']}</td>
        </tr>
        </table>
        """, unsafe_allow_html=True)
        st.markdown("<b>※ 기타</b>", unsafe_allow_html=True)
        st.markdown(patient_conditions['기타'], unsafe_allow_html=True)
        # --- Consent Content Sections ---
        sections = [
            ("2. 예정된 수술을 하지 않을 경우의 예후", "no_surgery_prognosis", 2),
            ("3. 예정된 수술 이외의 시행 가능한 다른 방법", "alternative_methods", 3),
            ("4. 수술의 목적/필요성/효과", "purpose", 4),
            ("5. 수술의 방법 및 내용", None, None),
            ("6. 발생 가능한 합병증/후유증/부작용", "complications", 6),
            ("7. 문제 발생시 조치사항", "preop_care", 7),
            ("8. 진단/수술 관련 사망 위험성", "mortality_risk", 8),
        ]
        for title, key, canvas_section in sections:
            st.markdown(f"### {title}")
            if key:
                st.markdown(st.session_state.get(key, ""))
            elif title.startswith("5."):
                subsections = [
                    ("1) 수술 과정 전반에 대한 설명", "method_1", 5, 1),
                    ("2) 수술 추정 소요시간", "method_2", 5, 2),
                    ("3) 수술 변경 및 수술 추가 가능성", "method_3", 5, 3),
                    ("4) 수혈 가능성", "method_4", 5, 4),
                    ("5) 집도의 변경 가능성", "method_5", 5, 5),
                ]
                for sub_title, sub_key, sec_idx, sub_idx in subsections:
                    st.markdown(f"**{sub_title}**")
                    st.markdown(st.session_state.get(sub_key, ""))
                    if sub_idx == 3:
                        st.markdown("""
                        > 수술/시술/검사과정에서 환자의 상태에 따라 부득이하게 수술/시술/검사방법이 변경되거나 수술/시술/검사범위가 추가될 수 있습니다.<br>
                        > 이 경우, 환자 또는 대리인에게 추가로 설명하여야 하는 사항이 있는 경우에는 수술/시술/검사의 시행 전에 이에 대하여 설명하고 동의를 얻도록 합니다.<br>
                        > 다만, 수술/시술/검사의 시행 도중에 환자의 상태에 따라 미리 설명하고 동의를 얻을 수 없을 정도로 긴급한 변경 또는 추가가 요구되는 경우에는<br>
                        > 시행 후에 지체 없이 그 사유 및 결과를 환자 또는 대리인에게 설명하도록 합니다.
                        """, unsafe_allow_html=True)
                    elif sub_idx == 5:
                        st.markdown("""
                        > 위에 기재된 참여 의료진이 있는 경우 수술/시술/검사과정에서 환자의 상태 또는 의료기관의 사정(응급환자 진료, 주치의의 질병·출장 등)에 따라<br>
                        > 부득이하게 주치의(집도의)가 변경될 수 있습니다. 이 경우 시행 전에 환자 또는 대리인에게 구체적인 변경사유를 설명하고 동의를 얻을 예정입니다.<br>
                        > 다만, 시행 도중에 미리 설명하고 동의를 얻을 수 없을 정도로 긴급한 변경이 요구되는 경우에는 시행 후에<br>
                        > 지체 없이 구체적인 변경 사유 및 시행결과를 환자 또는 대리인에게 설명하도록 합니다.
                        """, unsafe_allow_html=True)
            st.divider()
        # --- LLM Output Section ---
        llm_output = get_latest_llm_output()
        if llm_output:
            st.markdown("### AI 보조 설명")
            st.markdown(llm_output)
        # --- Signature and Confirmation Section ---
        st.markdown("### 수술 동의서 확인")
        st.markdown("""
        아래 내용을 읽고 동의해 주세요.

        1. 나는 수술/시술/검사의 목적, 효과, 과정, 예상되는 위험에 대해 설명을 들었습니다.
        2. 궁금한 점을 의료진에게 질문할 수 있었고, 충분히 생각할 시간을 가졌습니다.
        3. 예상치 못한 합병증이나 사고가 생길 수 있음을 이해합니다.
        4. 수술/시술/검사에 협조하고, 내 상태를 정확히 알릴 것을 약속합니다.
        5. 수술 방법이나 범위가 바뀔 수 있다는 설명을 들었습니다.
        6. 담당의사가 바뀔 수 있다는 설명을 들었습니다.
        7. 일정이 바뀔 수 있음을 이해합니다.
        """)
        st.markdown("**추가 정보/서명란 (필요시 담당의 입력)**")
        if st.button("Add Canvas", key="add_canvas_9"):
            add_canvas(9)
        for i in range(st.session_state.get("canvas_count_9", 0)):
            col1, col2 = st.columns([1, 10])
            with col1:
                if st.button(f"🗑️", key=f"delete_canvas_9_{i}"):
                    delete_canvas(9, i)
                    st.experimental_rerun()
            with col2:
                canvas_result = st_canvas(
                    fill_color="#fff", stroke_width=3, stroke_color="#222",
                    background_color="#f9f9f9", height=200, width=750,
                    drawing_mode="freedraw", key=f"canvas_9_{i}"
                )
                if canvas_result.json_data is not None:
                    st.session_state[f"canvas_9_{i}_data"] = canvas_result.json_data
                if canvas_result.image_data is not None:
                    st.session_state[f"canvas_9_{i}_image"] = canvas_result.image_data
        st.divider()
        if st.button("수술 동의서 PDF 출력하기", key="special"):
            if save_all_canvas_data():
                from page_pdf_progress import page_pdf_progress
                page_pdf_progress()
                st.session_state.step = 3
                st.experimental_rerun()
            else:
                st.error("데이터 저장에 실패했습니다. 다시 시도해주세요.")
