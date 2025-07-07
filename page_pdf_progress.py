import streamlit as st
from streamlit_drawable_canvas import st_canvas
import json
import numpy as np
from PIL import Image
import io
import base64
from page_confirmation import load_patient_data
import pdfkit
import os

def canvas_to_base64(canvas_key):
    """Convert canvas image to base64 HTML img tag"""
    if f"{canvas_key}_image" in st.session_state:
        img_array = st.session_state[f"{canvas_key}_image"].astype(np.uint8)
        if img_array.shape[2] == 4:  # Remove alpha channel if RGBA
            img_array = img_array[:, :, :3]
        img = Image.fromarray(img_array)
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        return f'<img src="data:image/png;base64,{img_str}" width="750" style="margin-bottom:12px;"><br>'
    return ""

def collect_all_content():
    consent_data = load_patient_data()
    full_html = ""
    
    # Patient & Surgery Info Table
    full_html += f"""
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
    """

    # Medical staff
    full_html += "<b>※ 참여 의료진</b><br>"
    doctor_rows = ""
    for doc in consent_data.get('의료진', []):
        doctor_rows += (
            f"<tr>"
            f"<td style='border:1px solid #aaa; padding:7px;'>{doc.get('집도의','')}</td>"
            f"<td style='border:1px solid #aaa; padding:7px;'>{doc.get('전문의여부','')}</td>"
            f"<td style='border:1px solid #aaa; padding:7px;'>{doc.get('진료과목','')}</td>"
            f"</tr>"
        )

    full_html += f"""
    <table style="width:100%; border-collapse:collapse; margin-bottom:12px;">
    <tr>
        <th style="border:1px solid #aaa; padding:7px;">집도의</th>
        <th style="border:1px solid #aaa; padding:7px;">전문의여부</th>
        <th style="border:1px solid #aaa; padding:7px;">진료과목</th>
    </tr>
    {doctor_rows}
    </table>
    """

    # Section 1: 환자 상태 및 특이사항
    full_html += "<b>1. 환자 상태 및 특이사항</b><br>"
    full_html += f"""
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
    """

    full_html += f"<b>※ 기타</b><br>{consent_data.get('기타','')}<br><br>"

    # Section 2
    full_html += "<h3>2. 예정된 수술을 하지 않을 경우의 예후</h3>"
    full_html += f"<p>{st.session_state.get('no_surgery_prognosis', '')}</p>"
    
    # Add canvas images for section 2
    for i in range(st.session_state.get("canvas_count_2", 0)):
        canvas_html = canvas_to_base64(f"canvas_2_{i}")
        if canvas_html:
            full_html += canvas_html

    # Section 3
    full_html += "<h3>3. 예정된 수술 이외의 시행 가능한 다른 방법</h3>"
    full_html += f"<p>{st.session_state.get('alternative_methods', '')}</p>"
    for i in range(st.session_state.get("canvas_count_3", 0)):
        canvas_html = canvas_to_base64(f"canvas_3_{i}")
        if canvas_html:
            full_html += canvas_html
    # Section 4
    full_html += "<h3>4. 수술의 목적/필요성/효과</h3>"
    full_html += f"<p>{st.session_state.get('purpose', '')}</p>"
    for i in range(st.session_state.get("canvas_count_4", 0)):
        canvas_html = canvas_to_base64(f"canvas_4_{i}")
        if canvas_html:
            full_html += canvas_html

    # Section 5
    full_html += "<h3>5. 수술의 방법 및 내용</h3>"
    
    # Subsection 1
    full_html += "<h4>1) 수술 과정 전반에 대한 설명</h4>"
    full_html += f"<p>{st.session_state.get('method_1', '')}</p>"
    for i in range(st.session_state.get("canvas_count_5_1", 0)):
        canvas_html = canvas_to_base64(f"canvas_5_1_{i}")
        if canvas_html:
            full_html += canvas_html

    # Subsection 2
    full_html += "<h4>2) 수술 추정 소요시간</h4>"
    full_html += f"<p>{st.session_state.get('method_2', '')}</p>"
    for i in range(st.session_state.get("canvas_count_5_2", 0)):
        canvas_html = canvas_to_base64(f"canvas_5_2_{i}")
        if canvas_html:
            full_html += canvas_html

    # Subsection 3
    full_html += "<h4>3) 수술 변경 및 수술 추가 가능성</h4>"
    full_html += """
    <blockquote>
    수술/시술/검사과정에서 환자의 상태에 따라 부득이하게 수술/시술/검사방법이 변경되거나 수술/시술/검사범위가 추가될 수 있습니다.<br>
    이 경우, 환자 또는 대리인에게 추가로 설명하여야 하는 사항이 있는 경우에는 수술/시술/검사의 시행 전에 이에 대하여 설명하고 동의를 얻도록 합니다.<br>
    다만, 수술/시술/검사의 시행 도중에 환자의 상태에 따라 미리 설명하고 동의를 얻을 수 없을 정도로 긴급한 변경 또는 추가가 요구되는 경우에는<br>
    시행 후에 지체 없이 그 사유 및 결과를 환자 또는 대리인에게 설명하도록 합니다.
    </blockquote>
    """
    for i in range(st.session_state.get("canvas_count_5_3", 0)):
        canvas_html = canvas_to_base64(f"canvas_5_3_{i}")
        if canvas_html:
            full_html += canvas_html

    # Subsection 4
    full_html += "<h4>4) 수혈 가능성</h4>"
    full_html += f"<p>{st.session_state.get('method_4', '')}</p>"
    for i in range(st.session_state.get("canvas_count_5_4", 0)):
        canvas_html = canvas_to_base64(f"canvas_5_4_{i}")
        if canvas_html:
            full_html += canvas_html

    # Subsection 5
    full_html += "<h4>5) 진단/수술 관련 사망 위험성</h4>"
    full_html += """
    <blockquote>
    위에 기재된 참여 의료진이 있는 경우 수술/시술/검사과정에서 환자의 상태 또는 의료기관의 사정(응급환자 진료, 주치의의 질병·출장 등)에 따라<br>
    부득이하게 주치의(집도의)가 변경될 수 있습니다. 이 경우 시행 전에 환자 또는 대리인에게 구체적인 변경사유를 설명하고 동의를 얻을 예정입니다.<br>
    다만, 시행 도중에 미리 설명하고 동의를 얻을 수 없을 정도로 긴급한 변경이 요구되는 경우에는 시행 후에<br>
    지체 없이 구체적인 변경 사유 및 시행결과를 환자 또는 대리인에게 설명하도록 합니다.
    </blockquote>
    """
    for i in range(st.session_state.get("canvas_count_5_5", 0)):
        canvas_html = canvas_to_base64(f"canvas_5_5_{i}")
        if canvas_html:
            full_html += canvas_html

    # Section 6
    full_html += "<h3>6. 발생 가능한 합병증/후유증/부작용</h3>"
    full_html += f"<p>{st.session_state.get('complications', '')}</p>"
    for i in range(st.session_state.get("canvas_count_6", 0)):
        canvas_html = canvas_to_base64(f"canvas_6_{i}")
        if canvas_html:
            full_html += canvas_html

    # Section 7
    full_html += "<h3>7. 문제 발생시 조치사항</h3>"
    full_html += f"<p>{st.session_state.get('preop_care', '')}</p>"
    for i in range(st.session_state.get("canvas_count_7_1", 0)):
        canvas_html = canvas_to_base64(f"canvas_7_1_{i}")
        if canvas_html:
            full_html += canvas_html

    # Section 8
    full_html += "<h3>8. 진단/수술 관련 사망 위험성</h3>"
    full_html += f"<p>{st.session_state.get('mortality_risk', '')}</p>"
    for i in range(st.session_state.get("canvas_count_8", 0)):
        canvas_html = canvas_to_base64(f"canvas_8_{i}")
        if canvas_html:
            full_html += canvas_html

    # Signature and Confirmation Section
    full_html += "<h3>수술 동의서 확인</h3>"
    full_html += """
    <p>아래 내용을 읽고 동의해 주세요.</p>
    <ol>
        <li>나는 수술/시술/검사의 목적, 효과, 과정, 예상되는 위험에 대해 설명을 들었습니다.</li>
        <li>궁금한 점을 의료진에게 질문할 수 있었고, 충분히 생각할 시간을 가졌습니다.</li>
        <li>예상치 못한 합병증이나 사고가 생길 수 있음을 이해합니다.</li>
        <li>수술/시술/검사에 협조하고, 내 상태를 정확히 알릴 것을 약속합니다.</li>
        <li>수술 방법이나 범위가 바뀔 수 있다는 설명을 들었습니다.</li>
        <li>담당의사가 바뀔 수 있다는 설명을 들었습니다.</li>
        <li>일정이 바뀔 수 있음을 이해합니다.</li>
    </ol>
    """

    full_html += "<h4>추가 정보/서명란 (필요시 담당의 입력)</h4>"
    for i in range(st.session_state.get("canvas_count_9", 0)):
        canvas_html = canvas_to_base64(f"canvas_9_{i}")
        if canvas_html:
            full_html += canvas_html

    return full_html

