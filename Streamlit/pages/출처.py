import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image

# 백슬래시를 raw string으로 처리하거나 슬래시 방향 바꾸기
img = Image.open(r'C:\Users\mycom\Desktop\project\Image\TAAS.jpg')
st.image(img, caption='TAAS 교통사고 분석 시스템')

# 링크를 제대로 표시하려면 st.markdown을 사용하고, 클릭 가능한 하이퍼링크로 만들어야 함
st.subheader("관련 링크:")
st.markdown("[TAAS 교통사고 분석 시스템 바로가기](https://taas.koroad.or.kr/sta/acs/exs/typical.do?menuId=WEB_KMP_OVT_UAS_ASA)")
