import streamlit as st

def page_main():
    # 페이지 설정
    st.set_page_config(layout="wide")

    st.image("assets/images/main_p.png", use_container_width=True) # 문서 이미지

    # CSS 스타일 (배경색, 폰트 크기 등 조절)

    st.markdown("""
        <style>
        body {
            background: linear-gradient(90deg, #0e7c3c, #a0d0b4);
        }
        </style>
        <div class="gradient-background"></div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined" rel="stylesheet" />

    <style>
        .block-container {
            padding: 0rem;
            max-width: 100% !important;
            padding-bottom: 2rem;
        }
        .reportview-container {
            background: #F0F2F6; /* 전체 페이지 배경색 */
        }
        .text-content {
            font-size: 1.1em;
            line-height: 1.6;
        }
        .section-background-green {
            background-color: #e6ffe6; /* 연한 초록색 배경 */
            padding: 40px 0;
            margin-bottom: 20px;
            border-radius: 10px;
        }
        .section-background-light-green {
            background-color: #DCEAE1; /* 연한 초록색 배경 */
            padding: 20px 0;
            margin-bottom: 20px;
            border-radius: 0px;
        }
        .section-background-white {
            background-color: #ffffff; /* 흰색 배경 */
            padding: 40px 0;
            margin-bottom: 20px;
            border-radius: 10px;
        }
        .button-green {
            display: inline-block;
            background-color: #1a6d3b; /* 어두운 초록색 버튼 */
            color: white;
            padding: 12px 25px;
            border-radius: 5px;
            text-decoration: none;
            font-weight: bold;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        .button-green:hover {
            background-color: #218c4b; /* 호버 시 약간 밝게 */
        }
        .material-symbols-outlined {
        font-variation-settings:
            'FILL' 0,
            'wght' 400,
            'GRAD' 0,
            'opsz' 24;
        font-size: 48px;
        color: #002366;
        }
        .icon-box {
            text-align: center;
            margin-bottom: 20px;
        }
        .icon-box img {
            width: 100px; /* 아이콘 이미지 크기 */
            height: auto;
            margin-bottom: 10px;
        }
        .review-box {
            border: 1px solid #ddd;
            border-radius: 20px;
            padding: 20px;
            margin: 10px 0;
            background-color: #DCEAE1;
            box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
            min-height: 180px; /* 리뷰 박스 높이 통일 */
        }
        .review-box p {
            font-size: 0.95em;
            line-height: 1.5;
            margin-bottom: 10px;
        }
        .review-box strong {
            padding-bottom: 10px;
            display: block;
            margin-top: 10px;
            color: #555;
        }
    </style>
    """, unsafe_allow_html=True)

    # # --- 상단 섹션 (초록색 배경) ---
    # st.container()
    # with st.container():
    #     st.markdown('<div class="section-background-green">', unsafe_allow_html=True)
    #     col1, col2 = st.columns([1, 1.5]) # 왼쪽 텍스트/이미지, 오른쪽 이미지

    #     with col1:
    #         st.markdown(
    #             """
    #             <h2 style="color: #1a6d3b; font-size: 1.8em; font-weight: bold; text-align: left;">
    #                 1분 1초가 소중한 응급외과의 시간
    #             </h2>
    #             <p style="font-size: 1.1em; line-height: 1.6;">
    #                 수술동의서를 작성하는 가장 빠르고 정확한 방법.
    #                 SurgiForm을 통해 환자와 의료진 모두를 위한 수술동의서를 받아보세요.
    #             </p>
    #             """, unsafe_allow_html=True
    #         )
    #         # 이미지 대신 더미 placeholder
    #         st.image("https://via.placeholder.com/400x200?text=SurgiForm+Documents", use_container_width='auto') # 문서 이미지
    #     with col2:
    #         # 사람과 컴퓨터 이미지
    #         st.image("https://via.placeholder.com/500x300?text=Doctor+and+Computer", use_container_width='auto')
    #         st.markdown(
    #             """
    #             <div style="text-align: right; margin-top: 20px;">
    #                 <a href="#" class="button-green">수술폼 작성해보기 >></a>
    #             </div>
    #             """, unsafe_allow_html=True
    #         )
    #     st.markdown('</div>', unsafe_allow_html=True)


    # --- Why SurgiForm? 섹션 (흰색 배경) ---
    st.container()
    with st.container():
        #st.markdown('<div class="section-background-white" style="padding-top: 60px; padding-bottom: 60px;">', unsafe_allow_html=True)

        st.markdown(
            """
            <h2 style="text-align: center; color: #1a6d3b; font-size: 2em; font-weight: bold; margin-bottom: 60px;">
                Why SurgiForm?
            </h2>
            """,
            unsafe_allow_html=True
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("""
                <div style="text-align: center;">
                <div style="text-align: center; font-size: 1.1em; font-weight: bold; line-height: 1.6;">
                    <div>다양한 종류의 수술로 인해</div><div style="color: #1a237e;">정해진 양식이 없는<br></div><div>응급외상외과의 수술 동의서</div>
                </div>
                <div style="height: 47px;"></div>
                <div style="width: 2px; height: 80px; margin: 0 auto; background-color: #cccccc;"></div>
                <div style="height: 30px;"></div>
                <span class="material-symbols-outlined">edit_note</span>
                <div style="text-align: center; font-size: 1.1em; font-weight: bold; line-height: 1.6;">
                <div>교수님들에게 익숙한</div>
                <div style="color: #1a237e;"><b>정보 입력 & 출력 템플릿</b></div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div style="text-align: center;">
                <p style="font-weight: bold; font-size: 1.1em;">개별 환자 맞춤형 수술 관련<br>연구 자료 반영을 위한<span style="color:#1a237e"><br>최신 레퍼런스 참고 시간 부족</span></p>
                <div style="height: 30px;"></div>
                <div style="width: 2px; height: 80px; margin: 0 auto; background-color: #cccccc;"></div>
                <div style="height: 30px;"></div>
                <span class="material-symbols-outlined">menu_book</span>
                <div style="text-align: center; font-size: 1.1em; font-weight: bold; line-height: 1.6;">
                <div>최신 데이터를 학습한</div>
                <div style="color: #1a237e;"><b>정확하고 방대한 연구 데이터베이스</b></div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown("""
            <div style="text-align: center;">
                <p style="font-weight: bold; font-size: 1.1em;">위급한 상황 속<br>반복되는 업무로 인한<br><span style="color:#1a237e">실수 및 누락</span></p>
                <div style="height: 30px;"></div>
                <div style="width: 2px; height: 80px; margin: 0 auto; background-color: #cccccc;"></div>
                <div style="height: 30px;"></div>
                <span class="material-symbols-outlined">description</span>
                <div style="text-align: center; font-size: 1.1em; font-weight: bold; line-height: 1.6;">
                <div>LLM을 통한</div>
                <div style="color: #1a237e;"><b>빠르고 빠짐없는 문서 생성</b></div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)


    # --- What is SurgiForm? 섹션 (연한 회색 배경) ---
    st.image("assets/images/main_w.png", use_container_width=True) # 문서 이미지

    st.container()
    with st.container():
        st.markdown('<div class="section-background-white" style="padding:60px 0;">', unsafe_allow_html=True)
        st.markdown("""
            <h2 style="text-align: center; color: #1a6d3b; 
                    font-size: 2em; font-weight: bold; margin-bottom: 50px;">
                What is SurgiForm?
            </h2>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("""
                <div style="text-align: center;">
                    <p style="font-weight: bold; margin: 4px 0;">STEP 1</p>
                    <p>간단한 수술 정보 입력</p>
                    <span class="material-symbols-outlined">desktop_windows</span>
                </div>
            """, unsafe_allow_html=True)
            #st.image("assets/images/step11.png", width=100)

        with col2:
            st.markdown("""
                <div style="text-align: center;">
                    <p style="font-weight: bold; margin: 4px 0;">STEP 2</p>
                    <p>빠르고 정확한 수술 기록서 생성</p>
                    <span class="material-symbols-outlined">assignment_turned_in</span>
                </div>
            """, unsafe_allow_html=True)
            #st.image("assets/images/step2.png", width=100)

        with col3:
            st.markdown("""
                <div style="text-align: center;">
                    <p style="font-weight: bold; margin: 4px 0;">STEP 3</p>
                    <p>PDF 출력 및 진료 & 저장</p>
                    <span class="material-symbols-outlined">description</span>
                </div>
            """, unsafe_allow_html=True)
            #st.image("assets/images/step3.png", width=100)

        st.markdown('</div>', unsafe_allow_html=True)

    # --- 병원 리뷰 섹션 (연한 회색 배경) ---
    st.container()
    with st.container():
        st.markdown('<div class="section-background-white" style="padding-top: 60px; padding-bottom: 60px;">', unsafe_allow_html=True)
        st.markdown(
            """
            <h2 style="text-align: center; color: #1a6d3b; font-size: 2em; font-weight: bold; margin-bottom: 50px;">
                약 OO개 병원의 응급외과가 선택한 'SurgiForm'
            </h2>
            """, unsafe_allow_html=True
        )

        col1, col2, col3, col4, col5 = st.columns([1, 2, 2, 2, 1])

        with col2:
            st.markdown(
                """
                <div class="review-box">
                    <strong>"수술 기록서 작성에 걸리는 시간이 획기적으로 줄어들었습니다."</strong>
                    <p>서울 OO병원 외과 교수</p>
                </div>
                """, unsafe_allow_html=True
            )
        with col3:
            st.markdown(
                """
                <div class="review-box">
                    <strong>"응급 상황에서 놓칠 수 있는 부분을 빠르게 파악하고 기록할 수 있어 좋습니다."</strong>
                    <p>부산 OO병원 외과 교수</p>
                </div>
                """, unsafe_allow_html=True
            )
        with col4:
            st.markdown(
                """
                <div class="review-box">
                    <strong>"최신 정보를 바탕으로 입력된 수술 정보를 분석하여 정확한 수술 기록을 제공합니다."</strong>
                    <p>대구 OO병원 외과 교수</p>
                </div>
                """, unsafe_allow_html=True
            )

        _, center, _ = st.columns([2.5, 1, 2])
        with center:
            if st.button("SurgiForm 시작하기", type="primary"):
                st.success("시작하기 버튼이 눌렸습니다!")
                return True
            return False