import streamlit as st
import json
import requests
from components.buttons import big_green_button
import logging
from datetime import time, date
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field, constr, field_validator, model_validator
from pydantic import ConfigDict

# -------------------------------------------------
# Base Models for Surgery Details and References
# -------------------------------------------------

from pydantic import BaseModel
from pydantic import Field


class SurgeryDetails(BaseModel):
    """수술 관련 세부 정보"""
    overall_description: str = Field(..., description="수술 과정 전반에 대한 설명")
    estimated_duration: str = Field(..., description="수술 추정 소요시간")
    method_change_or_addition: str = Field(..., description="수술 방법 변경 및 수술 추가 가능성")
    transfusion_possibility: str = Field(..., description="수혈 가능성")
    surgeon_change_possibility: str = Field(..., description="집도의 변경 가능성")


class ConsentBase(BaseModel):
    """
    수술동의서
    """
    prognosis_without_surgery: str = Field(..., description="예정된 수술을 하지 않을 경우의 예후")
    alternative_treatments: str = Field(..., description="예정된 수술 이외의 시행 가능한 다른 방법")
    surgery_purpose_necessity_effect: str = Field(..., description="수술의 목적/필요성/효과")
    surgery_method_content: SurgeryDetails = Field(..., description="수술의 방법 및 내용")
    possible_complications_sequelae: str = Field(..., description="발생 가능한 합병증/후유증/부작용")
    emergency_measures: str = Field(..., description="문제 발생시 조치사항")
    mortality_risk: str = Field(..., description="진단/수술 관련 사망 위험성")


class ReferenceItem(BaseModel):
    """
    참고 문헌 항목
    """
    title: str = Field(..., description="참고 문헌 제목")
    url: str = Field(..., description="참고 문헌 URL")
    text: str = Field(..., description="참고 문헌 텍스트")


class SurgeryDetailsReference(BaseModel):
    """
    수술 관련 세부 정보 참고 문헌
    """
    overall_description: list[ReferenceItem] = Field(default_factory=list, description="수술 과정 전반에 대한 설명")
    estimated_duration: list[ReferenceItem] = Field(default_factory=list, description="수술 추정 소요시간")
    method_change_or_addition: list[ReferenceItem] = Field(default_factory=list, description="수술 방법 변경 및 수술 추가 가능성")
    transfusion_possibility: list[ReferenceItem] = Field(default_factory=list, description="수혈 가능성")
    surgeon_change_possibility: list[ReferenceItem] = Field(default_factory=list, description="집도의 변경 가능성")


class ReferenceBase(BaseModel):
    """
    참고 문헌
    """
    prognosis_without_surgery: list[ReferenceItem] = Field(default_factory=list, description="예정된 수술을 하지 않을 경우의 예후")
    alternative_treatments: list[ReferenceItem] = Field(default_factory=list, description="예정된 수술 이외의 시행 가능한 다른 방법")
    surgery_purpose_necessity_effect: list[ReferenceItem] = Field(default_factory=list, description="수술의 목적/필요성/효과")
    surgery_method_content: SurgeryDetailsReference = Field(default_factory=SurgeryDetailsReference, description="수술의 방법 및 내용")
    possible_complications_sequelae: list[ReferenceItem] = Field(default_factory=list, description="발생 가능한 합병증/후유증/부작용")
    emergency_measures: list[ReferenceItem] = Field(default_factory=list, description="문제 발생시 조치사항")
    mortality_risk: list[ReferenceItem] = Field(default_factory=list, description="진단/수술 관련 사망 위험성")
# -------------------------------------------------
# Enums and Type Definitions
# -------------------------------------------------

class Gender(str, Enum):
    male = "M"
    female = "F"

BoolOrStr = bool | constr(strip_whitespace=True, min_length=1)

# -------------------------------------------------
# Medical Team and Patient Information Models
# -------------------------------------------------

class Participant(BaseModel):
    name: Optional[str] = Field(None, description="의료진 성명")
    is_specialist: bool = Field(..., description="전문의 여부")
    department: str = Field(..., description="진료과 명칭")

