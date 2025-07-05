import streamlit as st
from groq import Groq
import os
from typing import List, Dict
import requests

from pydantic import BaseModel
from pydantic import Field



def initialize_session_state():
    """Initialize session state variables"""
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "안녕하세요 장재율 교수님, 몇 번 항목 수정을 도와드릴까요?"}
        ]
    if "chatbot_input_key" not in st.session_state:
        st.session_state.chatbot_input_key = 0

# Initialize Groq client
@st.cache_resource
def get_groq_client():
    api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
    if not api_key:
        st.error("Groq API key not found. Please set GROQ_API_KEY in secrets or environment variables.")
        return None
    return Groq(api_key=api_key)

def get_streaming_response(messages: List[Dict[str, str]], response_placeholder) -> str:
    """Get streaming response from Groq API with real-time updates"""
    client = get_groq_client()
    if not client:
        return "죄송합니다. API 연결에 문제가 있습니다."
    
    try:
        # Convert messages to Groq format and add system prompt
        groq_messages = [
            {
                "role": "system", 
                "content": """당신은 의료진을 위한 수술 동의서 작성 도우미입니다. 
                다음 역할을 수행해주세요:
                1. 수술 관련 정보 수정 및 보완 제안
                2. 의학적으로 정확하고 환자가 이해하기 쉬운 설명 제공
                3. 동의서 작성 시 놓칠 수 있는 중요한 사항 알림
                4. 전문적이면서도 친근한 톤으로 대화
                항상 한국어로 응답하고, 의료진에게 존댓말을 사용해주세요."""
            }
        ]
        
        # Add conversation history
        recent_messages = messages[-10:] if len(messages) > 10 else messages
        for msg in recent_messages:
            groq_messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        # Use compound-beta model
        completion = client.chat.completions.create(
            model="compound-beta",
            messages=groq_messages,
            temperature=0.7,
            max_tokens=1000,
            top_p=1,
            stream=True,
            stop=None,
        )
        
        # Stream and update in real-time
        response_text = ""
        for chunk in completion:
            if chunk.choices[0].delta.content:
                response_text += chunk.choices[0].delta.content
                
                # Update the placeholder with current response
                response_placeholder.markdown(f"""
                <div style='background:#e8f5e9;color:#176d36;padding:10px 14px;border-radius:12px 12px 12px 2px;margin-bottom:8px;max-width:85%;'>
                    {response_text}
                </div>
                """, unsafe_allow_html=True)
        
        if not response_text:
            return "응답을 받지 못했습니다. 다시 시도해주세요."
            
        return response_text
        
    except Exception as e:
        error_message = str(e)
        
        if "rate_limit" in error_message.lower():
            return "⏰ API 사용량 한도를 초과했습니다. 잠시 후 다시 시도해주세요."
        elif "authentication" in error_message.lower() or "401" in error_message:
            return "🔑 API 키 인증에 문제가 있습니다. 설정을 확인해주세요."
        elif "model_decommissioned" in error_message.lower():
            return "🚫 사용하려는 모델이 더 이상 지원되지 않습니다."
        else:
            return f"❌ API 오류가 발생했습니다: {error_message}"

@st.dialog("챗봇", width="large")
def chatbot_modal():
    # Initialize session state at the beginning of the modal
    initialize_session_state()
    
    st.markdown("#### AI 수술 동의서 작성 도우미")
    
    # ✅ DISPLAY CHAT MESSAGES
    for i, message in enumerate(st.session_state.messages):
        if message["role"] == "user":
            st.markdown(f"""
            <div style='background:#e3f2fd;color:#0d47a1;padding:10px 14px;border-radius:12px 12px 2px 12px;margin-bottom:8px;max-width:85%;margin-left:auto;'>
                {message['content']}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style='background:#e8f5e9;color:#176d36;padding:10px 14px;border-radius:12px 12px 12px 2px;margin-bottom:8px;max-width:85%;'>
                {message['content']}
            </div>
            """, unsafe_allow_html=True)
    
    # ✅ CHAT INPUT FORM - ONLY THIS USES st.rerun()
    with st.form("chat_form"):
        prompt = st.text_input(
            "AI를 통해 실시간 정보 검색과 함께 수정을 도와드릴 수 있습니다.",
            key=f"chatbot_input_{st.session_state.chatbot_input_key}",
            label_visibility="collapsed",
            placeholder="예: '최신 수술 가이드라인을 검색해서 합병증 설명을 보완해주세요'"
        )
        
        col1, col2 = st.columns([3, 1])
        with col2:
            submitted = st.form_submit_button("전송", use_container_width=True)
        
        if submitted and prompt:
            # Add user message
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Create placeholder for streaming response
            response_placeholder = st.empty()
            
            # Get streaming response and update in real-time
            with st.spinner("AI가 실시간으로 답변을 생성하고 있습니다..."):
                response = get_streaming_response(st.session_state.messages, response_placeholder)
            
            # Add final response to session state
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.session_state.chatbot_input_key += 1
            # ✅ ONLY RERUN FOR FORM SUBMISSION TO CLEAR INPUT



