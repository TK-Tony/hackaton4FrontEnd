# page_pdf_progress.py
# ──────────────────────────────────────────────────────────────
# 1) 세션 데이터만 사용해 HTML → PDF 변환  
# 2) 환자 특이사항을 “있음/없음”으로 표시  
# 3) 5-3 · 5-5 항목에 동일한 설명 문단 삽입  
#    (확인 페이지와 동일한 한국어 블록 인용)  
# 4) 각 본문(2-8) 아래에 추가된 캔버스 이미지를 자동 삽입  
# ──────────────────────────────────────────────────────────────

import streamlit as st
from streamlit_drawable_canvas import st_canvas
import numpy as np, io, base64, pdfkit, os, json
from datetime import datetime
from PIL import Image

# ──────────────────────────
# 0. 세션-헬퍼
# ──────────────────────────
def get_patient_info() -> dict:
    return st.session_state.get("patient_info", {})

def get_form_data() -> dict:
    return st.session_state.get("form_data", {})

def yes_no(val: str) -> str:
    return "있음" if str(val).strip().lower() in {"유", "true", "yes", "y"} else "없음"

# ──────────────────────────
# 1. 캔버스 → base64 <img>
# ──────────────────────────
def canvas_to_base64(canvas_key: str) -> str:
    key = f"{canvas_key}_image"
    if key in st.session_state:
        img_arr = st.session_state[key].astype(np.uint8)
        if img_arr.shape[2] == 4:            # RGBA → RGB
            img_arr = img_arr[:, :, :3]
        img = Image.fromarray(img_arr)
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        return (
            "<img src='data:image/png;base64,"
            + base64.b64encode(buf.getvalue()).decode()
            + "' width='750' style='margin-bottom:12px;'><br>"
        )
    return ""

