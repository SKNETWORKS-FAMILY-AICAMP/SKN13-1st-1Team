import streamlit as st
from PIL import Image

st.set_page_config(page_title="교통사고 통계 시각화", layout="wide")

st.title("🚦 교통사고 통계 시각화 대시보드")
st.markdown("---")

# 이미지 표시
try:
    img = Image.open(r'C:\Users\mycom\Desktop\project_1st\SKN13-1st-1Team\Streamlit\Image\TAAS.jpg')
    st.image(img, use_container_width=True)
except:
    st.warning("메인 이미지 파일을 불러올 수 없습니다.")

# 앱 소개
st.markdown("""
### 📊 이 앱은 무엇인가요?
이 대시보드는 **연령대별**, **사고유형별**로 교통사고가 시간대에 따라 어떻게 발생하는지를 시각적으로 분석하기 위해 제작되었습니다.  
대한민국 교통사고 데이터를 기반으로 하며, 시계열 트렌드를 직관적으로 파악할 수 있습니다.

---

### 🔍 주요 기능 안내
- **연령대별 분석 탭**: 다양한 연령대의 사고 발생 시간대 및 규모 비교
- **사고유형별 분석 탭**: 사고의 유형에 따른 시간대별 발생 패턴 분석
- **연도 선택 기능**: 2014년부터 2023년까지 연도별 데이터 제공

---

### 📂 데이터 출처
본 데이터는 **[TAAS 교통사고 분석 시스템](https://taas.koroad.or.kr/sta/acs/exs/typical.do?menuId=WEB_KMP_OVT_UAS_ASA)** 에서 제공된 통계를 기반으로 정제하였습니다.

---

### 🧑‍💻 개발/기획
- 프로젝트명: **SKN13-1st-1Team**
- 목적: 교통사고 예방을 위한 데이터 기반 의사결정 지원
""")

st.success("왼쪽 사이드바 또는 상단 탭에서 분석을 시작해보세요!")
sd