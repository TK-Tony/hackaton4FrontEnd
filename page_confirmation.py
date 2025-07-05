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
    """Get form data from session state with fallbacks"""
    return st.session_state.get("form_data", {})

def get_display_value(session_key, json_key, consent_data, form_data):
    """Get display value with priority: session_state -> form_data -> json_data"""
    # First try session state
    if session_key in st.session_state and st.session_state[session_key]:
        return st.session_state[session_key]
    
    # Then try form data
    if session_key in form_data and form_data[session_key]:
        return form_data[session_key]
    
    # Finally try JSON data
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

def save_all_canvas_data():
    """Save all canvas data including counts and drawing content"""
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
    
    # Save canvas counts
    for key in st.session_state:
        if key.startswith("canvas_count_"):
            canvas_data['canvas_counts'][key] = st.session_state[key]
    
    # Save canvas drawing data and images
    for key in st.session_state:
        if key.startswith("canvas_") and not key.startswith("canvas_count_"):
            canvas_obj = st.session_state[key]
            if hasattr(canvas_obj, 'json_data') and canvas_obj.json_data:
                canvas_data['canvas_drawings'][key] = canvas_obj.json_data
            if hasattr(canvas_obj, 'image_data') and canvas_obj.image_data is not None:
                canvas_data['canvas_images'][key] = canvas_obj.image_data.tolist()
    
    # Save confirmation canvas
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

def format_medical_staff(form_data):
    """Format medical staff data from form_data"""
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
    """Format patient conditions from form_data"""
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