# ──────────────────────────
# 2. HTML 조립
# ──────────────────────────
def collect_all_content() -> str:
    info = get_patient_info()
    fd   = get_form_data()
    html = ""

    # 날짜 객체 → 문자열
    sched = info.get("시행예정일", "")
    if hasattr(sched, "strftime"):
        sched = sched.strftime("%Y-%m-%d")

    # ① 기본 정보 테이블
    html += f"""
    <table style="width:100%; border-collapse:collapse; margin-bottom:12px;">
      <tr><th style="border:1px solid #aaa;padding:7px;">등록번호</th>
          <td style="border:1px solid #aaa;padding:7px;">{info.get('등록번호','')}</td>
          <th style="border:1px solid #aaa;padding:7px;">환자명</th>
          <td style="border:1px solid #aaa;padding:7px;">{info.get('환자명','')}</td></tr>
      <tr><th style="border:1px solid #aaa;padding:7px;">수술명</th>
          <td style="border:1px solid #aaa;padding:7px;" colspan="3">{info.get('수술명','')}</td></tr>
      <tr><th style="border:1px solid #aaa;padding:7px;">나이/성별</th>
          <td style="border:1px solid #aaa;padding:7px;">{info.get('나이/성별','')}</td>
          <th style="border:1px solid #aaa;padding:7px;">시행예정일</th>
          <td style="border:1px solid #aaa;padding:7px;">{sched}</td></tr>
      <tr><th style="border:1px solid #aaa;padding:7px;">진단명</th>
          <td style="border:1px solid #aaa;padding:7px;" colspan="3">{info.get('진단명','')}</td></tr>
      <tr><th style="border:1px solid #aaa;padding:7px;">수술부위표시</th>
          <td style="border:1px solid #aaa;padding:7px;">{info.get('수술부위표시','')}</td>
          <th style="border:1px solid #aaa;padding:7px;">수술부위</th>
          <td style="border:1px solid #aaa;padding:7px;">{info.get('수술부위','')}</td></tr>
    </table>
    """

    # ② 의료진
    html += "<b>※ 참여 의료진</b><br>"
    staff_rows = "".join(
        f"<tr><td style='border:1px solid #aaa;padding:7px;'>{d['집도의']}</td>"
        f"<td style='border:1px solid #aaa;padding:7px;'>{d['전문의여부']}</td>"
        f"<td style='border:1px solid #aaa;padding:7px;'>{d['진료과목']}</td></tr>"
        for d in info.get("의료진", [])
    )
    html += f"""
    <table style="width:100%; border-collapse:collapse; margin-bottom:12px;">
      <tr><th style="border:1px solid #aaa;padding:7px;">집도의</th>
          <th style="border:1px solid #aaa;padding:7px;">전문의여부</th>
          <th style="border:1px solid #aaa;padding:7px;">진료과목</th></tr>
      {staff_rows}
    </table>
    """

    # ③ 환자 특이사항
    html += "<b>1. 환자 상태 및 특이사항</b><br>"
    cond_map = {
        "과거병력": yes_no(fd.get("past_history", "")),
        "당뇨병":   yes_no(fd.get("diabetes", "")),
        "흡연유무": yes_no(fd.get("smoking", "")),
        "고혈압":   yes_no(fd.get("hypertension", "")),
        "알레르기": yes_no(fd.get("allergy", "")),
        "저혈압":   yes_no(fd.get("hypotension", "")),
        "기도이상": yes_no(fd.get("airway_abnormality", "")),
        "심혈관질환": yes_no(fd.get("cardiovascular", "")),
        "호흡기질환": yes_no(fd.get("respiratory", "")),
        "혈액응고 관련 질환": yes_no(fd.get("coagulation", "")),
        "복용약물": yes_no(fd.get("medications", "")),
        "신장질환": yes_no(fd.get("renal", "")),
        "마약복용 혹은 약물사고": yes_no(fd.get("drug_abuse", "")),
        "기타": fd.get("other", ""),
    }
    html += "<table style='width:100%; border-collapse:collapse; margin-bottom:12px;'>"
    for k, v in cond_map.items():
        html += f"<tr><th style='border:1px solid #aaa;padding:7px;'>{k}</th><td style='border:1px solid #aaa;padding:7px;'>{v}</td></tr>"
    html += "</table>"

    # ④ 동의서 본문(2~8) + 캔버스
    sections = [
        ("2. 예정된 수술을 하지 않을 경우의 예후", "no_surgery_prognosis", "canvas_count_2", "canvas_2_"),
        ("3. 예정된 수술 이외의 시행 가능한 다른 방법", "alternative_methods", "canvas_count_3", "canvas_3_"),
        ("4. 수술의 목적/필요성/효과", "purpose", "canvas_count_4", "canvas_4_"),
        ("5. 수술의 방법 및 내용", None, None, None),
        ("6. 발생 가능한 합병증/후유증/부작용", "complications", "canvas_count_6", "canvas_6_"),
        ("7. 문제 발생시 조치사항", "preop_care", "canvas_count_7_1", "canvas_7_1_"),
        ("8. 진단/수술 관련 사망 위험성", "mortality_risk", "canvas_count_8", "canvas_8_"),
    ]

    for title, key, cnt_key, base in sections:
        html += f"<h3>{title}</h3>"
        if key:  # 단일 본문
            html += f"<p>{st.session_state.get(key, '')}</p>"
            for i in range(st.session_state.get(cnt_key, 0)):
                html += canvas_to_base64(f"{base}{i}")
        else:    # 5번 다단
            subs = [
                ("1) 수술 과정 전반에 대한 설명", "method_1", "canvas_count_5_1", "canvas_5_1_"),
                ("2) 수술 추정 소요시간", "method_2", "canvas_count_5_2", "canvas_5_2_"),
                ("3) 수술 변경 및 수술 추가 가능성", "method_3", "canvas_count_5_3", "canvas_5_3_"),
                ("4) 수혈 가능성", "method_4", "canvas_count_5_4", "canvas_5_4_"),
                ("5) 집도의 변경 가능성", "method_5", "canvas_count_5_5", "canvas_5_5_"),
            ]
            for sub_t, sub_k, sub_cnt, sub_base in subs:
                html += f"<h4>{sub_t}</h4><p>{st.session_state.get(sub_k, '')}</p>"

                # 5-3 · 5-5 추가 설명 문단
                if sub_k == "method_3":
                    html += """
                    <blockquote>
                      수술/시술/검사과정에서 환자의 상태에 따라 부득이하게 수술/시술/검사방법이 변경되거나
                      수술/시술/검사범위가 추가될 수 있습니다. 이 경우, 환자 또는 대리인에게 추가로 설명하여야
                      하는 사항이 있는 경우에는 시행 전에 설명하고 동의를 얻도록 합니다. 다만, 시행 도중
                      긴급한 변경·추가가 필요한 경우에는 시행 후 지체 없이 사유 및 결과를 설명합니다.
                    </blockquote>
                    """
                if sub_k == "method_5":
                    html += """
                    <blockquote>
                      참여 의료진이 기재되어 있더라도, 응급환자 진료·주치의 질병 등 사정으로 주치의(집도의)가
                      변경될 수 있습니다. 이 경우 시행 전에 사유를 설명하고 동의를 받을 예정이며, 시행 중
                      긴급 변경이 필요한 경우에는 시행 후 지체 없이 변경 사유 및 결과를 설명합니다.
                    </blockquote>
                    """

                for i in range(st.session_state.get(sub_cnt, 0)):
                    html += canvas_to_base64(f"{sub_base}{i}")

    # ⑤ 확인 항목 + 서명 캔버스
    html += """
    <h3>수술 동의서 확인</h3>
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
    <h4>추가 정보/서명란 (필요시 담당의 입력)</h4>
    """
    for i in range(st.session_state.get("canvas_count_signature", 0)):
        html += canvas_to_base64(f"canvas_signature_0")

    return html

