import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from PIL import Image

st.set_page_config(layout="wide")
st.title('연령별 사고유형 시간대')

# 연도 리스트 및 선택
years = list(range(2014, 2024))
year = st.selectbox("조회 연도를 선택해 주세요", years, index=len(years) - 1)
st.subheader(f"{year}년 시간대별 사고 통계")

# 시간대, 연령대, 사고유형 정의
time_slots = ['00~02시', '02~04시', '04~06시', '06~8시', '8~10시', '10~12시',
              '12~14시', '14~16시', '16~18시', '18~20시', '20~22시', '22~24시']
age_groups = ['20대 이하', '20대', '30대', '40대', '50대', '60대 이상']
metrics = ['사고건수', '부상자수', '사망자수']

# 사고유형 그룹 및 상세 항목
accident_group_slots = {
    '차대사람': ['횡단중', '차도통행중', '길가장자리구역통행중', '보도통행중', '기타'],
    '차대차': ['충돌', '추돌', '기타'],
    '차량단독': ['충돌', '도로이탈', '전복사고', '기타'],
    '철길건널목': ['기타']
}

# 사고유형 전체 리스트 구성
accident_types = []
accident_group_map = {}
for group, slots in accident_group_slots.items():
    for slot in slots:
        key = f"{group}-{slot}"
        accident_types.append(key)
        accident_group_map[key] = group

# 고정 데이터를 연도별로 미리 생성
np.random.seed(42)  # 항상 같은 값 나오도록 고정
yearly_data_time = {}
yearly_data_accident = {}

for y in years:
    yearly_data_time[y] = {
        metric: pd.DataFrame(
            np.random.randint(
                50 if metric == "사고건수" else 20 if metric == "부상자수" else 0,
                100 if metric == "사고건수" else 80 if metric == "부상자수" else 10,
                size=(len(age_groups), len(time_slots))
            ),
            index=age_groups,
            columns=time_slots
        ) for metric in metrics
    }

    yearly_data_accident[y] = {
        metric: pd.DataFrame(
            np.random.randint(
                50 if metric == "사고건수" else 20 if metric == "부상자수" else 0,
                100 if metric == "사고건수" else 80 if metric == "부상자수" else 10,
                size=(len(accident_types), len(time_slots))
            ),
            index=accident_types,
            columns=time_slots
        ) for metric in metrics
    }

# 탭 구성
tab1, tab2 = st.tabs(['연령대별', '사고유형별'])

# ---------------------- 연령대별 탭 ----------------------
with tab1:
    st.subheader("📋 연령대별 사고 지표")
    st.markdown("### ✅ 연령대 선택")
    selected_ages = [age for age in age_groups if st.checkbox(age, True, key=f"age_{age}")]
    selected_metric = st.selectbox("표시할 지표 선택", metrics, index=0, key="metric_age")

    if selected_ages:
        dft = yearly_data_time[year][selected_metric]
        filtered_dft = dft.loc[selected_ages]
        st.dataframe(filtered_dft, use_container_width=True, height=500)

        dft_melt = filtered_dft.reset_index().melt(id_vars='index', var_name='시간대', value_name=selected_metric)
        dft_melt.rename(columns={'index': '연령대'}, inplace=True)

        chart1 = alt.Chart(dft_melt).mark_bar().encode(
            x='시간대:O',
            y=f'{selected_metric}:Q',
            color='연령대:N',
            tooltip=['연령대', '시간대', selected_metric]
        ).properties(width=1000, height=500).interactive()

        st.altair_chart(chart1, use_container_width=True)
    else:
        st.warning("하나 이상의 연령대를 선택해 주세요.")

# ---------------------- 사고유형별 탭 ----------------------
with tab2:
    st.subheader("📋 사고유형별 사고 지표")
    group_filter = st.selectbox("사고유형 그룹 선택", options=list(accident_group_slots.keys()), key="group_filter")
    selected_types = []

    st.markdown(f"### ✅ '{group_filter}' 내 개별 사고유형 선택")
    for slot in accident_group_slots[group_filter]:
        full_label = f"{group_filter}-{slot}"
        if st.checkbox(slot, True, key=f"type_{full_label}"):
            selected_types.append(full_label)

    selected_metric = st.selectbox("표시할 지표 선택", metrics, index=0, key="metric_accident")

    if selected_types:
        dfa = yearly_data_accident[year][selected_metric]
        filtered_dfa = dfa.loc[selected_types]
        st.dataframe(filtered_dfa, use_container_width=True, height=500)

        dfa_melt = filtered_dfa.reset_index().melt(id_vars='index', var_name='시간대', value_name=selected_metric)
        dfa_melt.rename(columns={'index': '사고유형'}, inplace=True)

        chart2 = alt.Chart(dfa_melt).mark_bar().encode(
            x='시간대:O',
            y=f'{selected_metric}:Q',
            color='사고유형:N',
            tooltip=['사고유형', '시간대', selected_metric]
        ).properties(width=1000, height=500).interactive()

        st.altair_chart(chart2, use_container_width=True)
    else:
        st.warning("하나 이상의 사고유형을 선택해 주세요.")

# 출처 및 이미지
st.write(":green[데이터 출처:]")
st.markdown("[TAAS 교통사고 분석 시스템 바로가기](https://taas.koroad.or.kr/sta/acs/exs/typical.do?menuId=WEB_KMP_OVT_UAS_ASA)")

try:
    img = Image.open(r'C:\Users\mycom\Desktop\project\Image\TAAS.jpg')
    st.image(img, caption='TAAS 교통사고 분석 시스템')
except FileNotFoundError:
    st.warning("이미지 파일을 찾을 수 없습니다. 경로를 확인해 주세요.")
