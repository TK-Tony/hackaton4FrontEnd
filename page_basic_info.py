import streamlit as st
import requests
from datetime import date
from enum import Enum
from typing import List, Optional, TypeVar, Generic
from pydantic import BaseModel, Field, constr, field_validator, ConfigDict
from pydantic.generics import GenericModel

# ──────────────────────────────
# 0. 공통 타입
# ──────────────────────────────
class Gender(str, Enum):
    male = "M"
    female = "F"

BoolOrStr = bool | constr(strip_whitespace=True, min_length=1)

# ──────────────────────────────
# 1. Pydantic 모델
# ──────────────────────────────
class SurgeryDetails(BaseModel):
    overall_description: str
    estimated_duration: str
    method_change_or_addition: str
    transfusion_possibility: str
    surgeon_change_possibility: str


class ConsentBase(BaseModel):
    prognosis_without_surgery: str
    alternative_treatments: str
    surgery_purpose_necessity_effect: str
    surgery_method_content: SurgeryDetails
    possible_complications_sequelae: str
    emergency_measures: str
    mortality_risk: str


class ReferenceItem(BaseModel):
    title: str
    url: str
    text: str


class SurgeryDetailsReference(BaseModel):
    overall_description: list[ReferenceItem] = Field(default_factory=list)
    estimated_duration: list[ReferenceItem] = Field(default_factory=list)
    method_change_or_addition: list[ReferenceItem] = Field(default_factory=list)
    transfusion_possibility: list[ReferenceItem] = Field(default_factory=list)
    surgeon_change_possibility: list[ReferenceItem] = Field(default_factory=list)


class ReferenceBase(BaseModel):
    prognosis_without_surgery: list[ReferenceItem] = Field(default_factory=list)
    alternative_treatments: list[ReferenceItem] = Field(default_factory=list)
    surgery_purpose_necessity_effect: list[ReferenceItem] = Field(default_factory=list)
    surgery_method_content: SurgeryDetailsReference = Field(default_factory=SurgeryDetailsReference)
    possible_complications_sequelae: list[ReferenceItem] = Field(default_factory=list)
    emergency_measures: list[ReferenceItem] = Field(default_factory=list)
    mortality_risk: list[ReferenceItem] = Field(default_factory=list)


class Participant(BaseModel):
    name: Optional[str] = None
    is_specialist: bool
    department: str


class SpecialCondition(BaseModel):
    past_history: BoolOrStr = False
    diabetes: BoolOrStr = False
    smoking: BoolOrStr = False
    hypertension: BoolOrStr = False
    allergy: BoolOrStr = False
    cardiovascular: BoolOrStr = False
    respiratory: BoolOrStr = False
    coagulation: BoolOrStr = False
    medications: BoolOrStr = False
    renal: BoolOrStr = False
    drug_abuse: BoolOrStr = False
    other: Optional[str] = None


class PossumScore(BaseModel):
    mortality_risk: float = Field(..., ge=0, le=100)
    morbidity_risk: float = Field(..., ge=0, le=100)


class PrivateConsentGenerateIn(BaseModel):
    registration_no: str
    patient_name: str


class PublicConsentGenerateIn(BaseModel):
    model_config = ConfigDict(json_encoders={date: lambda v: v.isoformat()})
    surgery_name: str
    age: int = Field(..., ge=0, le=150)
    gender: Gender
    scheduled_date: date
    diagnosis: str
    surgical_site_mark: str
    participants: List[Participant]
    patient_condition: str
    special_conditions: SpecialCondition = Field(default_factory=SpecialCondition)
    possum_score: Optional[PossumScore] = None


class ConsentGenerateIn(PrivateConsentGenerateIn, PublicConsentGenerateIn):
    @field_validator("participants")
    @classmethod
    def check_participants(cls, v):
        if not v:
            raise ValueError("최소 1명의 의료진 정보가 필요합니다")
        return v