def page_confirmation():
    # Load data from multiple sources
    consent_data = load_patient_data()
    form_data = get_form_data()
    
    # 여백 제거 및 container 최대 폭 확장
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
    
    # Create columns to center the content
    col1, col2, col3 = st.columns([1, 4, 1])
    with col2:  # Place all content in the middle column
        # Patient & Surgery Info Table - Use form_data with fallbacks
        registration_no = get_display_value('registration_no', '등록번호', consent_data, form_data)
        patient_name = get_display_value('patient_name', '환자명', consent_data, form_data)
        surgery_name = get_display_value('surgery_name', '수술명', consent_data, form_data)
        
        # Format age and gender
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

        # Medical staff - Use form_data with fallback to JSON
        st.markdown("<b>※ 참여 의료진</b>", unsafe_allow_html=True)
        
        # Try to get medical staff from form_data first
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

        # Section 1: 환자 상태 및 특이사항 - Use form_data with fallback to JSON
        st.markdown("<b>1. 환자 상태 및 특이사항</b>", unsafe_allow_html=True)
        
        # Try to get conditions from form_data first
        patient_conditions = format_patient_conditions(form_data)
        
        # Fallback to JSON data if form_data is empty
        for key, value in patient_conditions.items():
            if not value or value == "없음":
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
        st.markdown(f"{patient_conditions['기타']}", unsafe_allow_html=True)

        # Section 2 - Generated consent content from session state
        st.markdown("### 2. 예정된 수술을 하지 않을 경우의 예후")
        st.markdown("수술을 하지 않으면 에스상결장 천공(대장에 구멍이 남) 때문에 배 안에 세균과 오염물질이 퍼질 수 있습니다. 이렇게 되면 복막염(배 안에 염증이 생기는 병)이 생길 수 있고, 이 병은 생명을 위협할 만큼 위험합니다. 치료하지 않으면 몸에 심한 감염이 생겨서 고열, 혈압 저하, 쇼크 등이 올 수 있습니다. 이런 상태가 계속되면 장기(심장, 신장 등)가 제대로 작동하지 않을 수 있습니다. 특히 면역력이 약한 경우에는 감염이 더 빨리 퍼질 수 있습니다. 젊고 건강해 보여도, 대장에 구멍이 난 상태를 방치하면 회복이 어렵고, 심하면 사망할 수도 있습니다. 약물치료나 관찰만으로는 이 문제를 해결할 수 없습니다. 따라서 수술 없이 두면 위험이 매우 크다고 할 수 있습니다.")
        if st.button("Add Canvas", key="add_canvas_2"):
            add_canvas(2)
        
        for i in range(st.session_state.get("canvas_count_2", 0)):
            col1, col2 = st.columns([1, 10])
            with col1:
                if st.button(f"🗑️", key=f"delete_canvas_2_{i}"):
                    delete_canvas(2, i)
                    st.rerun()
            with col2:
                canvas_result = st_canvas(
                    fill_color="#fff", stroke_width=3, stroke_color="#222",
                    background_color="#f9f9f9", height=200, width=750,
                    drawing_mode="freedraw", key=f"canvas_2_{i}"
                )
                if canvas_result.json_data is not None:
                    st.session_state[f"canvas_2_{i}_data"] = canvas_result.json_data
                if canvas_result.image_data is not None:
                    st.session_state[f"canvas_2_{i}_image"] = canvas_result.image_data

        st.divider()

        # Section 3
        st.markdown("### 3. 예정된 수술 이외의 시행 가능한 다른 방법")
        st.markdown("에스상결장 천공이 있을 때 하트만 수술 외에도 몇 가지 다른 치료 방법이 있습니다. 첫째, 상태가 아주 가벼운 경우에는 항생제 치료와 금식 등으로 경과를 관찰할 수 있지만, 대부분의 경우에는 효과가 제한적입니다. 둘째, 천공 부위가 작고 오염이 심하지 않으면, 에스상결장 절제술(에스상결장 일부를 잘라내는 수술) 후 바로 장을 다시 연결하는 방법도 있습니다. 하지만 이 방법은 감염 위험이 높거나 몸 상태가 좋지 않을 때는 어렵습니다. 셋째, 드물게 배에 관을 삽입해 고름이나 오염된 액체를 빼내는 치료를 시도할 수 있지만, 근본적인 해결이 되지 않아 임시방편일 뿐입니다. 마지막으로, 치료를 하지 않으면 복막염이나 패혈증 등 생명을 위협하는 합병증이 생길 수 있습니다. 각각의 치료 방법은 환자의 상태와 천공의 정도에 따라 선택되며, 담당 의사가 가장 안전하고 효과적인 방법을 권하게 됩니다.")

        if st.button("Add Canvas", key="add_canvas_3"):
            add_canvas(3)
        for i in range(st.session_state.get("canvas_count_3", 0)):
            col1, col2 = st.columns([1, 10])
            with col1:
                if st.button(f"🗑️", key=f"delete_canvas_3_{i}"):
                    delete_canvas(3, i)
                    st.rerun()
            with col2:
                canvas_result = st_canvas(
                    fill_color="#fff", stroke_width=3, stroke_color="#222",
                    background_color="#f9f9f9", height=200, width=750,
                    drawing_mode="freedraw", key=f"canvas_3_{i}"
                )
                if canvas_result.json_data is not None:
                    st.session_state[f"canvas_3_{i}_data"] = canvas_result.json_data
                if canvas_result.image_data is not None:
                    st.session_state[f"canvas_3_{i}_image"] = canvas_result.image_data
        st.divider()

        # Section 4
        st.markdown("### 4. 수술의 목적/필요성/효과")
        st.markdown("하트만 수술은 에스상결장(대장의 일부)에 구멍이 생겨서, 그 부분을 잘라내고 장의 끝을 밖으로 빼내는 수술입니다. 이렇게 구멍이 생기면 배 안에 세균이나 오염물이 퍼져서 생명을 위협할 수 있기 때문에, 빠른 수술이 꼭 필요합니다. 수술을 하지 않으면 복막염이나 심각한 감염이 생길 수 있습니다. 하트만 수술을 하면 오염된 장을 제거하고, 남은 장은 임시로 배 밖으로 연결해 배변이 가능하게 합니다. 이 수술을 통해 감염을 막고, 몸이 회복할 수 있는 시간을 줍니다. 나중에 몸 상태가 좋아지면 다시 장을 연결하는 추가 수술을 할 수 있습니다. 수술 후에는 일시적으로 인공항문(장루)이 필요할 수 있습니다. 이 수술은 생명을 지키기 위한 중요한 치료 방법입니다.")

        if st.button("Add Canvas", key="add_canvas_4"):
            add_canvas(4)
        for i in range(st.session_state.get("canvas_count_4", 0)):
            col1, col2 = st.columns([1, 10])
            with col1:
                if st.button(f"🗑️", key=f"delete_canvas_4_{i}"):
                    delete_canvas(4, i)
                    st.rerun()
            with col2:
                canvas_result = st_canvas(
                    fill_color="#fff", stroke_width=3, stroke_color="#222",
                    background_color="#f9f9f9", height=200, width=750,
                    drawing_mode="freedraw", key=f"canvas_4_{i}"
                )
                if canvas_result.json_data is not None:
                    st.session_state[f"canvas_4_{i}_data"] = canvas_result.json_data
                if canvas_result.image_data is not None:
                    st.session_state[f"canvas_4_{i}_image"] = canvas_result.image_data
        st.divider()

        # Section 5
        st.markdown("### 5. 수술의 방법 및 내용")

        # Subsection 1
        st.markdown("**1) 수술 과정 전반에 대한 설명**")
        st.markdown(st.session_state.get("method_1", ""))

        if st.button("Add Canvas", key="add_canvas_5_1"):
            add_canvas(5, 1)
        for i in range(st.session_state.get("canvas_count_5_1", 0)):
            col1, col2 = st.columns([1, 10])
            with col1:
                if st.button(f"🗑️", key=f"delete_canvas_5_1_{i}"):
                    delete_canvas(5, i, 1)
                    st.rerun()
            with col2:
                canvas_result = st_canvas(
                    fill_color="#fff", stroke_width=3, stroke_color="#222",
                    background_color="#f9f9f9", height=200, width=750,
                    drawing_mode="freedraw", key=f"canvas_5_1_{i}"
                )
                if canvas_result.json_data is not None:
                    st.session_state[f"canvas_5_1_{i}_data"] = canvas_result.json_data
                if canvas_result.image_data is not None:
                    st.session_state[f"canvas_5_1_{i}_image"] = canvas_result.image_data

        # Subsection 2
        st.markdown("**2) 수술 추정 소요시간**")
        st.markdown(st.session_state.get("method_2", ""))

        if st.button("Add Canvas", key="add_canvas_5_2"):
            add_canvas(5, 2)
        for i in range(st.session_state.get("canvas_count_5_2", 0)):
            col1, col2 = st.columns([1, 10])
            with col1:
                if st.button(f"🗑️", key=f"delete_canvas_5_2_{i}"):
                    delete_canvas(5, i, 2)
                    st.rerun()
            with col2:
                canvas_result = st_canvas(
                    fill_color="#fff", stroke_width=3, stroke_color="#222",
                    background_color="#f9f9f9", height=200, width=750,
                    drawing_mode="freedraw", key=f"canvas_5_2_{i}"
                )
                if canvas_result.json_data is not None:
                    st.session_state[f"canvas_5_2_{i}_data"] = canvas_result.json_data
                if canvas_result.image_data is not None:
                    st.session_state[f"canvas_5_2_{i}_image"] = canvas_result.image_data

        # Subsection 3
        st.markdown("**3) 수술 변경 및 수술 추가 가능성**")
        st.markdown(st.session_state.get("method_3", ""))
        st.markdown("""
        > 수술/시술/검사과정에서 환자의 상태에 따라 부득이하게 수술/시술/검사방법이 변경되거나 수술/시술/검사범위가 추가될 수 있습니다.  
        > 이 경우, 환자 또는 대리인에게 추가로 설명하여야 하는 사항이 있는 경우에는 수술/시술/검사의 시행 전에 이에 대하여 설명하고 동의를 얻도록 합니다.  
        > 다만, 수술/시술/검사의 시행 도중에 환자의 상태에 따라 미리 설명하고 동의를 얻을 수 없을 정도로 긴급한 변경 또는 추가가 요구되는 경우에는  
        > 시행 후에 지체 없이 그 사유 및 결과를 환자 또는 대리인에게 설명하도록 합니다.
        """)
        if st.button("Add Canvas", key="add_canvas_5_3"):
            add_canvas(5, 3)
        for i in range(st.session_state.get("canvas_count_5_3", 0)):
            col1, col2 = st.columns([1, 10])
            with col1:
                if st.button(f"🗑️", key=f"delete_canvas_5_3_{i}"):
                    delete_canvas(5, i, 3)
                    st.rerun()
            with col2:
                canvas_result = st_canvas(
                    fill_color="#fff", stroke_width=3, stroke_color="#222",
                    background_color="#f9f9f9", height=200, width=750,
                    drawing_mode="freedraw", key=f"canvas_5_3_{i}"
                )
                if canvas_result.json_data is not None:
                    st.session_state[f"canvas_5_3_{i}_data"] = canvas_result.json_data
                if canvas_result.image_data is not None:
                    st.session_state[f"canvas_5_3_{i}_image"] = canvas_result.image_data

        # Subsection 4
        st.markdown("**4) 수혈 가능성**")
        st.markdown(st.session_state.get("method_4", ""))

        if st.button("Add Canvas", key="add_canvas_5_4"):
            add_canvas(5, 4)
        for i in range(st.session_state.get("canvas_count_5_4", 0)):
            col1, col2 = st.columns([1, 10])
            with col1:
                if st.button(f"🗑️", key=f"delete_canvas_5_4_{i}"):
                    delete_canvas(5, i, 4)
                    st.rerun()
            with col2:
                canvas_result = st_canvas(
                    fill_color="#fff", stroke_width=3, stroke_color="#222",
                    background_color="#f9f9f9", height=200, width=750,
                    drawing_mode="freedraw", key=f"canvas_5_4_{i}"
                )
                if canvas_result.json_data is not None:
                    st.session_state[f"canvas_5_4_{i}_data"] = canvas_result.json_data
                if canvas_result.image_data is not None:
                    st.session_state[f"canvas_5_4_{i}_image"] = canvas_result.image_data

        # Subsection 5
        st.markdown("**5) 집도의 변경 가능성**")
        st.markdown(st.session_state.get("method_5", ""))
        st.markdown("""
        > 위에 기재된 참여 의료진이 있는 경우 수술/시술/검사과정에서 환자의 상태 또는 의료기관의 사정(응급환자 진료, 주치의의 질병·출장 등)에 따라  
        > 부득이하게 주치의(집도의)가 변경될 수 있습니다. 이 경우 시행 전에 환자 또는 대리인에게 구체적인 변경사유를 설명하고 동의를 얻을 예정입니다.  
        > 다만, 시행 도중에 미리 설명하고 동의를 얻을 수 없을 정도로 긴급한 변경이 요구되는 경우에는 시행 후에  
        > 지체 없이 구체적인 변경 사유 및 시행결과를 환자 또는 대리인에게 설명하도록 합니다.
        """)
        if st.button("Add Canvas", key="add_canvas_5_5"):
            add_canvas(5, 5)
        for i in range(st.session_state.get("canvas_count_5_5", 0)):
            col1, col2 = st.columns([1, 10])
            with col1:
                if st.button(f"🗑️", key=f"delete_canvas_5_5_{i}"):
                    delete_canvas(5, i, 5)
                    st.rerun()
            with col2:
                canvas_result = st_canvas(
                    fill_color="#fff", stroke_width=3, stroke_color="#222",
                    background_color="#f9f9f9", height=200, width=750,
                    drawing_mode="freedraw", key=f"canvas_5_5_{i}"
                )
                if canvas_result.json_data is not None:
                    st.session_state[f"canvas_5_5_{i}_data"] = canvas_result.json_data
                if canvas_result.image_data is not None:
                    st.session_state[f"canvas_5_5_{i}_image"] = canvas_result.image_data
        st.divider()

        # Section 6
        st.markdown("### 6. 발생 가능한 합병증/후유증/부작용")
        st.markdown("하트만 수술을 받으면 몇 가지 합병증이 생길 수 있습니다. 수술 부위에 감염이 생기거나, 출혈이 발생할 수 있습니다. 장이 막히거나(장폐색), 남은 장 끝이 잘 아물지 않아 누출이 생길 수도 있습니다. 일시적으로 배에 인공항문(장루)이 만들어지는데, 이 부위에 피부 자극이나 감염이 생길 수 있습니다. 드물게는 주변 장기(예: 방광, 위, 간 등)에 손상이 갈 수 있습니다. 면역력이 약한 경우, 감염 위험이 더 높아질 수 있습니다. 수술 후에는 일시적으로 배가 붓거나, 소화가 잘 안 될 수 있습니다. 아주 드물게는 심장이나 혈관에 문제가 생길 수 있으니, 수술 후 몸 상태를 잘 살펴야 합니다. 모든 합병증은 조기에 발견하면 치료가 가능하니, 이상 증상이 있으면 바로 의료진에게 알려야 합니다.")

        if st.button("Add Canvas", key="add_canvas_6"):
            add_canvas(6)
        for i in range(st.session_state.get("canvas_count_6", 0)):
            col1, col2 = st.columns([1, 10])
            with col1:
                if st.button(f"🗑️", key=f"delete_canvas_6_{i}"):
                    delete_canvas(6, i)
                    st.rerun()
            with col2:
                canvas_result = st_canvas(
                    fill_color="#fff", stroke_width=3, stroke_color="#222",
                    background_color="#f9f9f9", height=200, width=750,
                    drawing_mode="freedraw", key=f"canvas_6_{i}"
                )
                if canvas_result.json_data is not None:
                    st.session_state[f"canvas_6_{i}_data"] = canvas_result.json_data
                if canvas_result.image_data is not None:
                    st.session_state[f"canvas_6_{i}_image"] = canvas_result.image_data
        st.divider()

        # Section 7
        st.markdown("### 7. 문제 발생시 조치사항")
        st.markdown(" 수술 중이나 수술 후에 갑자기 문제가 생기면, 의료진이 바로 응급조치를 하게 됩니다. 예를 들어, 심장이 멈추거나 호흡이 어려워지면 심폐소생술(심장과 폐를 살리는 응급처치)을 시행할 수 있습니다. 출혈이 심하게 발생하면 추가로 지혈이나 수혈이 필요할 수 있습니다. 감염이 생기면 항생제 투여나 추가적인 치료가 필요할 수 있습니다. 드물게 장이나 다른 장기가 손상될 수 있는데, 이 경우 추가 수술이 필요할 수도 있습니다. 심장에 문제가 있는 경우, 심장 모니터링을 하면서 필요한 응급약물이나 처치를 바로 시행합니다. 면역체계에 문제가 있다면 감염 위험이 높으므로, 의료진이 더 신속하게 대응합니다. 모든 응급상황에서는 환자의 안전을 최우선으로 생각하며, 빠르게 적절한 치료를 진행합니다.")

        if st.button("Add Canvas", key="add_canvas_7_1"):
            add_canvas(7, 1)
        for i in range(st.session_state.get("canvas_count_7_1", 0)):
            col1, col2 = st.columns([1, 10])
            with col1:
                if st.button(f"🗑️", key=f"delete_canvas_7_1_{i}"):
                    delete_canvas(7, i, 1)
                    st.rerun()
            with col2:
                canvas_result = st_canvas(
                    fill_color="#fff", stroke_width=3, stroke_color="#222",
                    background_color="#f9f9f9", height=200, width=750,
                    drawing_mode="freedraw", key=f"canvas_7_1_{i}"
                )
                if canvas_result.json_data is not None:
                    st.session_state[f"canvas_7_1_{i}_data"] = canvas_result.json_data
                if canvas_result.image_data is not None:
                    st.session_state[f"canvas_7_1_{i}_image"] = canvas_result.image_data
        st.divider()

        # Section 8
        st.markdown("### 8. 진단/수술 관련 사망 위험성")
        st.markdown("하트만 수술은 에스상결장(대장의 한 부분)에 구멍이 생겼을 때 시행하는 큰 수술입니다. 이 수술로 인해 사망(돌아가실) 위험이 아주 낮지만, 완전히 없지는 않습니다. 현재 건강 상태가 안정적이고, 나이가 젊기 때문에 위험이 더 낮은 편입니다. 하지만 심혈관계(심장과 혈관) 질환이 있어서 수술 중이나 후에 심장 관련 문제가 생길 가능성이 있습니다. 면역 체계에 문제가 있으면 감염 등 합병증 위험도 조금 더 높아질 수 있습니다. 통계적으로 계산된 사망 위험은 0.2% 정도로, 1,000명 중 2명꼴로 매우 낮은 수치입니다. 그래도 수술 전후로 몸 상태가 갑자기 나빠질 수 있으니, 의료진이 계속 주의 깊게 관찰할 예정입니다. 수술 전후로 이상 증상이 있으면 바로 알려주셔야 합니다. 모든 위험을 줄이기 위해 최선을 다하겠습니다.")

        if st.button("Add Canvas", key="add_canvas_8"):
            add_canvas(8)
        for i in range(st.session_state.get("canvas_count_8", 0)):
            col1, col2 = st.columns([1, 10])
            with col1:
                if st.button(f"🗑️", key=f"delete_canvas_8_{i}"):
                    delete_canvas(8, i)
                    st.rerun()
            with col2:
                canvas_result = st_canvas(
                    fill_color="#fff", stroke_width=3, stroke_color="#222",
                    background_color="#f9f9f9", height=200, width=750,
                    drawing_mode="freedraw", key=f"canvas_8_{i}"
                )
                if canvas_result.json_data is not None:
                    st.session_state[f"canvas_8_{i}_data"] = canvas_result.json_data
                if canvas_result.image_data is not None:
                    st.session_state[f"canvas_8_{i}_image"] = canvas_result.image_data
        st.divider()

        # Signature and Confirmation Section
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
                    st.rerun()
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
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("수술 동의서 PDF 출력하기", key="special"):
            # Save all canvas data before proceeding
            if save_all_canvas_data():
                from page_pdf_progress import page_pdf_progress
                page_pdf_progress()               
                st.session_state.step = 3
                st.rerun()
            else:
                st.error("데이터 저장에 실패했습니다. 다시 시도해주세요.")
