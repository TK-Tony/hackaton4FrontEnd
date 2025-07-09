import streamlit as st
from streamlit_drawable_canvas import st_canvas
import json
from datetime import date, datetime

# ──────────────────────────────
# 0. Session-state helpers
# ──────────────────────────────
def get_form_data() -> dict:
    """page_basic_info 단계에서 저장된 폼 원본"""
    return st.session_state.get("form_data", {})


def get_patient_info() -> dict:
    """page_basic_info 단계에서 저장된 요약 정보"""
    return st.session_state.get("patient_info", {})


def get_display_value(session_key: str,
                      info_key: str,
                      patient_info: dict,
                      form_data: dict) -> str:
    """
    ① st.session_state → ② form_data → ③ patient_info
    순서로 값 검색 후 반환
    """
    if st.session_state.get(session_key):
        return st.session_state[session_key]
    if form_data.get(session_key):
        return form_data[session_key]
    return patient_info.get(info_key, '')

# ──────────────────────────────
# 1. Canvas counter helpers
# ──────────────────────────────
def add_canvas(section_idx, sub_idx=None):
    key = f"canvas_count_{section_idx}_{sub_idx}" if sub_idx else f"canvas_count_{section_idx}"
    st.session_state[key] = st.session_state.get(key, 0) + 1


def delete_canvas(section_idx, canvas_idx, sub_idx=None):
    key = f"canvas_count_{section_idx}_{sub_idx}" if sub_idx else f"canvas_count_{section_idx}"
    if st.session_state.get(key, 0) > 0:
        st.session_state[key] -= 1

# ──────────────────────────────
# 2. Formatting helpers
# ──────────────────────────────
def format_medical_staff(fd: dict) -> list[dict]:
    rows = []
    for i in range(1, 4):
        op  = fd.get(f"operator_{i}", "").strip()
        dpt = fd.get(f"department_{i}", "").strip()
        spc = fd.get(f"specialist_{i}", "전문의")
        if op and dpt:
            rows.append({"집도의": op, "전문의여부": spc, "진료과목": dpt})
    return rows


def yes_no(raw: str) -> str:
    return "있음" if str(raw).lower() in {"유", "true", "y", "yes"} else "없음"


def format_patient_conditions(fd: dict) -> dict:
    return {
        '과거병력': yes_no(fd.get('past_history', '')),
        '당뇨병': yes_no(fd.get('diabetes', '')),
        '흡연유무': yes_no(fd.get('smoking', '')),
        '고혈압': yes_no(fd.get('hypertension', '')),
        '알레르기': yes_no(fd.get('allergy', '')),
        '저혈압': yes_no(fd.get('hypotension', '')),
        '기도이상': yes_no(fd.get('airway_abnormality', '')),
        '심혈관질환': yes_no(fd.get('cardiovascular', '')),
        '호흡기질환': yes_no(fd.get('respiratory', '')),
        '혈액응고 질환': yes_no(fd.get('coagulation', '')),
        '복용약물': yes_no(fd.get('medications', '')),
        '신장질환': yes_no(fd.get('renal', '')),
        '마약복용 혹은 약물사고': yes_no(fd.get('drug_abuse', '')),
        '기타': fd.get('other', '')
    }