# Use this before creating your Pydantic model:
# cleaned_references = convert_references_to_strings(st.session_state.get("consent_references", {}))
# consent_output = ConsentGenerateOut(references=cleaned_references, ...)

    
    

def page_surgery_info():
    st.set_page_config(layout="wide")
    # Initialize session state at the beginning of the page
    initialize_session_state()
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

    st.markdown(
        "<h2 style='text-align:center; color:#176d36; margin: 0 0 20px 0'>Reference Textbook을 기반으로 작성된 수술 관련 정보입니다.<br>확인 후 수정사항이 있으면 반영한 후 확정해주세요.</h2>",
        unsafe_allow_html=True
    )
    col1, col2, col3 = st.columns([1, 6, 1])
    with col2:  # Place all content in the middle column

        tabs = st.tabs(["수술 정보", "출처 보기"])

        with tabs[0]:  # 입력 폼 탭 
            with st.form("surgery_info_form"):
                # Use dividers to create clear, formal sections
                st.markdown("### 2. 예정된 수술/시술/검사를 하지 않을 경우의 예후")
                st.text_area("", 
                            value=st.session_state.get("no_surgery_prognosis", ""), 
                            key="no_surgery_prognosis", 
                            height=120)
                
                st.divider()
                st.markdown("### 3. 예정된 수술 이외의 시행 가능한 다른 방법")
                st.text_area("", 
                            value=st.session_state.get("alternative_methods", ""), 
                            key="alternative_methods", 
                            height=120)
                
                st.divider()
                st.markdown("### 4. 수술 목적/필요/효과")
                st.text_area("", 
                            value=st.session_state.get("purpose", ""), 
                            key="purpose", 
                            height=120)
                
                st.divider()
                st.markdown("### 5. 수술 방법 및 내용")
                
                st.markdown("**1) 수술 과정 전반에 대한 설명**")
                st.text_area("과정 설명", 
                            value=st.session_state.get("method_1", ""), 
                            key="method_1", 
                            height=120, 
                            label_visibility="collapsed")
                
                st.markdown("**2) 수술 추정 소요시간**")
                st.text_area("예상 소요시간", 
                            value=st.session_state.get("method_2", ""), 
                            key="method_2", 
                            height=120, 
                            label_visibility="collapsed")
                
                st.markdown("**3) 수술 방법 변경 및 수술 추가 가능성**")
                st.markdown(
                    """
                    > 수술/시술/검사과정에서 환자의 상태에 따라 부득이하게 수술/시술/검사방법이 변경되거나 수술/시술/검사범위가 추가될 수 있습니다. 
                    > 이 경우, 환자 또는 대리인에게 추가로 설명하여야 하는 사항이 있는 경우에는 수술/시술/검사의 시행 전에 이에 대하여 설명하고 동의를 얻도록 합니다. 
                    > 다만, 수술/시술/검사의 시행 도중에 환자의 상태에 따라 미리 설명하고 동의를 얻을 수 없을 정도로 긴급한 변경 또는 추가가 요구되는 경우에는 
                    > 시행 후에 지체 없이 그 사유 및 결과를 환자 또는 대리인에게 설명하도록 합니다.
                    """
                )

                
                st.markdown("**4) 수혈 가능성**")
                st.text_area("수혈 가능성 및 관련 정보",
                            value=st.session_state.get("method_4", ""),
                            key="method_4",
                            height=120,
                            label_visibility="collapsed")
                
                st.markdown("**5) 집도의 변경 가능성**")
                st.markdown(
                    """
                    > 위에 기재된 참여 의료진이 있는 경우 수술/시술/검사과정에서 환자의 상태 또는 의료기관의 사정(응급환자 진료, 주치의의 질병·출장 등)에 따라 
                    > 부득이하게 주치의(집도의)가 변경될 수 있습니다. 이 경우 시행 전에 환자 또는 대리인에게 구체적인 변경사유를 설명하고 동의를 얻을 예정입니다. 
                    > 다만, 시행 도중에 미리 설명하고 동의를 얻을 수 없을 정도로 긴급한 변경이 요구되는 경우에는 시행 후에 
                    > 지체 없이 구체적인 변경 사유 및 시행결과를 환자 또는 대리인에게 설명하도록 합니다.
                    """
                )

                st.divider()
                st.markdown("### 6. 발생 가능한 합병증/후유증/부작용")
                st.text_area("",
                            value=st.session_state.get("complications", ""),
                            key="complications",
                            height=120)
                
                st.divider()
                st.markdown("### 7. 문제 발생시 조치사항")
                st.text_area("",
                            value=st.session_state.get("preop_care", ""),
                            key="preop_care",
                            height=120)
                
                st.divider()
                st.markdown("### 8. 진단/수술 관련 사망 위험성")
                st.text_area("",
                            value=st.session_state.get("mortality_risk", ""),
                            key="mortality_risk",
                            height=120)
                
                st.divider()
                
                submitted = st.form_submit_button(
                    "수술 내용 확정 및 동의서 출력 단계로",
                    use_container_width=True,
                    type="primary"
                )
                if submitted:
                    st.session_state.step = 2
                    st.rerun()
        with tabs[1]:  # 입력 폼 탭 
            with st.form("surgery_o_form"):
                # Medical Reference Sources Section
                st.markdown("### Medical Reference Sources")
                all_sources = [
                    "Lower urinary tract symptoms in males - https://www.uptodate.com/contents/lower-urinary-tract-symptoms-in-males",
"Evaluation of epistaxis in children - https://www.uptodate.com/contents/evaluation-of-epistaxis-in-children",
"Sigmoid volvulus - https://www.uptodate.com/contents/sigmoid-volvulus",
"Large bowel obstruction - https://www.uptodate.com/contents/large-bowel-obstruction",
"Overview of endometrial ablation - https://www.uptodate.com/contents/overview-of-endometrial-ablation",
"Diversion colitis: Clinical manifestations and diagnosis - https://www.uptodate.com/contents/diversion-colitis-clinical-manifestations-and-diagnosis",
"Surgical female pelvic anatomy: Uterus and related structures - https://www.uptodate.com/contents/surgical-female-pelvic-anatomy-uterus-and-related-structures",
"Approach to minimal bright red blood per rectum in adults - https://www.uptodate.com/contents/approach-to-minimal-bright-red-blood-per-rectum-in-adults",
"Overview of colon resection - https://www.uptodate.com/contents/overview-of-colon-resection",
"Procedure-specific and late complications of open aortic surgery in adults - https://www.uptodate.com/contents/procedure-specific-and-late-complications-of-open-aortic-surgery-in-adults",
"Endometriosis: Clinical manifestations and diagnosis of rectovaginal or bowel disease - https://www.uptodate.com/contents/endometriosis-clinical-manifestations-and-diagnosis-of-rectovaginal-or-bowel-disease",
"Cecal volvulus - https://www.uptodate.com/contents/cecal-volvulus",
"Practical aspects of red blood cell transfusion in adults: Storage, processing, modifications, and infusion - https://www.uptodate.com/contents/practical-aspects-of-red-blood-cell-transfusion-in-adults-storage-processing-modifications-and-infusion",
"Treatments for male infertility - https://www.uptodate.com/contents/treatments-for-male-infertility",
"Acute colonic diverticulitis: Surgical management - https://www.uptodate.com/contents/acute-colonic-diverticulitis-surgical-management",
"Radiation proctitis: Clinical manifestations, diagnosis, and management - https://www.uptodate.com/contents/radiation-proctitis-clinical-manifestations-diagnosis-and-management",
"Diversion colitis: Management - https://www.uptodate.com/contents/diversion-colitis-management",
"Counseling in abortion care - https://www.uptodate.com/contents/counseling-in-abortion-care",
"Acute simple cystitis in children older than two years and adolescents: Management - https://www.uptodate.com/contents/acute-simple-cystitis-in-children-older-than-two-years-and-adolescents-management",
"Causes of scrotal pain in children and adolescents - https://www.uptodate.com/contents/causes-of-scrotal-pain-in-children-and-adolescents",
"Overview of burn injury in older patients - https://www.uptodate.com/contents/overview-of-burn-injury-in-older-patients",
"Induced fetal demise - https://www.uptodate.com/contents/induced-fetal-demise",
"Transabdominal ultrasonography of the small and large intestine - https://www.uptodate.com/contents/transabdominal-ultrasonography-of-the-small-and-large-intestine",
"Surgical resection of primary colon cancer - https://www.uptodate.com/contents/surgical-resection-of-primary-colon-cancer",
"Clinical manifestations and diagnosis of cholangiocarcinoma - https://www.uptodate.com/contents/clinical-manifestations-and-diagnosis-of-cholangiocarcinoma"

                ]
                st.text_area("Sources", 
                    value="\n".join(all_sources), 
                    height=800, 
                    key="medical_sources")

                st.divider()

                st.form_submit_button(label="Next Page")

    

        




    st.markdown("""
    <style>
    div[data-testid="stButton"] {
        position: fixed;
        bottom: 20px;
        left: 20px;
        z-index: 9999;
    }
    </style>
    """, unsafe_allow_html=True)

    if st.button("AI 챗봇과 상담하기"):
        chatbot_modal()
