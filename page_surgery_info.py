import streamlit as st
from components.buttons import big_green_button
from components.chatbot_popup import chatbot_modal
# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "안녕하세요 OOO 교수님, 몇 번 항목 수정을 도와드릴까요?"}
    ]

# Define the chatbot modal dialog function
@st.dialog("챗봇 모달", width="large")
def chatbot_modal():
    st.markdown("#### 챗봇")
    
    # Display chat messages
    for message in st.session_state.messages:
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
    
    # Chat input
    prompt = st.text_input("챗봇을 통해 수정을 도와드릴 수 있습니다.", key="chatbot_input", label_visibility="collapsed")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Replace with your chatbot API call here
        response = f"관련 내용 보강하였습니다. 수정이 필요하면 말씀해주세요."
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

def page_surgery_info():
    st.set_page_config(layout="wide")
    st.markdown("""
        <h2 style='text-align:center; color:#176d36; margin: 0 0 20px 0'>Reference Textbook을 기반으로 작성된 수술 관련 정보입니다.<br>확인 후 수정사항이 있으면 반영한 후 확정해주세요.</h2>
    """, unsafe_allow_html=True)
    
    with st.form("surgery_info_form"):
        section_labels = [
            "2. 예정된 수술을 하지 않을 경우의 예후",
            "3. 예정된 수술 이외의 시행 가능한 다른 방법",
            "4. 수술의 목적/필요성/효과",
            "5. 수술의 방법 및 내용",
            "6. 발생 가능한 합병증/후유증/부작용",
            "7. 문제 발생시 조치사항",
            "8. 진단/수술 관련 사망 위험성"
        ]
        text_keys = [
            "no_surgery_prognosis",
            "alternative_methods",
            "purpose",
            "method",
            "complications",
            "actions_on_problems",
            "mortality_risk"
        ]
        answers = {}
        for idx, (label, key) in enumerate(zip(section_labels, text_keys), start=2):
            st.markdown(f"<div style='font-weight:bold; margin-top:28px; margin-bottom:4px;'>{label}</div>", unsafe_allow_html=True)
            answers[key] = st.text_area(
                label="",
                value="Reference 조회 후 생성된 수술 관련 정보입니다.\n수정 사항이 있을 경우 반영하실 수 있습니다.",
                height=120,
                key=f"surgery_info_{key}"
            )

        submitted = st.form_submit_button("수술 내용 확정하기", use_container_width=True)
        if submitted:
            # Save answers if needed
            for key, value in answers.items():
                st.session_state[key] = value
            st.session_state.step = 2
            st.rerun()

    # Add CSS for floating chatbot button
    st.markdown("""
    <style>
    .floating-chat-btn {
        position: fixed;
        bottom: 30px;
        right: 30px;
        z-index: 1000;
        background: #338a3e;
        color: white;
        border-radius: 50%;
        width: 60px;
        height: 60px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 4px 16px rgba(51,138,62,0.3);
        font-size: 1.8em;
        cursor: pointer;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

    # Floating chatbot button
    if st.button("💬", key="open_chatbot", help="챗봇 열기"):
        chatbot_modal()
