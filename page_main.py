import streamlit as st

def page_main():
    st.title("TrustSurgy")
    st.write("Welcome to the main page.")

    # 페이지 설정
    st.set_page_config(layout="wide")

    # CSS 스타일 (배경색, 폰트 크기 등 조절)
    st.markdown("""
    <style>
        .reportview-container {
            background: #F0F2F6; /* 전체 페이지 배경색 */
        }
        .main-header {
            color: #007bff; /* 파란색 계열 */
            font-size: 2.5em;
            font-weight: bold;
            text-align: center;
            margin-bottom: 20px;
        }
        .sub-header {
            color: #333;
            font-size: 1.5em;
            font-weight: bold;
            margin-bottom: 15px;
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
        .section-background-light-gray {
            background-color: #f8f8f8; /* 아주 연한 회색 배경 */
            padding: 40px 0;
            margin-bottom: 20px;
            border-radius: 10px;
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
            border-radius: 8px;
            padding: 20px;
            margin: 10px 0;
            background-color: #fff;
            box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
            min-height: 180px; /* 리뷰 박스 높이 통일 */
        }
        .review-box p {
            font-size: 0.95em;
            line-height: 1.5;
            margin-bottom: 10px;
        }
        .review-box strong {
            display: block;
            margin-top: 10px;
            color: #555;
        }
    </style>
    """, unsafe_allow_html=True)

    # --- 상단 섹션 (초록색 배경) ---
    st.container()
    with st.container():
        st.markdown('<div class="section-background-green">', unsafe_allow_html=True)
        col1, col2 = st.columns([1, 1.5]) # 왼쪽 텍스트/이미지, 오른쪽 이미지

        with col1:
            st.markdown(
                """
                <h2 style="color: #1a6d3b; font-size: 1.8em; font-weight: bold; text-align: left;">
                    1분 초가 소중한 응급외과의 시간
                </h2>
                <p style="font-size: 1.1em; line-height: 1.6;">
                    SurgiForm은 응급외과 의사의 수술기록 작성을 위한 솔루션입니다.
                </p>
                """, unsafe_allow_html=True
            )
            # 이미지 대신 더미 placeholder
            st.image("https://via.placeholder.com/400x200?text=SurgiForm+Documents", use_container_width='auto') # 문서 이미지
        with col2:
            # 사람과 컴퓨터 이미지
            st.image("https://via.placeholder.com/500x300?text=Doctor+and+Computer", use_container_width='auto')
            st.markdown(
                """
                <div style="text-align: right; margin-top: 20px;">
                    <a href="#" class="button-green">수술폼 작성해보기 >></a>
                </div>
                """, unsafe_allow_html=True
            )
        st.markdown('</div>', unsafe_allow_html=True)


    # --- Why SurgiForm? 섹션 (흰색 배경) ---
    st.container()
    with st.container():
        st.markdown('<div class="section-background-white" style="padding-top: 60px; padding-bottom: 60px;">', unsafe_allow_html=True)
        st.markdown(
            """
            <h2 style="text-align: center; color: #1a6d3b; font-size: 2em; font-weight: bold; margin-bottom: 50px;">
                Why SurgiForm?
            </h2>
            <div style="text-align: center; font-size: 1.2em; line-height: 1.8;">
                <p>다양한 수술로 인해 정해진 양식이 없는 응급외과의의 수술 기록서</p>
                <p>위급한 상황 속 반복되는 업무로 인한 실수 및 누락</p>
                <p>개별 환자의 정보에 맞춰진 레퍼런스 참고 및 사전 파악</p>
            </div>
            """, unsafe_allow_html=True
        )
        st.markdown('</div>', unsafe_allow_html=True)

    # --- What is SurgiForm? 섹션 (연한 회색 배경) ---
    st.container()
    with st.container():
        st.markdown('<div class="section-background-light-gray" style="padding-top: 60px; padding-bottom: 60px;">', unsafe_allow_html=True)
        st.markdown(
            """
            <h2 style="text-align: center; color: #1a6d3b; font-size: 2em; font-weight: bold; margin-bottom: 50px;">
                What is SurgiForm?
            </h2>
            """, unsafe_allow_html=True
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(
                """
                <div class="icon-box">
                    <img src="https://via.placeholder.com/100x100?text=STEP+1+Icon" alt="Step 1 Icon">
                    <p><b>STEP 1</b></p>
                    <p>간단한 수술 정보 입력</p>
                </div>
                """, unsafe_allow_html=True
            )
        with col2:
            st.markdown(
                """
                <div class="icon-box">
                    <img src="https://via.placeholder.com/100x100?text=STEP+2+Icon" alt="Step 2 Icon">
                    <p><b>STEP 2</b></p>
                    <p>빠르고 정확한 수술 기록서 생성</p>
                </div>
                """, unsafe_allow_html=True
            )
        with col3:
            st.markdown(
                """
                <div class="icon-box">
                    <img src="https://via.placeholder.com/100x100?text=STEP+3+Icon" alt="Step 3 Icon">
                    <p><b>STEP 3</b></p>
                    <p>PDF 출력 및 진료 & 저장</p>
                </div>
                """, unsafe_allow_html=True
            )
        st.markdown('</div>', unsafe_allow_html=True)

    # --- SurgiForm 로고 및 기능 설명 섹션 (흰색 배경) ---
    st.container()
    with st.container():
        st.markdown('<div class="section-background-white" style="padding-top: 60px; padding-bottom: 60px;">', unsafe_allow_html=True)
        st.markdown(
            """
            <div style="text-align: center; margin-bottom: 40px;">
                <img src="https://via.placeholder.com/200x80?text=S+J+Logo" alt="SurgiForm Logo" style="width: 200px; height: auto;">
            </div>
            <h2 style="text-align: center; color: #1a6d3b; font-size: 2em; font-weight: bold; margin-bottom: 50px;">
                How SurgiForm?
            </h2>
            """, unsafe_allow_html=True
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(
                """
                <div class="icon-box">
                    <img src="https://via.placeholder.com/80x80?text=Icon1" alt="Icon 1">
                    <p>교수님들에게 익숙한</p>
                    <p><b>정보 입력 & 출력 템플릿</b></p>
                </div>
                """, unsafe_allow_html=True
            )
        with col2:
            st.markdown(
                """
                <div class="icon-box">
                    <img src="https://via.placeholder.com/80x80?text=Icon2" alt="Icon 2">
                    <p>환자 데이터를 학습한 정확하고 방대한</p>
                    <p><b>연구 데이터베이스</b></p>
                </div>
                """, unsafe_allow_html=True
            )
        with col3:
            st.markdown(
                """
                <div class="icon-box">
                    <img src="https://via.placeholder.com/80x80?text=Icon3" alt="Icon 3">
                    <p>LLM을 통한 빠르고 핵심 되는</p>
                    <p><b>문서 생성</b></p>
                </div>
                """, unsafe_allow_html=True
            )
        st.markdown('</div>', unsafe_allow_html=True)

    # --- 병원 리뷰 섹션 (연한 회색 배경) ---
    st.container()
    with st.container():
        st.markdown('<div class="section-background-light-gray" style="padding-top: 60px; padding-bottom: 60px;">', unsafe_allow_html=True)
        st.markdown(
            """
            <h2 style="text-align: center; color: #1a6d3b; font-size: 2em; font-weight: bold; margin-bottom: 50px;">
                약 OO개 병원의 응급외과가 선택한 'SurgiForm'
            </h2>
            """, unsafe_allow_html=True
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(
                """
                <div class="review-box">
                    <p>"수술 기록서 작성에 걸리는 시간이 획기적으로 줄어들었습니다."</p>
                    <strong>서울 OO병원 외과 교수</strong>
                </div>
                """, unsafe_allow_html=True
            )
        with col2:
            st.markdown(
                """
                <div class="review-box">
                    <p>"응급 상황에서 놓칠 수 있는 부분을 빠르게 파악하고 기록할 수 있어 좋습니다."</p>
                    <strong>부산 OO병원 외과 교수</strong>
                </div>
                """, unsafe_allow_html=True
            )
        with col3:
            st.markdown(
                """
                <div class="review-box">
                    <p>"최신 정보를 바탕으로 입력된 수술 정보를 분석하여 정확한 수술 기록을 제공합니다."</p>
                    <strong>대구 OO병원 외과 교수</strong>
                </div>
                """, unsafe_allow_html=True
            )

        st.markdown(
            """
            <div style="text-align: center; margin-top: 50px;">
                <a href="#" class="button-green">SurgiForm 시작하기 >></a>
            </div>
            """, unsafe_allow_html=True
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Display the image (adjust the path to your image)
    st.image("assets/images/main.png", use_container_width=True)
    
    # Add a button
    if st.button("시작하기"):
        # You can set a session state or perform an action here
        st.success("시작하기 버튼이 눌렸습니다!")
        return True
    return False
