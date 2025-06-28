import streamlit as st

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "안녕하세요 OOO 교수님, 몇 번 항목 수정을 도와드릴까요?"}
    ]
if "chatbot_input_key" not in st.session_state:
    st.session_state.chatbot_input_key = 0

@st.dialog("챗봇 모달", width="large")
def chatbot_modal():
    st.markdown("#### 챗봇")
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
    with st.form("chat_form"):
        prompt = st.text_input(
            "챗봇을 통해 수정을 도와드릴 수 있습니다.",
            key=f"chatbot_input_{st.session_state.chatbot_input_key}",
            label_visibility="collapsed"
        )
        submitted = st.form_submit_button("전송")
        if submitted and prompt:
            st.session_state.messages.append({"role": "user", "content": prompt})
            response = f"관련 내용 보강하였습니다. 수정이 필요하면 말씀해주세요."
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.session_state.chatbot_input_key += 1  # Change the key to clear the input

def page_surgery_info():

    st.set_page_config(layout="wide")

    if st.query_params.get("open_chatbot") == "1":
        st.session_state.open_chatbot = True
        st.query_params.clear()

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

    with col2:

        tabs = st.tabs(["수술 정보", "출처 보기"])

        with tabs[0]:  # 입력 폼 탭
            #st.markdown("## 생성된 수술 정보")

            with st.form("surgery_info_form"):
                
                # Use dividers to create clear, formal sections
                st.markdown("### 2. 예정된 수술/시술/검사를 하지 않을 경우의 예후")
                st.text_area("예상되는 예후를 입력하세요.", key="no_surgery_prognosis", height=120)

                st.divider()
                st.markdown("### 3. 시행 가능한 다른 치료 방법")
                st.text_area("대체 가능한 치료법이 있다면 기재하세요.", key="alternative_methods", height=120)

                st.divider()
                st.markdown("### 4. 수술/시술/검사의 목적, 필요성 및 효과")
                st.text_area("수술의 구체적인 목적과 기대 효과를 설명하세요.", key="purpose", height=120)

                st.divider()
                st.markdown("### 5. 수술/시술/검사의 방법 및 내용")
                
                # Use bold for subheadings within a section
                st.markdown("**1) 수술/시술/검사 과정 전반에 대한 설명**")
                st.text_area("과정 설명", key="method_1", height=120, label_visibility="collapsed")
                
                st.markdown("**2) 수술/시술/검사 추정 소요시간**")
                st.text_area("예상 소요시간", key="method_2", height=120, label_visibility="collapsed")
                
                st.markdown("**3) 수술/시술/검사방법 변경 및 수술/시술/검사범위 추가 가능성**")
                # Use a formal blockquote for long explanatory text
                st.markdown(
                    """
                    > 수술/시술/검사과정에서 환자의 상태에 따라 부득이하게 수술/시술/검사방법이 변경되거나 수술/시술/검사범위가 추가될 수 있습니다. 
                    > 이 경우, 환자 또는 대리인에게 추가로 설명하여야 하는 사항이 있는 경우에는 수술/시술/검사의 시행 전에 이에 대하여 설명하고 동의를 얻도록 합니다. 
                    > 다만, 수술/시술/검사의 시행 도중에 환자의 상태에 따라 미리 설명하고 동의를 얻을 수 없을 정도로 긴급한 변경 또는 추가가 요구되는 경우에는 
                    > 시행 후에 지체 없이 그 사유 및 결과를 환자 또는 대리인에게 설명하도록 합니다.
                    """
                )
                
                st.markdown("**4) 수혈 가능성**")
                st.text_area("수혈 가능성 및 관련 정보", key="method_4", height=120, label_visibility="collapsed")
                
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
                st.markdown("### 6. 발생 가능한 합병증/후유증/부작용 및 대처 계획")
                st.text_area(
                    "예상되는 합병증과 문제 발생 시 대처 방안을 기술하세요.",
                    key="complications",
                    height=120,
                    help="회복과 관련하여 발생할 수 있는 문제와 의료진의 대처 계획을 상세하게 기재합니다."
                )

                st.divider()
                st.markdown("### 7. 수술/시술/검사 전후 환자 준수사항")
                st.markdown("**1) 수술/시술/검사 전**")
                st.text_area(
                    "수술 전 준수사항",
                    key="preop_care",
                    height=120,
                    help="금식, 식이 조절 등 수술 전 환자가 지켜야 할 주의사항입니다."
                )
                st.markdown("**2) 수술/시술/검사 후**")
                st.text_area(
                    "수술 후 준수사항",
                    key="postop_care",
                    height=120,
                    help="수술 후 건강관리에 필요한 사항들입니다."
                )

                st.divider()
                st.markdown("### 8. 기타 추가설명")
                st.text_area(
                    "추가 설명이 필요한 경우 기재하세요.",
                    height=120,
                )

                st.divider()
                
                # A more prominent, action-oriented submit button
                submitted = st.form_submit_button(
                    "수술 내용 확정 및 동의서 출력 단계로",
                    use_container_width=True,
                    type="primary"
                )
                if submitted:
                    st.session_state.step = 2
                    st.rerun()
        with tabs[1]:  # 출처 탭
            #st.markdown("## 📚 각 항목별 출처")

            with st.expander("2. 시행 가능한 다른 치료 방법"):
                st.markdown("""
                - [대한외과학회 대체 치료 지침](https://example.com)
                - 보존적 치료 옵션에 대한 최신 연구 (Lee et al., 2022)
                """)

            with st.expander("3. 수술/시술/검사의 목적, 필요성 및 효과"):
                st.markdown("""
                - NEJM: 수술의 임상적 목적과 효과 분석 (2021)
                - 건강보험심사평가원 치료효과 보고서
                """)

            with st.expander("4. 수술/시술/검사의 방법 및 내용"):
                st.markdown("""
                - [보건복지부 수술절차 설명 가이드](https://example.com)
                - Surgical Techniques Handbook, 3rd ed.
                """)

            with st.expander("5. 수술/시술/검사 중 발생 가능한 사항 (변경/수혈/집도의 변경 등)"):
                st.markdown("""
                - 수술 중 동의서 가이드라인 (대한의사협회)
                - 응급 수혈 및 집도의 교체 관련 법령 자료 (의료법 제24조)
                """)

            with st.expander("6. 발생 가능한 합병증/후유증/부작용 및 대처 계획"):
                st.markdown("""
                - 국내 수술 합병증 통계 보고서 2020
                - 부작용 발생 시 대응 매뉴얼 (서울대병원 내부 문서)
                """)

            with st.expander("7. 수술/시술/검사 전후 환자 준수사항"):
                st.markdown("""
                - 환자 행동요령 안내서 (분당서울대병원)
                - 수술 전 금식, 약물 중단 가이드 (American College of Surgeons)
                """)

            with st.expander("8. 기타 추가설명"):
                st.markdown("""
                - 의료진 판단에 따른 추가 안내사항 (개별 병원 수술안내서 참조)
                - 환자 교육 자료집 부록
                """)
    with col1:
        # 고정된 챗봇 버튼 (HTML + JS)
        st.markdown("""
            <script>
            function openChatbot() {
                const url = new URL(window.location);
                url.searchParams.set('open_chatbot', '1');
                window.location.href = url;
            }
            </script>

            <div style="position: fixed; bottom: 40px; left: 40px;">
                <button onclick="openChatbot()" style="
                    background-color: #176d36;
                    color: white;
                    padding: 12px 18px;
                    font-size: 16px;
                    border: none;
                    border-radius: 20px;
                    cursor: pointer;
                ">
                    💬
                </button>
            </div>
        """, unsafe_allow_html=True)

        # Python 측 감지
        if st.session_state.get("open_chatbot"):
            chatbot_modal()
            st.session_state.open_chatbot = False