class ConsentGenerateOut(BaseModel):
    consents: ConsentBase
    references: ReferenceBase


T = TypeVar("T")
class APIResponse(GenericModel, Generic[T]):
    success: bool = True
    message: str = ""
    data: Optional[T] = None
    errors: Optional[List[str]] = None

# ──────────────────────────────
# 2. 헬퍼
# ──────────────────────────────
def str_to_bool(s: str) -> bool:
    return s.strip().lower() in {"true", "유", "yes", "y"}


def create_consent_request(form: dict) -> ConsentGenerateIn:
    parts: List[Participant] = []
    for i in range(1, 4):
        n, dpt = form.get(f"operator_{i}", "").strip(), form.get(f"department_{i}", "").strip()
        if n and dpt:
            parts.append(
                Participant(
                    name=n,
                    is_specialist=form.get(f"specialist_{i}") == "전문의",
                    department=dpt,
                )
            )
    if not parts:
        parts.append(Participant(name="미입력", is_specialist=True, department="외과"))

    sc = SpecialCondition(
        past_history=str_to_bool(form.get("past_history", "false")),
        diabetes=str_to_bool(form.get("diabetes", "false")),
        smoking=str_to_bool(form.get("smoking", "false")),
        hypertension=str_to_bool(form.get("hypertension", "false")),
        allergy=str_to_bool(form.get("allergy", "false")),
        cardiovascular=str_to_bool(form.get("cardiovascular", "false")),
        respiratory=str_to_bool(form.get("respiratory", "false")),
        coagulation=str_to_bool(form.get("coagulation", "false")),
        medications=str_to_bool(form.get("medications", "false")),
        renal=str_to_bool(form.get("renal", "false")),
        drug_abuse=str_to_bool(form.get("drug_abuse", "false")),
        other=form.get("other", ""),
    )

    possum = (
        PossumScore(
            mortality_risk=st.session_state.possum_results["mortality"],
            morbidity_risk=st.session_state.possum_results["morbidity"],
        )
        if st.session_state.get("possum_results")
        else None
    )

    return ConsentGenerateIn(
        registration_no=form["registration_no"],
        patient_name=form["patient_name"],
        surgery_name=form["surgery_name"],
        age=int(form["age"] or 0),
        gender=Gender(form["gender"] or "M"),
        scheduled_date=form["scheduled_date"],
        diagnosis=form["diagnosis"],
        surgical_site_mark=form["surgical_site_mark"],
        participants=parts,
        patient_condition="Stable",
        special_conditions=sc,
        possum_score=possum,
    )


def send_consent_request(req: ConsentGenerateIn) -> APIResponse[ConsentGenerateOut]:
    url = "https://api.surgi-form.com/consent"      # ① 실제 엔드포인트
    try:
        r = requests.post(
            url,
            json=req.model_dump(mode="json", by_alias=True),
            timeout=(15, 60)                          # ② 연결 5 초·응답 60 초
        )

        if r.ok:                                     # ③ 200–299
            return APIResponse(
                success=True,
                message="동의서가 성공적으로 생성되었습니다",
                data=ConsentGenerateOut.model_validate(r.json()),
            )
        return APIResponse(success=False,
                           message=f"API 오류: {r.status_code}",
                           errors=[r.text])
    except requests.exceptions.RequestException as e:
        return APIResponse(success=False, message="네트워크 오류", errors=[str(e)])

def store_consent_to_session(resp: APIResponse[ConsentGenerateOut]) -> None:
    if not (resp.success and resp.data):
        return
    c = resp.data.consents
    st.session_state.update(
        {
            "no_surgery_prognosis": c.prognosis_without_surgery,
            "alternative_methods": c.alternative_treatments,
            "purpose": c.surgery_purpose_necessity_effect,
            "method_1": c.surgery_method_content.overall_description,
            "method_2": c.surgery_method_content.estimated_duration,
            "method_3": c.surgery_method_content.method_change_or_addition,
            "method_4": c.surgery_method_content.transfusion_possibility,
            "method_5": c.surgery_method_content.surgeon_change_possibility,
            "complications": c.possible_complications_sequelae,
            "preop_care": c.emergency_measures,
            "mortality_risk": c.mortality_risk,
            "consent_references": resp.data.references.model_dump(),
        }
    )

