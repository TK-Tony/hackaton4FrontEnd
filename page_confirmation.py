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
        st.success(f"데이터가 {filename}에 저장되었습니다.")
        return True
    except Exception as e:
        st.error(f"데이터 저장 실패: {e}")
        return False

def page_confirmation():
    consent_data = load_patient_data()
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
        # Patient & Surgery Info Table
        st.markdown(f"""
        <table style="width:100%; border-collapse:collapse; margin-bottom:12px;">
        <tr>
            <th style="border:1px solid #aaa; padding:7px;">등록번호</th>
            <td style="border:1px solid #aaa; padding:7px;">{consent_data.get('등록번호','')}</td>
            <th style="border:1px solid #aaa; padding:7px;">환자명</th>
            <td style="border:1px solid #aaa; padding:7px;">{consent_data.get('환자명','')}</td>
        </tr>
        <tr>
            <th style="border:1px solid #aaa; padding:7px;">수술명</th>
            <td style="border:1px solid #aaa; padding:7px;" colspan="3">{consent_data.get('수술명','')}</td>
        </tr>
        <tr>
            <th style="border:1px solid #aaa; padding:7px;">나이/성별</th>
            <td style="border:1px solid #aaa; padding:7px;">{consent_data.get('나이/성별','')}</td>
            <th style="border:1px solid #aaa; padding:7px;">시행예정일</th>
            <td style="border:1px solid #aaa; padding:7px;">{consent_data.get('시행예정일','')}</td>
        </tr>
        <tr>
            <th style="border:1px solid #aaa; padding:7px;">진단명</th>
            <td style="border:1px solid #aaa; padding:7px;" colspan="3">{consent_data.get('진단명','')}</td>
        </tr>
        <tr>
            <th style="border:1px solid #aaa; padding:7px;">수술부위표시</th>
            <td style="border:1px solid #aaa; padding:7px;">{consent_data.get('수술부위표시','')}</td>
            <th style="border:1px solid #aaa; padding:7px;">수술부위</th>
            <td style="border:1px solid #aaa; padding:7px;">{consent_data.get('수술부위','')}</td>
        </tr>
        </table>
        """, unsafe_allow_html=True)

        # Medical staff
        st.markdown("<b>※ 참여 의료진</b>", unsafe_allow_html=True)

        doctor_rows = ""
        for doc in consent_data.get('의료진', []):
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

        # Section 1: 환자 상태 및 특이사항 (table)
        st.markdown("<b>1. 환자 상태 및 특이사항</b>", unsafe_allow_html=True)
        st.markdown(f"""
        <table style="width:100%; border-collapse:collapse; margin-bottom:12px;">
        <tr>
            <th style="border:1px solid #aaa; padding:7px;">과거병력</th>
            <td style="border:1px solid #aaa; padding:7px;">{consent_data.get('과거병력','')}</td>
            <th style="border:1px solid #aaa; padding:7px;">당뇨병</th>
            <td style="border:1px solid #aaa; padding:7px;">{consent_data.get('당뇨병','')}</td>
        </tr>
        <tr>
            <th style="border:1px solid #aaa; padding:7px;">흡연유무</th>
            <td style="border:1px solid #aaa; padding:7px;">{consent_data.get('흡연유무','')}</td>
            <th style="border:1px solid #aaa; padding:7px;">고혈압</th>
            <td style="border:1px solid #aaa; padding:7px;">{consent_data.get('고혈압','')}</td>
        </tr>
        <tr>
            <th style="border:1px solid #aaa; padding:7px;">알레르기</th>
            <td style="border:1px solid #aaa; padding:7px;">{consent_data.get('알레르기','')}</td>
            <th style="border:1px solid #aaa; padding:7px;">저혈압</th>
            <td style="border:1px solid #aaa; padding:7px;">{consent_data.get('저혈압','')}</td>
        </tr>
        <tr>
            <th style="border:1px solid #aaa; padding:7px;">기도이상</th>
            <td style="border:1px solid #aaa; padding:7px;">{consent_data.get('기도이상','')}</td>
            <th style="border:1px solid #aaa; padding:7px;">심혈관질환</th>
            <td style="border:1px solid #aaa; padding:7px;">{consent_data.get('심혈관질환','')}</td>
        </tr>
        <tr>
            <th style="border:1px solid #aaa; padding:7px;">호흡기질환</th>
            <td style="border:1px solid #aaa; padding:7px;">{consent_data.get('호흡기질환','')}</td>
            <th style="border:1px solid #aaa; padding:7px;">혈액응고 관련 질환</th>
            <td style="border:1px solid #aaa; padding:7px;">{consent_data.get('혈액응고 관련 질환','')}</td>
        </tr>
        <tr>
            <th style="border:1px solid #aaa; padding:7px;">복용약물</th>
            <td style="border:1px solid #aaa; padding:7px;">{consent_data.get('복용약물','')}</td>
            <th style="border:1px solid #aaa; padding:7px;">신장질환</th>
            <td style="border:1px solid #aaa; padding:7px;">{consent_data.get('신장질환','')}</td>
        </tr>
        <tr>
            <th style="border:1px solid #aaa; padding:7px;">마약복용 혹은 약물사고</th>
            <td style="border:1px solid #aaa; padding:7px;">{consent_data.get('마약복용 혹은 약물사고','')}</td>
            <th style="border:1px solid #aaa; padding:7px;">기타</th>
            <td style="border:1px solid #aaa; padding:7px;">{consent_data.get('기타','')}</td>
        </tr>
        </table>
        """, unsafe_allow_html=True)

        st.markdown("<b>※ 기타</b>", unsafe_allow_html=True)
        st.markdown(f"{consent_data.get('기타','')}", unsafe_allow_html=True)

        # Section 2
        st.markdown("### 2. 예정된 수술을 하지 않을 경우의 예후")
        st.markdown(st.session_state.get("no_surgery_prognosis", ""))
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
                # Store canvas result in session state for later saving
                if canvas_result.json_data is not None:
                    st.session_state[f"canvas_2_{i}_data"] = canvas_result.json_data
                    print(st.session_state[f"canvas_2_{i}_data"])
                if canvas_result.image_data is not None:
                    st.session_state[f"canvas_2_{i}_image"] = canvas_result.image_data

        st.divider()

        # Section 3
        st.markdown("### 3. 예정된 수술 이외의 시행 가능한 다른 방법")
        st.markdown(st.session_state.get("alternative_methods", ""))

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
        st.markdown(st.session_state.get("purpose", ""))

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
                if st.button(f"🗑️ (Section 5-1, Canvas {i+1})", key=f"delete_canvas_5_1_{i}"):
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
                if st.button(f"🗑️ (Section 5-2, Canvas {i+1})", key=f"delete_canvas_5_2_{i}"):
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
                if st.button(f"🗑️ (Section 5-3, Canvas {i+1})", key=f"delete_canvas_5_3_{i}"):
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
        st.markdown("**5) 진단/수술 관련 사망 위험성**")
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
        st.markdown(st.session_state.get("complications", ""))

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
        st.markdown(st.session_state.get("preop_care", ""))

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
        st.markdown(st.session_state.get("mortality_risk", ""))

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
        confirmation_canvas = st_canvas(
            fill_color="#fff", stroke_width=3, stroke_color="#222",
            background_color="#f9f9f9", height=180, width=800,
            drawing_mode="freedraw", key="confirmation_big_canvas"
        )
        
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("수술 동의서 PDF 출력하기"):
            # Save all canvas data before proceeding
            if save_all_canvas_data():
                st.success("캔버스 데이터가 저장되었습니다.")
                # PDF 생성 전 필요한 데이터 저장
                st.session_state.step = 3
                st.rerun()
            else:
                st.error("데이터 저장에 실패했습니다. 다시 시도해주세요.")