# ──────────────────────────────
# 3. Save canvas data
# ──────────────────────────────
def _to_serializable(obj):
    """date/datetime → ISO 문자열, 그 외는 그대로"""
    if isinstance(obj, (date, datetime)):
        return obj.isoformat()
    if isinstance(obj, dict):
        return {k: _to_serializable(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_to_serializable(v) for v in obj]
    return obj

def save_all_canvas_data() -> bool:
    canvas_data = {
        'patient_info': get_patient_info(),
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

    for k, v in st.session_state.items():
        if k.startswith("canvas_count_"):
            canvas_data['canvas_counts'][k] = v
        elif k.startswith("canvas_") and not k.startswith("canvas_count_"):
            if hasattr(v, "json_data") and v.json_data:
                canvas_data['canvas_drawings'][k] = v.json_data
            if hasattr(v, "image_data") and v.image_data is not None:
                canvas_data['canvas_images'][k] = v.image_data.tolist()

    safe_data = _to_serializable(canvas_data)

    try:
        filename = f"consent_form_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(safe_data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        st.error(f"데이터 저장 실패: {e}")
        return False

# ──────────────────────────────
# 5. Main page
# ──────────────────────────────
def page_confirmation():
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
    
    st.markdown("""
        <h2 style='text-align:center; color:#176d36; padding-top:0px; margin: 0 0 20px 0'>
        앞서 작성한 모든 정보입니다. 환자 숙지 후 서명을 부탁드립니다.
        </h2>
    """, unsafe_allow_html=True)

    patient_info = get_patient_info()
    form_data = get_form_data()

    # ── 기존 표/레이아웃 유지 ──
    col1, col2, col3 = st.columns([1, 4, 1])
    with col2:
        registration_no = get_display_value('registration_no', '등록번호', patient_info, form_data)
        patient_name    = get_display_value('patient_name', '환자명', patient_info, form_data)
        surgery_name    = get_display_value('surgery_name', '수술명',   patient_info, form_data)

        age    = form_data.get('age',    patient_info.get('나이', ''))
        gender = form_data.get('gender', patient_info.get('성별', ''))
        age_gender = f"{age}/{gender}" if age and gender else patient_info.get('나이/성별', '')

        scheduled_date = form_data.get('scheduled_date', patient_info.get('시행예정일', ''))
        if hasattr(scheduled_date, 'strftime'):
            scheduled_date = scheduled_date.strftime('%Y-%m-%d')

        diagnosis           = get_display_value('diagnosis',           '진단명',      patient_info, form_data)
        surgical_site_mark  = get_display_value('surgical_site_mark',  '수술부위표시', patient_info, form_data)
        surgical_site_detail= form_data.get('surgical_site_detail', patient_info.get('수술부위', ''))

        # 상단 요약 표
        st.markdown(f"""
        <table style="width:100%; border-collapse:collapse; margin-bottom:12px;">
        <tr><th style="border:1px solid #aaa; padding:7px;">등록번호</th>
            <td style="border:1px solid #aaa; padding:7px;">{registration_no}</td>
            <th style="border:1px solid #aaa; padding:7px;">환자명</th>
            <td style="border:1px solid #aaa; padding:7px;">{patient_name}</td></tr>
        <tr><th style="border:1px solid #aaa; padding:7px;">수술명</th>
            <td style="border:1px solid #aaa; padding:7px;" colspan="3">{surgery_name}</td></tr>
        <tr><th style="border:1px solid #aaa; padding:7px;">나이/성별</th>
            <td style="border:1px solid #aaa; padding:7px;">{age_gender}</td>
            <th style="border:1px solid #aaa; padding:7px;">시행예정일</th>
            <td style="border:1px solid #aaa; padding:7px;">{scheduled_date}</td></tr>
        <tr><th style="border:1px solid #aaa; padding:7px;">진단명</th>
            <td style="border:1px solid #aaa; padding:7px;" colspan="3">{diagnosis}</td></tr>
        <tr><th style="border:1px solid #aaa; padding:7px;">수술부위표시</th>
            <td style="border:1px solid #aaa; padding:7px;">{surgical_site_mark}</td>
            <th style="border:1px solid #aaa; padding:7px;">수술부위</th>
            <td style="border:1px solid #aaa; padding:7px;">{surgical_site_detail}</td></tr>
        </table>
        """, unsafe_allow_html=True)

        # ── 참여 의료진 표 ──
        st.markdown("<b>※ 참여 의료진</b>", unsafe_allow_html=True)
        medical_staff = format_medical_staff(form_data) or patient_info.get('의료진', [])
        doctor_rows = "".join(
            f"<tr><td style='border:1px solid #aaa; padding:7px;'>{doc['집도의']}</td>"
            f"<td style='border:1px solid #aaa; padding:7px;'>{doc['전문의여부']}</td>"
            f"<td style='border:1px solid #aaa; padding:7px;'>{doc['진료과목']}</td></tr>"
            for doc in medical_staff
        )
        st.markdown(f"""
        <table style="width:100%; border-collapse:collapse; margin-bottom:12px;">
        <tr><th style="border:1px solid #aaa; padding:7px;">집도의</th>
            <th style="border:1px solid #aaa; padding:7px;">전문의여부</th>
            <th style="border:1px solid #aaa; padding:7px;">진료과목</th></tr>
        {doctor_rows}
        </table>
        """, unsafe_allow_html=True)

        # ── 환자 특이사항 표 ──
        st.markdown("<b>1. 환자 상태 및 특이사항</b>", unsafe_allow_html=True)
        patient_conditions = format_patient_conditions(form_data)
        pc_rows = "".join(
            f"<tr><th style='border:1px solid #aaa; padding:7px;'>{k}</th>"
            f"<td style='border:1px solid #aaa; padding:7px;'>{v}</td></tr>"
            for k, v in patient_conditions.items()
        )
        st.markdown(f"""
        <table style="width:100%; border-collapse:collapse; margin-bottom:12px;">
        {pc_rows}
        </table>
        """, unsafe_allow_html=True)

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

        for title, key, section_idx in sections:
            st.markdown(f"### {title}")

            if key:                         # 2·3·4·6·7·8
                st.markdown(st.session_state.get(key, ""))

            else:                           # 5번 다단
                subsections = [
                    ("1) 수술 과정 전반에 대한 설명", "method_1", 1),
                    ("2) 수술 추정 소요시간",       "method_2", 2),
                    ("3) 수술 변경 및 수술 추가 가능성", "method_3", 3),
                    ("4) 수혈 가능성",              "method_4", 4),
                    ("5) 집도의 변경 가능성",       "method_5", 5),
                ]

                for sub_title, sub_key, sub_idx in subsections:
                    st.markdown(f"**{sub_title}**")

                    # 5-3 · 5-5 → 고정 문구만, 나머지는 세션 값 사용
                    if sub_idx in (3, 5):
                        if sub_idx == 3:
                            st.markdown("""
        > 수술/시술/검사과정에서 환자의 상태에 따라 부득이하게 수술/시술/검사방법이 변경되거나
        > 수술/시술/검사범위가 추가될 수 있습니다.<br>
        > 이 경우, 환자 또는 대리인에게 추가로 설명하여야 하는 사항이 있는 경우에는
        > 수술/시술/검사의 시행 전에 이에 대하여 설명하고 동의를 얻도록 합니다.<br>
        > 다만, 수술/시술/검사의 시행 도중에 환자의 상태에 따라
        > 미리 설명하고 동의를 얻을 수 없을 정도로 긴급한 변경 또는 추가가 요구되는 경우에는<br>
        > 시행 후에 지체 없이 그 사유 및 결과를 환자 또는 대리인에게 설명하도록 합니다.
        """, unsafe_allow_html=True)
                        else:  # sub_idx == 5
                            st.markdown("""
        > 위에 기재된 참여 의료진이 있는 경우 수술/시술/검사과정에서
        > 환자의 상태 또는 의료기관의 사정(응급환자 진료, 주치의의 질병·출장 등)에 따라
        > 부득이하게 주치의(집도의)가 변경될 수 있습니다. 이 경우 시행 전에
        > 환자 또는 대리인에게 구체적인 변경사유를 설명하고 동의를 얻을 예정입니다.<br>
        > 다만, 시행 도중에 미리 설명하고 동의를 얻을 수 없을 정도로 긴급한 변경이 요구되는 경우에는
        > 시행 후에 지체 없이 구체적인 변경 사유 및 시행결과를 환자 또는 대리인에게 설명하도록 합니다.
        """, unsafe_allow_html=True)
                    else:
                        st.markdown(st.session_state.get(sub_key, ""))

            # Canvas add/delete & 구분선은 기존 로직 그대로
            if st.button("Add Canvas", key=f"add_canvas_{section_idx}"):
                add_canvas(section_idx)

            for i in range(st.session_state.get(f"canvas_count_{section_idx}", 0)):
                colA, colB = st.columns([1, 10])
                with colA:
                    if st.button("🗑️", key=f"del_cv_{section_idx}_{i}"):
                        delete_canvas(section_idx, i)
                with colB:
                    result = st_canvas(
                        fill_color="#fff", stroke_width=3, stroke_color="#222",
                        background_color="#f9f9f9", height=200, width=750,
                        drawing_mode="freedraw", key=f"canvas_{section_idx}_{i}"
                    )
                    if result.json_data:
                        st.session_state[f"canvas_{section_idx}_{i}_data"] = result.json_data
                    if result.image_data is not None:
                        st.session_state[f"canvas_{section_idx}_{i}_image"] = result.image_data
            st.divider()



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

        # ▼ 신규 : 서명용 캔버스(1개 고정) ‑ 첫 진입 시 자동 생성
        if "canvas_count_signature" not in st.session_state:
            st.session_state.canvas_count_signature = 1     # 서명 칸 1개

        sig_key = "canvas_signature_0"
        canvas_result = st_canvas(
            fill_color="#fff",
            stroke_width=3,
            stroke_color="#222",
            background_color="#f9f9f9",
            height=200,
            width=750,
            drawing_mode="freedraw",
            key=sig_key
        )
        # 그린 내용 세션에 저장
        if canvas_result.json_data:
            st.session_state[f"{sig_key}_data"] = canvas_result.json_data
        if canvas_result.image_data is not None:
            st.session_state[f"{sig_key}_image"] = canvas_result.image_data

        st.divider()

        if st.button("수술 동의서 PDF 출력하기"):
            if save_all_canvas_data():
                st.success("저장 완료! PDF 생성 페이지로 이동합니다.")
                st.session_state.step =4
            else:
                st.error("데이터 저장에 실패했습니다. 다시 시도해 주세요.")

# ──────────────────────────────
if __name__ == "__main__":
    page_confirmation()
