import streamlit as st
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
