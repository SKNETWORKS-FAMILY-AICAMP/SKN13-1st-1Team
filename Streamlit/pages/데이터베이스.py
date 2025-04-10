import streamlit as st
import pandas as pd
import pymysql
import altair as alt
from PIL import Image

st.set_page_config(layout="wide")
st.title("연령대·사고유형별 시간대별 교통사고 데이터")

# 연도 선택을 체크박스와 같은 줄에 배치
header_col1, header_col2 = st.columns([8, 1])
with header_col2:
    years = list(range(2014, 2024))
    year = st.selectbox("연도 선택", years, index=len(years) - 1)

# 탭
tab1, tab2 = st.tabs(['연령대별', '사고유형별'])

# DB 연결 함수
def get_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='1111',
        database='TrafficAccidentStats',
        cursorclass=pymysql.cursors.DictCursor
    )

# 공통 설정
time_slots = ['00~02시', '02~04시', '04~06시', '06~08시', '08~10시', '10~12시',
              '12~14시', '14~16시', '16~18시', '18~20시', '20~22시', '22~24시']

age_groups = ['20세 이하', '21~30세', '31~40세', '41~50세', '51~60세', '61~64세 이상', '65세 이상', '연령불명']

accident_group_slots = {
    '차대사람': ['횡단중', '차도통행중', '길가장자리구역통행중', '보도통행중', '기타'],
    '차대차': ['충돌', '추돌', '기타'],
    '차량단독': ['충돌', '도로이탈', '전복사고', '기타'],
    '철길건널목': ['기타']
}

time_slot_fix = {
    '06~8시': '06~08시',
    '8~10시': '08~10시',
    '10~12시': '10~12시'
}

# ---------------- 연령대별 탭 ----------------
with tab1:
    st.subheader("📋 연령대별 사고 지표")

    selected_ages = []
    age_cols = st.columns(8)
    for i, age in enumerate(age_groups):
        if age_cols[i].checkbox(age, value=True, key=f"age_{age}"):
            selected_ages.append(age)

    if selected_ages:
        try:
            conn = get_connection()
            placeholders = ', '.join(['%s'] * len(selected_ages))
            query = f"""
                SELECT ag.age_range, ts.time_range,
                       ast.accident_count, ast.injury_count, ast.death_count
                FROM AccidentStatsAge ast
                JOIN AgeGroup ag ON ast.age_group_id = ag.id
                JOIN TimeSlot ts ON ast.time_slot_id = ts.id
                WHERE ast.year_type_id = %s
                  AND ag.age_range IN ({placeholders})
                ORDER BY ag.age_range, ts.time_range
            """
            with conn.cursor() as cursor:
                cursor.execute(query, (year, *selected_ages))
                rows = cursor.fetchall()
            df = pd.DataFrame(rows)

            if df.empty:
                st.warning("선택한 조건에 해당하는 데이터가 없습니다.")
            else:
                df['time_range'] = df['time_range'].replace(time_slot_fix)
                df = df.rename(columns={
                    'age_range': '연령대',
                    'time_range': '시간대',
                    'accident_count': '사고건수',
                    'injury_count': '부상자수',
                    'death_count': '사망자수'
                })

                chart = alt.Chart(df).mark_bar().encode(
                    x=alt.X('시간대:O', sort=time_slots),
                    y='사고건수:Q',
                    color='연령대:N',
                    tooltip=['연령대', '시간대', '사고건수']
                ).properties(width=1000, height=500).interactive()

                st.altair_chart(chart, use_container_width=True)

                melt = pd.melt(df,
                               id_vars=['연령대', '시간대'],
                               value_vars=['사고건수', '부상자수', '사망자수'],
                               var_name='지표',
                               value_name='값')

                pivot_df = melt.pivot_table(
                    index=['연령대', '지표'],
                    columns='시간대',
                    values='값'
                )
                st.dataframe(pivot_df, use_container_width=True, height=600)

        except Exception as e:
            st.error(f"DB 조회 중 오류: {e}")
    else:
        st.warning("하나 이상의 연령대를 선택해 주세요.")

# ---------------- 사고유형별 탭 ----------------
with tab2:
    st.subheader("📋 사고유형별 사고 지표")

    group_filter = st.selectbox("사고유형 그룹 선택", options=list(accident_group_slots.keys()), key="group_filter")
    subtypes = accident_group_slots[group_filter]

    selected_types = []
    type_cols = st.columns(5)
    for i, slot in enumerate(subtypes):
        full_label = f"{group_filter}-{slot}"
        if type_cols[i % 5].checkbox(slot, value=True, key=f"type_{full_label}"):
            selected_types.append(full_label)

    if selected_types:
        try:
            conn = get_connection()
            placeholders = ', '.join(['%s'] * len(selected_types))
            query = f"""
                SELECT ac.type_list AS 사고유형, ts.time_range AS 시간대,
                       ast.accident_count, ast.injury_count, ast.death_count
                FROM AccidentStatsTime ast
                JOIN AccidentCause ac ON ast.accident_type_id = ac.id
                JOIN TimeSlot ts ON ast.time_slot_id = ts.id
                WHERE ast.year_type_id = %s
                  AND ac.type_list IN ({placeholders})
                ORDER BY ac.type_list, ts.time_range
            """
            with conn.cursor() as cursor:
                cursor.execute(query, (year, *selected_types))
                rows = cursor.fetchall()
            df = pd.DataFrame(rows)

            if df.empty:
                st.warning("선택한 조건에 해당하는 데이터가 없습니다.")
            else:
                df['시간대'] = df['시간대'].replace(time_slot_fix)
                df = df.rename(columns={
                    'accident_count': '사고건수',
                    'injury_count': '부상자수',
                    'death_count': '사망자수'
                })

                chart = alt.Chart(df).mark_bar().encode(
                    x=alt.X('시간대:O', sort=time_slots),
                    y='사고건수:Q',
                    color='사고유형:N',
                    tooltip=['사고유형', '시간대', '사고건수']
                ).properties(width=1000, height=500).interactive()

                st.altair_chart(chart, use_container_width=True)

                melt = pd.melt(df,
                               id_vars=['사고유형', '시간대'],
                               value_vars=['사고건수', '부상자수', '사망자수'],
                               var_name='지표',
                               value_name='값')

                pivot_df = melt.pivot_table(
                    index=['사고유형', '지표'],
                    columns='시간대',
                    values='값'
                )
                st.dataframe(pivot_df, use_container_width=True, height=600)

        except Exception as e:
            st.error(f"DB 조회 중 오류: {e}")
    else:
        st.warning("하나 이상의 사고유형을 선택해 주세요.")

# 출처 및 이미지
st.write(":green[데이터 출처:]")
st.markdown("[TAAS 교통사고 분석 시스템 바로가기](https://taas.koroad.or.kr/sta/acs/exs/typical.do?menuId=WEB_KMP_OVT_UAS_ASA)")

try:
    img = Image.open(r'C:\Users\mycom\Desktop\project_1st\SKN13-1st-1Team\Streamlit\Image\TAAS.jpg')
    st.image(img, caption='TAAS 교통사고 분석 시스템')
except FileNotFoundError:
    st.warning("이미지 파일을 찾을 수 없습니다. 경로를 확인해 주세요.")
