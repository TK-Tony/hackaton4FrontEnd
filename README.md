You can download all relevant libraries through this command: 

pip install -r requirements.txt

---

# Team4 – SurgiForm

안녕하세요, 저희는 서울대학교 의과대학 경제경영학회 MD Winners가 주최한 **2025 PIEthon 3.0 해커톤**에 참여한 **Team4**입니다.  
저희는 장재율 교수님과 함께하며, 늘 예상치 못했던 다양한 수술 상황에서 빠르고 정확하게 수술 동의서를 작성해야 하는 외상응급의학과의 문제를 해결하고자 **SurgiForm**을 개발하였습니다.

---

## 🏆 대회 및 팀 정보
- **대회**: 2025 PIEthon 3.0 해커톤  
- **주최**: 서울대학교 의과대학 경제경영학회 MD Winners  
- **멘토**: 장재율 교수님
- **팀원**: 손종현, 김민준, 박현, 성현주, 신서원, 임정묵, 정인서

---

## 💡 주요 기능 & 기술적 주안점
1. **메인 페이지**  
   - SurgiForm의 필요성 및 해결 방안 소개  
2. **기본 정보 입력 페이지**  
   - 환자·수술 기본 정보 입력  
   - POSSUM SCORE 계산기 탑재
   - 직관적이고 쉬운 UI  
3. **수술 정보 입력 페이지**  
   - 두 번의 LLM 호출  
     1. UpToDate 기반 Textbook에서 최신 전문 정보 조회  
     2. 조회된 정보를 “쉬운 말”로 재설명  
   - 출처명시 ✓, 수정·보완 가능 ✓  
   - 추가 수정 시 **챗봇** 기능 활용 가능  
4. **수술동의서 설명 및 서명 페이지**  
   - 수술 설명 시 필요에 따라 **캔버스** 추가 가능  
   - 추후 **녹음 기능** 계획 중  
5. **수술동의서 PDF 출력 페이지**  
   - 확정된 동의서를 **PDF** 형식으로 변환·저장  

---

## 🚀 페이지별 소개

### 1. 메인 페이지
메인 페이지는 외상응급의학과에 SurgiForm이 필요한 이유와 이를 어떠한 기술을 통해 해결하였는지를 소개하는 페이지입니다.  
1박 2일 동안 짧게 진행된 해커톤인 만큼 Streamlit을 사용하여 빠르게 제작되었기에 디자인에 부족한 점이 있지만, 후속 개발에는 다른 프레임워크를 사용하여 보완할 예정입니다.
<img width="1000" alt="image" src="https://github.com/user-attachments/assets/b06f8220-2b78-4914-8121-207a4050a18f" />

---

### 2. 기본 정보 입력 페이지
Reference 기반의 수술 정보를 생성하기 위해, 수술과 환자에 관한 가장 기본적인 정보들을 입력하는 페이지입니다.  
현재의 수술동의서와 굉장히 유사한 형태의 UI로 제작되어 사용자(의사 선생님)가 익숙하고 빠르게 작성할 수 있도록 하였습니다.  
<img width="1000" alt="image" src="https://github.com/user-attachments/assets/c9502650-112a-45cb-bea3-81c4fdadfdce" />

또한, 수술의 위험도를 엿볼 수 있는 **POSSUM SCORE 계산기 알고리즘**을 만들어 진단에 도움이 될 수 있도록 하였습니다.
<img width="1000" alt="image" src="https://github.com/user-attachments/assets/c7cb09f7-2c9f-4b47-af2f-8bbffae85780" />


---

### 3. 수술 정보 입력 페이지
그 정보들을 바탕으로 SurgiForm은 총 **두 번의 LLM**을 거쳐 수술 정보를 빠르고 정확하게 생성합니다.  
1. UpToDate 기반 Textbook에서 수술과 관련된 최신의 전문적인 정보들을 조회하는 LLM  
2. 조회된 정보를 좀 더 쉬운 말로 풀어 설명해 주는 LLM  

그 두 LLM을 거친 정보가 수술 정보 입력 페이지에 출처와 함께 제공됩니다.  
<img width="1000" alt="image" src="https://github.com/user-attachments/assets/1da58fab-a34b-41c0-be1a-af9cd93c9828" />

의사 선생님들께서는 출처와 함께 생성된 정보를 보고 수정할 수 있으며, 추가적인 정보가 필요할 경우 **챗봇**의 도움을 받을 수도 있습니다.
<img width="1000" alt="image" src="https://github.com/user-attachments/assets/72d52414-8673-4d9c-9c81-6aade9ca6725" />


---

### 4. 수술동의서 설명 및 서명 페이지
수술에 대한 모든 정보가 확정되면, 설명 및 서명 페이지로 이동하게 됩니다.  
<img width="1000" alt="image" src="https://github.com/user-attachments/assets/76d69963-1699-45de-820e-d54a8ba29b9d" />

여러 수술 설명은 그림을 그리며 진행되는 경우가 많다고 하여, 항목별로 필요할 경우 **캔버스**를 추가할 수 있도록 발전시켰습니다.  
추후 **녹음 기능**을 추가할 예정입니다.
<img width="1000" alt="image" src="https://github.com/user-attachments/assets/8e6644d9-7bcb-4896-8e9e-f22decfd13ec" />


---

### 5. 수술동의서 PDF 출력 페이지
끝으로 환자와 의사가 서명을 마무리하면 확정된 수술동의서를 **PDF 형식**으로 출력하여 저장할 수 있습니다.
<img width="1000" alt="image" src="https://github.com/user-attachments/assets/5af5023d-00f1-4937-8c25-3c9c839c0a08" />

---

> 앞으로도 지속적인 업데이트와 후속 개발을 통해 완성도를 높여 나가겠습니다!