class SpecialCondition(BaseModel):
    past_history: bool | str = False       # 과거병력
    diabetes: bool | str = False           # 당뇨병
    smoking: bool | str = False            # 흡연 여부
    hypertension: bool | str = False       # 고혈압
    allergy: bool | str = False            # 약물/음식 알레르기
    cardiovascular: bool | str = False     # 심혈관 질환
    respiratory: bool | str = False        # 호흡기 질환
    coagulation: bool | str = False        # 혈액응고 관련 질환
    medications: bool | str = False        # 복용 약물
    renal: bool | str = False              # 신장 질환
    drug_abuse: bool | str = False         # 마약/약물 사고
    other: Optional[str] = None            # 기타 자유 기술

class PossumScore(BaseModel):
    """POSSUM Score - 수술 후 사망률과 이환율 위험도 예측"""
    mortality_risk: float = Field(..., ge=0, le=100, description="사망률 위험도 (%)")
    morbidity_risk: float = Field(..., ge=0, le=100, description="합병증 위험도 (%)")

# -------------------------------------------------
# Request Models (Grouped Data Input)
# -------------------------------------------------

class PrivateConsentGenerateIn(BaseModel):
    """수술동의서 생성 요청 - 개인정보"""
    registration_no: str = Field(..., description="등록번호")
    patient_name: str = Field(..., description="환자 성명")

class PublicConsentGenerateIn(BaseModel):
    model_config = ConfigDict(
        json_encoders={
            date: lambda v: v.isoformat()
        }
    )
    surgery_name: str = Field(..., description="수술 명칭")
    age: int = Field(..., ge=0, le=150)
    gender: Gender
    scheduled_date: date = Field(..., description="수술 예정일")
    diagnosis: str = Field(..., description="진단명")
    surgical_site_mark: str = Field(..., description="수술 부위 표시")
    participants: List[Participant] = Field(..., min_items=1, description="참여 의료진 목록")
    patient_condition: str = Field(..., description="현재 환자 상태 요약")
    special_conditions: SpecialCondition = Field(default_factory=SpecialCondition)
    possum_score: Optional[PossumScore] = Field(None, description="POSSUM Score 위험도 평가")


class ConsentGenerateIn(PrivateConsentGenerateIn, PublicConsentGenerateIn):
    
    @field_validator('participants')
    @classmethod
    def validate_participants(cls, v):
        if not v:
            raise ValueError("최소 1명의 의료진 정보가 필요합니다")
        return v
    

# -------------------------------------------------
# Response Models (Grouped Data Output)
# -------------------------------------------------

class ConsentGenerateOut(BaseModel):
    """수술동의서 생성 결과"""
    consents: ConsentBase = Field(..., description="수술동의서")
    references: ReferenceBase = Field(..., description="참고 문헌")

class APIResponse[T](BaseModel):
    """Generic API Response Wrapper"""
    success: bool = Field(default=True, description="요청 성공 여부")
    message: str = Field(default="", description="응답 메시지")
    data: Optional[T] = Field(None, description="응답 데이터")
    errors: Optional[List[str]] = Field(None, description="오류 목록")

class ConsentMetadata(BaseModel):
    """동의서 메타데이터"""
    request_id: str = Field(..., description="요청 ID")
    generated_at: str = Field(..., description="생성 시간")
    version: str = Field(default="1.0", description="버전")

class EnhancedConsentResponse(BaseModel):
    """향상된 동의서 응답 모델"""
    metadata: ConsentMetadata = Field(..., description="메타데이터")
    consent_data: ConsentGenerateOut = Field(..., description="동의서 데이터")
    formatted_text: Optional[str] = Field(None, description="포맷된 텍스트")

# -------------------------------------------------
# Utility Functions
# -------------------------------------------------

def str_to_bool(s: str) -> bool:
    """문자열을 불린값으로 변환"""
    return {
        "true": True,
        "false": False
    }.get(s.strip().lower(), False)

