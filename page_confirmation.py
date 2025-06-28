import streamlit as st
from streamlit_drawable_canvas import st_canvas
import json

def load_patient_data():
    try:
        with open("patient_data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"데이터 파일을 읽을 수 없습니다: {e}")
        return {}

def delete_canvas(section_idx, canvas_idx):
    """Delete a specific canvas from a section"""
    count_key = f"canvas_count_{section_idx}"
    canvas_data_key = f"canvas_data_{section_idx}"
    
    if count_key in st.session_state and st.session_state[count_key] > 0:
        st.session_state[count_key] -= 1
        
        # Remove canvas data if it exists
        if canvas_data_key not in st.session_state:
            st.session_state[canvas_data_key] = {}
        
        # Shift canvas data to fill the gap
        canvas_data = st.session_state[canvas_data_key]
        new_canvas_data = {}
        
        for i in range(st.session_state[count_key] + 1):
            if i < canvas_idx:
                new_canvas_data[i] = canvas_data.get(i, None)
            elif i > canvas_idx:
                new_canvas_data[i-1] = canvas_data.get(i, None)
        
        st.session_state[canvas_data_key] = new_canvas_data

def page_confirmation():
    consent_data = load_patient_data()

    def gender_str(g):
        return "남" if g == "M" or g == "남" else "여"

    def bool_or_str(val):
        if isinstance(val, bool):
            return "무" if not val else "유"
        if isinstance(val, str) and val.strip():
            return f"유 ({val})" if val != "무" else "무"
        return "무"
    
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

    col1, col2, col3 = st.columns([1, 6, 1])

    with col2:

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
            <td style="border:1px solid #aaa; padding:7px;" colspan="3">{consent_data.get('수술부위표시','')}</td>
        </tr>
        </table>
        """, unsafe_allow_html=True)

        # Medical staff
        st.markdown("<b>※ 참여 의료진</b>", unsafe_allow_html=True)
        st.markdown(f"""
        <table style="width:100%; border-collapse:collapse; margin-bottom:12px;">
        <tr>
            <th style="border:1px solid #aaa; padding:7px;">집도의</th>
            <th style="border:1px solid #aaa; padding:7px;">전문의여부</th>
            <th style="border:1px solid #aaa; padding:7px;">진료과목</th>
        </tr>
        <tr>
            <td style="border:1px solid #aaa; padding:7px;">{consent_data.get('집도의','')}</td>
            <td style="border:1px solid #aaa; padding:7px;">{consent_data.get('전문의여부','')}</td>
            <td style="border:1px solid #aaa; padding:7px;">{consent_data.get('진료과목','')}</td>
        </tr>
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

        # Sections 2~8 with add/delete canvas logic
        sections = [
            ("2. 예정된 수술을 하지 않을 경우의 예후", "예정된 수술을 하지 않을 경우의 예후"),
            ("3. 예정된 수술 이외의 시행 가능한 다른 방법", "예정된 수술 이외의 시행 가능한 다른 방법"),
            ("4. 수술의 목적/필요성/효과", "수술의 목적/필요성/효과"),
            ("5. 수술의 방법 및 내용", "수술의 방법 및 내용"),
            ("6. 발생 가능한 합병증/후유증/부작용", "발생 가능한 합병증/후유증/부작용"),
            ("7. 문제 발생시 조치사항", "문제 발생시 조치사항"),
            ("8. 진단/수술 관련 사망 위험성", "진단/수술 관련 사망 위험성")
        ]
        
        for idx, (title, key) in enumerate(sections, start=2):
            st.markdown(f"<b>{title}</b>", unsafe_allow_html=True)
            st.markdown(f"<div style='border:1px solid #aaa; padding:10px; margin-bottom:12px; min-height: 100px;'>{consent_data.get(key, '')}</div>", unsafe_allow_html=True)
            
            count_key = f"canvas_count_{idx}"
            if count_key not in st.session_state:
                st.session_state[count_key] = 0
            
            # Add canvas button
            col1, col2 = st.columns([1, 4])
            with col1:
                if st.button(f"➕ Add Canvas", key=f"add_canvas_btn_{idx}"):
                    st.session_state[count_key] += 1
                    st.rerun()
            
            # Display existing canvases with delete buttons
            for i in range(st.session_state[count_key]):
                canvas_col1, canvas_col2 = st.columns([1, 10])
                
                with canvas_col1:
                    if st.button(f"🗑️", key=f"delete_canvas_btn_{idx}_{i}", help=f"Delete Canvas {i+1}"):
                        delete_canvas(idx, i)
                        st.rerun()
                
                with canvas_col2:
                    st.markdown(f"<small>Canvas {i+1} for Section {idx}</small>", unsafe_allow_html=True)
                    st_canvas(
                        fill_color="#fff",
                        stroke_width=3,
                        stroke_color="#222",
                        background_color="#f9f9f9",
                        height=200,
                        width=850,
                        drawing_mode="freedraw",
                        key=f"canvas_{idx}_{i}"
                    )

        st.markdown("<h1 style='text-align:center; color:#176d36;'>수술 동의서 확정을 위한 마지막 정보입니다.</h1>", unsafe_allow_html=True)
        st.markdown("""
        <div style="margin: 0 auto; width: 1000px; background: #fff; border-radius: 12px; padding: 36px 36px 24px 36px; box-shadow: 0 0 12px #eee;">
        <div style="font-size:1.1em; margin-bottom:18px;">
        나는 다음의 사항을 확인하고 동의합니다.<br>
        1. 나(또는 환자)에 대한 수술/시술/검사의 목적, 효과, 과정, 예상되는 합병증, 후유증 등에 대한 설명(필요시 별지 포함)을 의료진으로부터 들었음을 확인합니다.<br>
        2. 또한 나는 설명 내용에 대해 의료진에게 추가 질문을 할 수 있는 기회를 가졌으며 설명 후 수술/시술/검사에 동의하기까지 충분한 시간을 가졌음을 확인합니다.<br>
        3. 이 수술/시술/검사로서 불가항력적으로 야기될 수 있는 합병증 또는 환자의 특이체질로 예상치 못한 사고가 생길 수 있다는 점을 이해하였음을 확인합니다.<br>
        4. 이 수술/시술/검사에 협력하고, 환자의 현재 상태에 대해 성실하게 고지할 것을 서약하며, 이에 따른 의학적 처리를 주치의의 판단에 따라 수술/시술/검사를 하는 데에 동의합니다.<br>
        5. 수술/시술/검사 방법의 변경 또는 수술/시술/검사 범위의 추가 가능성에 대한 설명을 이 수술/시술/검사 시행 전에 의료진으로부터 들었음을 확인합니다.<br>
        6. 주치의(집도의)의 변경 가능성과 사유에 대한 설명을 이 수술/시술/검사 시행 전에 의료진으로부터 들었음을 확인합니다.<br>
        7. 시행예정일은 환자 또는 병원의 부득이한 사정에 따라 변경 될 수 있습니다.<br>
        </div>
        """, unsafe_allow_html=True)

        # Main signature canvas (this one cannot be deleted)
        st.markdown("<b>추가 정보/서명란 (담당의가 필요시 입력)</b>", unsafe_allow_html=True)
        st.write("아래 칸에 추가 설명, 도식, 서명 등을 자유롭게 입력할 수 있습니다.")
        st_canvas(
            fill_color="#fff",
            stroke_width=3,
            stroke_color="#222",
            background_color="#f9f9f9",
            height=180,
            width=900,
            drawing_mode="freedraw",
            key="confirmation_big_canvas"
        )

        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("수술 동의서 PDF 출력하기"):
            st.session_state.step = 3
            st.markdown("<script>window.scrollTo(0, 0);</script>", unsafe_allow_html=True)
            st.rerun()