def page_pdf_progress():

    #st.set_page_config(layout="wide")

    #여백 제거 및 container 최대 폭 확장
    st.markdown("""
        <style>
        .block-container {
            padding: 0rem;
            max-width: 100% !important;
        }
        .form-wrapper {
            max-width: 800px;
            margin-left: 10px;
            margin-right: 10px;
            padding: 0rem;
        }
        </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 6, 1])
    with col2:

        st.markdown("""
            <h2 style='text-align:center; color:#176d36; padding-top:0px; margin: 0 0 20px 0'>PDF 생성이 완료되었습니다.<br>항상 환자를 위한 헌신에 감사드립니다.</h2>
        """, unsafe_allow_html=True)


        full_content = collect_all_content()
        
        # Add proper HTML structure with UTF-8 encoding for Korean text
        html_with_encoding = f"""
        <!DOCTYPE html>
        <html lang="ko">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>수술 동의서</title>
            <style>
                body {{ 
                    font-family: 'Malgun Gothic', '맑은 고딕', Arial, sans-serif; 
                    line-height: 1.6;
                    margin: 20px;
                }}
                table {{ 
                    border-collapse: collapse; 
                    width: 100%; 
                    margin-bottom: 15px;
                }}
                th, td {{ 
                    border: 1px solid #aaa; 
                    padding: 7px; 
                    text-align: left; 
                }}
                th {{
                    background-color: #f5f5f5;
                    font-weight: bold;
                }}
                h3 {{
                    color: #333;
                    margin-top: 25px;
                    margin-bottom: 15px;
                }}
                h4 {{
                    color: #555;
                    margin-top: 20px;
                    margin-bottom: 10px;
                }}
                blockquote {{
                    background-color: #f9f9f9;
                    border-left: 4px solid #ccc;
                    margin: 15px 0;
                    padding: 10px 15px;
                }}
                img {{
                    max-width: 100%;
                    height: auto;
                    display: block;
                    margin: 10px 0;
                }}
                ol {{
                    padding-left: 20px;
                }}
                li {{
                    margin-bottom: 5px;
                }}
            </style>
        </head>
        <body>
            <h1 style="text-align: center; color: #333; margin-bottom: 30px;">수술 동의서</h1>
            {full_content}
        </body>
        </html>
        """
        
        # Configure pdfkit for Windows with proper encoding
        path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
        config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
        
        # PDF generation options for Korean text
        options = {
            'page-size': 'A4',
            'encoding': 'UTF-8',
            'no-outline': None,
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'enable-local-file-access': None,
        }
        
        try:
            # Generate PDF with proper Korean encoding
            pdfkit.from_string(
                html_with_encoding, 
                'surgery_consent.pdf', 
                configuration=config,
                options=options
            )
            st.success("PDF가 성공적으로 생성되었습니다: surgery_consent.pdf")
            
            # Provide download button
            with open('surgery_consent.pdf', 'rb') as pdf_file:
                st.download_button(
                    label="PDF 다운로드",
                    data=pdf_file.read(),
                    file_name="수술동의서.pdf",
                    mime="application/pdf"
                )
                
        except Exception as e:
            st.error(f"PDF 생성 중 오류가 발생했습니다: {str(e)}")
            st.info("wkhtmltopdf가 설치되어 있는지 확인해주세요.")

        col1, col2 = st.columns([0.8, 1])
        with col2:
            if st.button("메인화면으로"):
                st.session_state.step = -1
                st.rerun()