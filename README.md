# 📊 박수연의 한국 복지패널 대시보드 (Sooyeon's Korean Welfare Panel Dashboard)

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://sooyeon-s-korean-welfare-panel-dashboard.streamlit.app/)

한국 복지패널 데이터를 활용한 인터랙티브 데이터 시각화 대시보드입니다. 성별, 연령, 직업, 종교, 지역 등 다양한 요인에 따른 삶의 실태(월급, 직업 빈도, 이혼율 등)를 Streamlit을 통해 직관적인 차트와 표로 분석하여 제공합니다.

---

## 1. 프로젝트의 주요 기능과 목적 💡

### 주요 목적
복지패널 데이터를 정제 및 전처리하여, 사용자가 원하는 조건(필터)에 맞춰 대한민국 국민의 경제적, 사회적 삶의 단면을 손쉽게 탐색할 수 있도록 돕는 웹 대시보드를 제공합니다.

### 주요 분석 기능
1. **성별에 따른 월급 차이**: 성별에 따라 평균 월급이 어떻게 다른지 분석합니다.
2. **나이와 월급의 관계**: 몇 살 때 월급을 가장 많이 받는지 선 그래프로 확인합니다.
3. **연령대에 따른 월급 차이**: 청년(young), 중년(middle), 노년(old) 등 연령대별 평균 월급을 비교합니다.
4. **연령대 및 성별 월급 차이**: 연령대별로 성별 월급 차이가 존재하는지 확인합니다.
5. **직업별 월급 차이**: 평균 월급 상위 10개 직업을 파악합니다.
6. **성별 직업 빈도**: 남성과 여성 각각 어떤 직업 종사자가 많은지 상위 10개 직업을 제공합니다.
7. **종교 유무에 따른 이혼율**: 종교의 유무 및 연령대가 이혼율에 미치는 영향을 분석합니다.
8. **지역별 연령대 비율**: 7개 권역별로 어느 지역에 노년층이 많은지 누적 막대 그래프로 살펴봅니다.

---

## 2. 저장소 파일 구조 및 설명 📂

이 프로젝트에 포함된 주요 파일과 각각의 역할은 다음과 같습니다. 저장소를 클론(Clone)하면 아래 파일들이 모두 로컬 환경으로 복사됩니다.

- **`app.py`**: Streamlit 대시보드를 실행하는 메인 파이썬 웹 애플리케이션 스크립트입니다.
- **`welfare_2015.csv`**: 본 대시보드에서 분석에 사용하는 한국 복지패널 원본 데이터셋입니다.
- **`welfare_2015_codebook.xlsx`**: 직업 코드(숫자)를 실제 직업명(문자열)으로 변환할 때 사용하는 코드북입니다.
- **`requirements.txt`**: 프로젝트 실행에 필요한 파이썬 라이브러리 목록이 적힌 파일입니다. (로컬 환경 세팅용)
- **`packages.txt`**: Streamlit Community Cloud 배포 시, 리눅스 서버에 나눔고딕 등 추가 시스템 패키지(예: 한글 폰트)를 설치하기 위해 사용되는 파일입니다.
- **`logo.png`**: 앱 상단과 사이드바에 표시되는 로고 이미지 파일입니다.

---

## 3. 설치 방법 ⚙️

로컬PC에서 대시보드를 직접 실행하고 싶은 경우 다음 단계를 따라주세요.

### 요구 사항 (Prerequisites)
- Python 3.10 이상
- Git

### 설치 및 실행 과정
1. **저장소 클론(Clone)**
   ```bash
   git clone https://github.com/MDA04systack/Sooyeon-s-Korean-Welfare-Panel-Dashboard.git
   cd Sooyeon-s-Korean-Welfare-Panel-Dashboard
   ```

2. **필수 패키지 설치**
   ```bash
   pip install -r requirements.txt
   ```
   *(이 프로젝트는 `streamlit`, `pandas`, `numpy`, `matplotlib`, `seaborn`, `openpyxl` 등을 사용합니다.)*

3. **애플리케이션 실행**
   ```bash
   streamlit run app.py
   ```
   실행 후 브라우저에서 `http://localhost:8501`로 접속하면 대시보드를 확인할 수 있습니다.

---

## 4. 문제 해결 방법 (Troubleshooting) 🛠️

- **폰트가 깨져서 네모(□)로 나오는 경우**  
  본 프로젝트는 실행 환경(Windows, Linux 등)을 인식하여 자동으로 맑은 고딕(Windows)과 나눔고딕(Linux)을 적용합니다. 만약 폰트가 깨진다면 로컬 PC에 해당 폰트가 설치되어 있는지 확인하세요.
- **데이터 로드 실패 오류 ("파일을 찾을 수 없습니다")**  
  사이드바의 '데이터 파일 경로'가 프로젝트 내의 `welfare_2015.csv`를 제대로 가리키고 있는지 확인하세요. 또한 `welfare_2015_codebook.xlsx` 파일이 루트 폴더에 있어야 직업명 변환이 정상적으로 수행됩니다.
- **`ModuleNotFoundError` 발생**  
  `pip install -r requirements.txt`를 통해 필요한 파이썬 라이브러리(패키지)가 모두 설치되었는지 다시 확인해주세요.

---

## 5. 지원 창구 📞

버그 발견, 기능 추가 요청 혹은 기타 문의 사항이 있으시다면 아래 방법으로 연락해주세요.
- **GitHub Issues**: [이곳에 이슈를 남겨주세요](https://github.com/MDA04systack/Sooyeon-s-Korean-Welfare-Panel-Dashboard/issues).

---

## 6. 라이선스 정보 📄

이 프로젝트는 [MIT License](LICENSE)를 따릅니다. 누구나 자유롭게 이용, 수정, 배포하실 수 있습니다. (공공 데이터인 복지패널 데이터의 활용 규정은 해당 데이터 출처의 방침을 따릅니다.)

---

## 7. 변경 로그 (Changelog) 📝

- **v1.0.0** (최초 배포)
  - Streamlit 기반 인터랙티브 대시보드 구축
  - 성별, 연령, 직업, 종교, 혼인 및 지역별 8가지 파생 변수 분석 차트 제공
  - Windows / Linux 환경 한글 폰트 자동 대응 로직 추가
  - Streamlit Community Cloud 배포 및 안정화