# ──────────────────────────
# 3. PDF 생성 진행 페이지
# ──────────────────────────
def page_pdf_progress():
    st.markdown(
        "<h2 style='text-align:center; color:#176d36;'>PDF 생성이 완료되었습니다.<br>항상 환자를 위한 헌신에 감사드립니다.</h2>",
        unsafe_allow_html=True,
    )

    html_body = collect_all_content()
    html_doc = f"""
    <!DOCTYPE html><html lang="ko"><head>
      <meta charset="UTF-8"><title>수술 동의서</title>
      <style>
        body{{font-family:'Malgun Gothic','맑은 고딕',Arial,sans-serif;line-height:1.6;margin:20px}}
        table{{border-collapse:collapse;width:100%;margin-bottom:15px}}
        th,td{{border:1px solid #aaa;padding:7px;text-align:left}}
        th{{background:#f5f5f5;font-weight:bold}}
        h3{{color:#333;margin-top:25px;margin-bottom:15px}}
        h4{{color:#555;margin-top:20px;margin-bottom:10px}}
        blockquote{{background:#f9f9f9;border-left:4px solid #ccc;margin:15px 0;padding:10px 15px}}
        img{{max-width:100%;height:auto;display:block;margin:10px 0}}
        ol{{padding-left:20px}} li{{margin-bottom:5px}}
      </style></head><body>
      <h1 style='text-align:center;color:#333;margin-bottom:30px;'>수술 동의서</h1>
      {html_body}
    </body></html>
    """

    wkhtml = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"  # "/usr/bin/wkhtmltopdf" 
    config = pdfkit.configuration(wkhtmltopdf=wkhtml)
    opts = {
        "page-size": "A4",
        "encoding": "UTF-8",
        "no-outline": None,
        "margin-top": "0.75in",
        "margin-right": "0.75in",
        "margin-bottom": "0.75in",
        "margin-left": "0.75in",
        "enable-local-file-access": None,
    }

    try:
        pdfkit.from_string(html_doc, "surgery_consent.pdf", configuration=config, options=opts)
        st.success("PDF가 성공적으로 생성되었습니다.")
        with open("surgery_consent.pdf", "rb") as f:
            st.download_button("PDF 다운로드", f.read(), "수술동의서.pdf", "application/pdf")
    except Exception as e:
        st.error(f"PDF 생성 오류: {e}<br>wkhtmltopdf 설치·경로를 확인해 주세요.", unsafe_allow_html=True)

# ──────────────────────────
if __name__ == "__main__":
    page_pdf_progress()