def create_consent_request(form_data: dict) -> ConsentGenerateIn:
    """폼 데이터로부터 ConsentGenerateIn 객체 생성"""
    
    # 의료진 정보 처리 - 개선된 버전
    participants = []
    for i in range(1, 4):
        operator = form_data.get(f"operator_{i}", "").strip()
        department = form_data.get(f"department_{i}", "").strip()
        
        # 이름과 진료과가 모두 있는 경우만 추가
        if operator and department:
            participants.append(Participant(
                name=operator,
                is_specialist=form_data.get(f"specialist_{i}", "전문의") == "전문의",
                department=department
            ))
    
    # 의료진이 없는 경우 기본값 추가
    if not participants:
        participants.append(Participant(
            name="미입력",
            is_specialist=True,
            department="외과"
        ))
    
    # 특이사항 처리
    special_conditions = SpecialCondition(
        past_history=str_to_bool(form_data.get("past_history", "false")),
        diabetes=str_to_bool(form_data.get("diabetes", "false")),
        smoking=str_to_bool(form_data.get("smoking", "false")),
        hypertension=str_to_bool(form_data.get("hypertension", "false")),
        allergy=str_to_bool(form_data.get("allergy", "false")),
        cardiovascular=str_to_bool(form_data.get("cardiovascular", "false")),
        respiratory=str_to_bool(form_data.get("respiratory", "false")),
        coagulation=str_to_bool(form_data.get("coagulation", "false")),
        medications=str_to_bool(form_data.get("medications", "false")),
        renal=str_to_bool(form_data.get("renal", "false")),
        drug_abuse=str_to_bool(form_data.get("drug_abuse", "false")),
        other=form_data.get("other", "")
    )
    
    possum_score = None
    if st.session_state.get("possum_results"):
        possum_score = PossumScore(
            mortality_risk=st.session_state.possum_results.get("mortality", 0.0),
            morbidity_risk=st.session_state.possum_results.get("morbidity", 0.0)
        )
    
    scheduled_date_value = form_data.get("scheduled_date")
    
    if isinstance(scheduled_date_value, date):
        scheduled_date = scheduled_date_value
    elif isinstance(scheduled_date_value, str) and scheduled_date_value:
        try:
            scheduled_date = date.fromisoformat(scheduled_date_value)
        except ValueError:
            scheduled_date = date.today()
    else:
        scheduled_date = date.today()
    
    age_value = form_data.get("age", "0")
    try:
        age = int(age_value) if age_value else 0
    except (ValueError, TypeError):
        age = 0
    
    return ConsentGenerateIn(
        registration_no=form_data.get("registration_no", ""),
        patient_name=form_data.get("patient_name", ""),
        surgery_name=form_data.get("surgery_name", ""),
        age=age,
        gender=Gender(form_data.get("gender", "M")),
        scheduled_date=scheduled_date,
        diagnosis=form_data.get("diagnosis", ""),
        surgical_site_mark=form_data.get("surgical_site_mark", ""),
        participants=participants,
        patient_condition=form_data.get("patient_condition", "Stable"),
        special_conditions=special_conditions,
        possum_score=possum_score
    )