# ──────────────────────────────
# 3. 세션 기본값
# ──────────────────────────────
_defaults = {
    "possum_results": None,
    "navigate_to_possum": False,
    "show_possum": False,
    "step": 0,
}
for k, v in _defaults.items():
    st.session_state.setdefault(k, v)

# ──────────────────────────────
# 4. 페이지 본문
# ──────────────────────────────
def page_basic_info() -> None:
    st.set_page_config(layout="wide")

    st.markdown(
        "<h2 style='text-align:center;color:#176d36;'>Reference "
        "Textbook 조회를 위한 기본 정보를 입력해주세요.</h2>",
        unsafe_allow_html=True,
    )
    _l, c, _r = st.columns([1, 6, 1])
    with c, st.form("basic_info_form"):
        # 0. 수술 기본 정보
        st.markdown("### 0. 수술 기본 정보")
        surgery_name = st.selectbox(
            "수술명",
            [
                "복강경 담낭절제",
                "복강경 충수절제",
                "십이지장궤양 천공의 일차봉합",
                "위궤양 천공으로 인한 위절제술",
                "소장 절제 및 문합",
                "회장맹장절제",
                "결장우반절제술",
                "하트만 수술",
                "탐색개복술",
                "서혜부 탈장 수술",
                "절개탈장 수술",
            ],
        )
        c1, c2 = st.columns(2)
        with c1:
            reg_num = st.text_input("등록번호")
        with c2:
            patient_name = st.text_input("환자명")
        c3, c4 = st.columns(2)
        with c3:
            age = st.text_input("나이")
            gender = st.text_input("성별 (M/F)")
        with c4:
            scheduled_date = st.date_input("시행예정일")

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
                "Incisional hernia (절개탈장)",
            ],
        )

        c5, c6 = st.columns(2)
        with c5:
            surgery_site = st.radio(
                "수술부위표시", ["R", "L", "Both", "해당없음"], horizontal=True
            )
        with c6:
            surgery_site_detail = st.text_input(
                "수술부위", placeholder="예: 좌측 하복부 등"
            )

        # 참여 의료진
        st.markdown("**※ 참여 의료진**")
        for i in range(1, 3 + 1):
            cc1, cc2, cc3 = st.columns([2, 2, 3])
            with cc1:
                st.text_input(f"집도의 {i}", key=f"operator_{i}")
            with cc2:
                st.radio(
                    "전문의 여부",
                    ["전문의", "일반의"],
                    key=f"specialist_{i}",
                    horizontal=True,
                    index=0,
                )
            with cc3:
                st.text_input("진료과목", key=f"department_{i}")

        # 환자 특이사항
        st.markdown("### 1. 환자 상태 및 특이사항")
        lft, rgt = st.columns(2)
        with lft:
            past_history = st.radio("과거병력", ["유", "무"], index=1, horizontal=True)
            smoking = st.radio("흡연유무", ["유", "무"], index=1, horizontal=True)
            allergy = st.radio("알레르기", ["유", "무"], index=1, horizontal=True)
            airway_abnormality = st.radio("기도이상", ["유", "무"], index=1, horizontal=True)
            respiratory = st.radio("호흡기질환", ["유", "무"], index=1, horizontal=True)
            medication = st.radio("복용약물", ["유", "무"], index=1, horizontal=True)
            drug_abuse = st.radio("마약복용·약물사고", ["유", "무"], index=1, horizontal=True)
        with rgt:
            diabetes = st.radio("당뇨병", ["유", "무"], index=1, horizontal=True)
            hypertension = st.radio("고혈압", ["유", "무"], index=1, horizontal=True)
            hypotension = st.radio("저혈압", ["유", "무"], index=1, horizontal=True)
            cardiovascular = st.radio("심혈관질환", ["유", "무"], index=1, horizontal=True)
            coagulation = st.radio("혈액응고 질환", ["유", "무"], index=1, horizontal=True)
            renal = st.radio("신장질환", ["유", "무"], index=1, horizontal=True)

            # ▶ POSSUM 점수 계산 버튼
            possum_btn = st.form_submit_button(
                "POSSUM 점수 계산",
                help="수술 위험도를 평가하기 위한 POSSUM 점수를 계산합니다.",
            )
            if possum_btn:
                # 실제 계산 로직은 별도 페이지/모달에서 처리한다고 가정
                st.session_state.navigate_to_possum = True
                st.session_state.show_possum = True
                

            if st.session_state.get("possum_results"):
                st.markdown("**POSSUM 결과**")
                a, b = st.columns(2)
                with a:
                    st.metric(
                        "Mortality Risk",
                        f"{st.session_state.possum_results['mortality']:.2%}",
                    )
                with b:
                    st.metric(
                        "Morbidity Risk",
                        f"{st.session_state.possum_results['morbidity']:.2%}",
                    )

        etc = st.text_area("기타")

        submit_btn = st.form_submit_button("수술 동의서 생성하기")

    # ── 제출 처리
    if submit_btn:
        form = {
            "registration_no": reg_num,
            "patient_name": patient_name,
            "surgery_name": surgery_name,
            "age": age,
            "gender": gender,
            "scheduled_date": scheduled_date,
            "diagnosis": diagnosis,
            "surgical_site_mark": surgery_site,
            "surgical_site_detail": surgery_site_detail,
            "past_history": past_history.lower(),
            "diabetes": diabetes.lower(),
            "smoking": smoking.lower(),
            "hypertension": hypertension.lower(),
            "allergy": allergy.lower(),
            "cardiovascular": cardiovascular.lower(),
            "respiratory": respiratory.lower(),
            "coagulation": coagulation.lower(),
            "medications": medication.lower(),
            "renal": renal.lower(),
            "drug_abuse": drug_abuse.lower(),
            "other": etc,
        }

        for i in range(1, 4):
            form[f"operator_{i}"] = st.session_state.get(f"operator_{i}", "")
            form[f"specialist_{i}"] = st.session_state.get(
                f"specialist_{i}", "전문의"
            )
            form[f"department_{i}"] = st.session_state.get(f"department_{i}", "")

        st.session_state["form_data"] = form
        st.session_state["patient_info"] = {
            "등록번호": reg_num,
            "환자명": patient_name,
            "수술명": surgery_name,
            "나이": age,
            "성별": gender,
            "시행예정일": scheduled_date.strftime("%Y-%m-%d"),
            "진단명": diagnosis,
            "수술부위표시": surgery_site,
            "수술부위": surgery_site_detail,
            "의료진": [
                {
                    "집도의": form[f"operator_{i}"],
                    "전문의여부": form[f"specialist_{i}"],
                    "진료과목": form[f"department_{i}"],
                }
                for i in range(1, 4)
                if form[f"operator_{i}"] and form[f"department_{i}"]
            ],
        }

        api_resp = send_consent_request(create_consent_request(form))
        
        st.subheader("🔍 Raw response from /consent")
        st.json(api_resp.model_dump())
        
        st.subheader("📝 Form payload you just submitted")
        st.json(st.session_state.get("form_data", {}))

        if api_resp.success:
            st.success(api_resp.message)
            store_consent_to_session(api_resp)
            st.session_state.step = 2
        else:
            st.error(api_resp.message)
            for e in api_resp.errors or []:
                st.error(e)
