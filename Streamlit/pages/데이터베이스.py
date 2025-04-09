import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

st.title('연령별 사고유형 시간대')

# 연도 선택
year = st.selectbox(
    "조회 연도를 선택해 주세요",
    list(range(2005, 2024)),
    index=2023 - 2005
)

st.subheader(f"{year}년 시간대별 사고 건수 (임의 데이터)")

# 시간대 리스트
time_slots = ['00~02시', '02~04시', '04~06시', '06~8시', '8~10시', '10~12시',
              '12~14시', '14~16시', '16~18시', '18~20시', '20~22시', '22~24시']

# 연령대
age_groups = ['10대 이하', '20대', '30대', '40대', '50대', '60대 이상']
data_time = np.random.randint(0, 100, size=(len(age_groups), len(time_slots)))

# 사고유형 항목
cm_slots = ['횡단중', '차도통행중', '길가장자리구역통행중', '보도통행중', '기타']
cc_slots = ['충돌', '추돌', '기타']
c_slots = ['충돌', '도로이탈', '전복사고', '기타']
railroad = ['기타']

accident_group_slots = {
    '차대사람': cm_slots,
    '차대차': cc_slots,
    '차량단독': c_slots,
    '철길건널목': railroad
}

# 전체 사고유형 리스트
accident_types = []
accident_group_map = {}
for group, slots in accident_group_slots.items():
    for slot in slots:
        key = f"{group}-{slot}"
        accident_types.append(key)
        accident_group_map[key] = group

# 사고유형별 데이터 생성
data_accident = np.random.randint(0, 100, size=(len(accident_types), len(time_slots)))

# DataFrame 생성
dft = pd.DataFrame(data_time, index=age_groups, columns=time_slots)
dfa = pd.DataFrame(data_accident, index=accident_types, columns=time_slots)

# 탭 생성
tab1, tab2 = st.tabs(['연령대별', '사고유형별'])

# ---------------------- 연령대별 탭 ----------------------
with tab1:
    st.subheader("📋 연령대별 사고 건수")
    
    st.markdown("### ✅ 연령대 선택")
    selected_ages = []
    for age in age_groups:
        if st.checkbox(age, value=True, key=f"age_{age}"):
            selected_ages.append(age)

    # 필터 적용
    if selected_ages:
        filtered_dft = dft.loc[selected_ages]
        st.dataframe(filtered_dft)

        # Melt 후 시각화
        dft_melt = filtered_dft.reset_index().melt(id_vars='index', var_name='시간대', value_name='사고건수')
        dft_melt.rename(columns={'index': '연령대'}, inplace=True)

        chart1 = alt.Chart(dft_melt).mark_bar().encode(
            x='시간대:O',
            y='사고건수:Q',
            color='연령대:N',
            tooltip=['연령대', '시간대', '사고건수']
        ).properties(width=700, height=400).interactive()

        st.altair_chart(chart1)
    else:
        st.warning("하나 이상의 연령대를 선택해 주세요.")

# ---------------------- 사고유형별 탭 ----------------------
with tab2:
    st.subheader("📋 사고유형별 사고 건수")

    # 사고 그룹 선택
    group_filter = st.selectbox("사고유형 그룹 선택", options=list(accident_group_slots.keys()), key="group_filter")
    selected_types = []

    st.markdown(f"### ✅ '{group_filter}' 내 개별 사고유형 선택")
    for slot in accident_group_slots[group_filter]:
        full_label = f"{group_filter}-{slot}"
        if st.checkbox(slot, value=True, key=f"type_{full_label}"):
            selected_types.append(full_label)

    # 필터 적용
    if selected_types:
        filtered_dfa = dfa.loc[selected_types]
        st.dataframe(filtered_dfa)

        # Melt 후 시각화
        dfa_melt = filtered_dfa.reset_index().melt(id_vars='index', var_name='시간대', value_name='사고건수')
        dfa_melt.rename(columns={'index': '사고유형'}, inplace=True)

        chart2 = alt.Chart(dfa_melt).mark_bar().encode(
            x='시간대:O',
            y='사고건수:Q',
            color='사고유형:N',
            tooltip=['사고유형', '시간대', '사고건수']
        ).properties(width=700, height=400).interactive()

        st.altair_chart(chart2)
    else:
        st.warning("하나 이상의 사고유형을 선택해 주세요.")