def send_consent_request(request_data: ConsentGenerateIn) -> APIResponse[ConsentGenerateOut]:
    try:
        url = "http://10.104.198.155:8000/consent"
        headers = {"Content-Type": "application/json"}
        
        # model_dump_json() 사용하여 JSON 직렬화 문제 해결
        json_data = request_data.model_dump_json()
        
        response = requests.post(
            url, 
            data=json_data, 
            headers=headers, 
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            consent_out = ConsentGenerateOut.model_validate(result)
            return APIResponse(
                success=True,
                message="동의서가 성공적으로 생성되었습니다",
                data=consent_out
            )
        else:
            return APIResponse(
                success=False,
                message=f"API 오류: {response.status_code}",
                errors=[response.text]
            )
            
    except Exception as e:
        return APIResponse(
            success=False,
            message="요청 처리 중 오류가 발생했습니다",
            errors=[str(e)]
        )


# -------------------------------------------------
# Session State Management
# -------------------------------------------------

def store_consent_response(api_response: APIResponse[ConsentGenerateOut]):
    if api_response.success and api_response.data:
        consent_data = api_response.data
        
        # Store consent content
        # Convert reference objects to strings if needed
        def extract_references(ref_list):
            if isinstance(ref_list, list):
                return [item.get('title', str(item)) if isinstance(item, dict) else str(item) for item in ref_list]
            return ref_list
        
        st.session_state.update({
            "no_surgery_prognosis": consent_data.consents.prognosis_without_surgery,
            "alternative_methods": consent_data.consents.alternative_treatments,
            "purpose": consent_data.consents.surgery_purpose_necessity_effect,
            "method_1": consent_data.consents.surgery_method_content.overall_description,
            "method_2": consent_data.consents.surgery_method_content.estimated_duration,
            "method_3": consent_data.consents.surgery_method_content.method_change_or_addition,
            "method_4": consent_data.consents.surgery_method_content.transfusion_possibility,
            "method_5": consent_data.consents.surgery_method_content.surgeon_change_possibility,
            "complications": consent_data.consents.possible_complications_sequelae,
            "preop_care": consent_data.consents.emergency_measures,
            "mortality_risk": consent_data.consents.mortality_risk,
        })
        
        # Store references properly
        references_dict = consent_data.references.model_dump()
        st.session_state["consent_references"] = references_dict


# Initialize session state
if 'possum_results' not in st.session_state:
    st.session_state.possum_results = None

if 'navigate_to_possum' not in st.session_state:
    st.session_state.navigate_to_possum = False

if 'show_possum' not in st.session_state:
    st.session_state.show_possum = False

# -------------------------------------------------
# Main Page Function (Streamlit UI)
# -------------------------------------------------

def page_basic_info():
    st.set_page_config(layout="wide")
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
                ], key="surgery_name"
            )

            # 환자 기본 정보
            col1, col2 = st.columns(2)
            with col1:
                reg_num = st.text_input("등록번호")
            with col2:
                patient_name = st.text_input("환자명")

            col3, col4 = st.columns(2)
            with col3:
                age = st.text_input("나이")
                gender = st.text_input("성별 (M/F)")
            with col4:
                scheduled_date = st.date_input("시행예정일")

            # 진단명
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
            
            # 의료진 정보
            st.markdown("**※ 참여 의료진 (집도의가 다수인 경우 모두 기재해 주시기 바랍니다.)**")
            for i in range(1, 4):
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

            # 환자 특이사항
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
                
                # POSSUM 점수 계산 버튼 및 결과 표시
                possum = st.form_submit_button("POSSUM 점수 계산 (먼저 계산 후 위의 정보를 입력하세요)", help="수술의 위험도를 평가하기 위한 POSSUM 점수를 계산합니다.")
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

            # POSSUM 버튼 처리
            if possum:
                st.session_state.navigate_to_possum = True

            # 동의서 생성 처리
            if submitted:
                try:
                    # 폼 데이터 수집
                    form_data = {
                        "registration_no": reg_num,
                        "patient_name": patient_name,
                        "surgery_name": surgery_name,
                        "age": age,
                        "gender": gender,
                        "scheduled_date": scheduled_date,
                        "diagnosis": diagnosis,
                        "surgical_site_mark": surgery_site,
                        "patient_condition": "Stable",
                        "past_history": past_history,
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
                    
                    # 의료진 정보 추가
                    for i in range(1, 4):
                        form_data[f"operator_{i}"] = st.session_state.get(f"operator_{i}", "")
                        form_data[f"specialist_{i}"] = st.session_state.get(f"specialist_{i}", "전문의")
                        form_data[f"department_{i}"] = st.session_state.get(f"department_{i}", "")
                    
                    # Pydantic 모델로 변환
                    consent_request = create_consent_request(form_data)
                    
                    # API 요청 전송
                    api_response = send_consent_request(consent_request)
                    
                    if api_response.success:
                        st.success(api_response.message)
                        store_consent_response(api_response)
                        st.session_state.step = 1
                        
                        # 결과 표시
                        if api_response.data:
                            st.markdown("#### 수술 동의서 본문")
                            consent_text = f"""
                            **예정된 수술을 하지 않을 경우의 예후:** {api_response.data.consents.prognosis_without_surgery}
                            
                            **대안 치료법:** {api_response.data.consents.alternative_treatments}
                            
                            **수술의 목적/필요성/효과:** {api_response.data.consents.surgery_purpose_necessity_effect}
                            
                            **발생 가능한 합병증/후유증/부작용:** {api_response.data.consents.possible_complications_sequelae}
                            
                            **응급 조치사항:** {api_response.data.consents.emergency_measures}
                            
                            **사망 위험성:** {api_response.data.consents.mortality_risk}
                            """
                            st.text_area("동의서", consent_text, height=400)
                    else:
                        st.error(f"오류: {api_response.message}")
                        if api_response.errors:
                            for error in api_response.errors:
                                st.error(error)
                                
                except Exception as e:
                    st.error(f"처리 중 오류가 발생했습니다: {str(e)}")

    # POSSUM 계산기 네비게이션 처리
    if possum:  
        st.session_state.show_possum = True
        st.rerun()
