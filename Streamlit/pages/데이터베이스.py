import streamlit as st
import pandas as pd
import pymysql
import altair as alt
from PIL import Image

# DB 연결 함수
def get_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='1111',
        database='TrafficAccidentStats',
        cursorclass=pymysql.cursors.DictCursor
    )

# 시간대, 연령대, 사고유형 정의
time_slots = ['00~02시', '02~04시', '04~06시', '06~8시', '8~10시', '10~12시',
              '12~14시', '14~16시', '16~18시', '18~20시', '20~22시', '22~24시']
age_groups = ['20세 이하', '21`~`30세', '31`~`40세', '41`~`50세', '51`~`60세', '61`~`64세 이상','65세 이상', '연령불명']
metrics = {'사고건수': 'accident_count', '부상자수': 'injury_count', '사망자수': 'death_count'}

accident_group_slots = {
    '차대사람': ['횡단중', '차도통행중', '길가장자리구역통행중', '보도통행중', '기타'],
    '차대차': ['충돌', '추돌', '기타'],
    '차량단독': ['충돌', '도로이탈', '전복사고', '기타'],
    '철길건널목': ['기타']
}

accident_types = []
accident_group_map = {}
for group, slots in accident_group_slots.items():
    for slot in slots:
        key = f"{group}-{slot}"
        accident_types.append(key)
        accident_group_map[key] = group

# 연도 선택
years = list(range(2014, 2024))
year = st.selectbox("조회 연도를 선택해 주세요", years, index=len(years) - 1)

# 탭 구성
tab1, tab2 = st.tabs(['연령대별', '사고유형별'])

# ---------------- 연령대별 탭 ----------------
with tab1:
    st.subheader("📋 연령대별 사고 지표")

    # ✅ 연령대 체크박스를 2줄(3열)로 배치
    cols = st.columns(3)
    selected_ages = []
    for i, age in enumerate(age_groups):
        if cols[i % 3].checkbox(age, True, key=f"age_{age}"):
            selected_ages.append(age)

    selected_metric = st.selectbox("표시할 지표 선택", list(metrics.keys()), index=0, key="metric_age")

    if selected_ages:
        try:
            conn = get_connection()
            placeholders = ', '.join(['%s'] * len(selected_ages))
            query = f"""
                SELECT ag.age_range, ts.time_range, ast.{metrics[selected_metric]}
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
                pivot_df = df.pivot(index='age_range', columns='time_range', values=metrics[selected_metric])
                st.dataframe(pivot_df, use_container_width=True, height=500)

                melt_df = df.rename(columns={
                    'age_range': '연령대',
                    'time_range': '시간대',
                    metrics[selected_metric]: selected_metric
                })

                chart = alt.Chart(melt_df).mark_bar().encode(
                    x='시간대:O',
                    y=f'{selected_metric}:Q',
                    color='연령대:N',
                    tooltip=['연령대', '시간대', selected_metric]
                ).properties(width=1000, height=500).interactive()

                st.altair_chart(chart, use_container_width=True)

        except Exception as e:
            st.error(f"DB 조회 중 오류: {e}")

    else:
        st.warning("하나 이상의 연령대를 선택해 주세요.")

# ---------------- 사고유형별 탭 ----------------
with tab2:
    st.subheader("📋 사고유형별 사고 지표")

    group_filter = st.selectbox("사고유형 그룹 선택", options=list(accident_group_slots.keys()), key="group_filter")
    selected_types = []

    st.markdown(f"### ✅ '{group_filter}' 내 개별 사고유형 선택")

    # ✅ 사고유형 체크박스를 4열로 정렬
    cols = st.columns(4)
    for i, slot in enumerate(accident_group_slots[group_filter]):
        full_label = f"{group_filter}-{slot}"
        if cols[i % 4].checkbox(slot, True, key=f"type_{full_label}"):
            selected_types.append(full_label)

    selected_metric = st.selectbox("표시할 지표 선택", list(metrics.keys()), index=0, key="metric_accident")

    if selected_types:
        try:
            conn = get_connection()
            placeholders = ', '.join(['%s'] * len(selected_types))
            query = f"""
                SELECT ac.type_list AS 사고유형, ts.time_range AS 시간대, ast.{metrics[selected_metric]}
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
                pivot_df = df.pivot(index='사고유형', columns='시간대', values=metrics[selected_metric])
                st.dataframe(pivot_df, use_container_width=True, height=500)

                chart = alt.Chart(df).mark_bar().encode(
                    x='시간대:O',
                    y=f'{metrics[selected_metric]}:Q',
                    color='사고유형:N',
                    tooltip=['사고유형', '시간대', metrics[selected_metric]]
                ).properties(width=1000, height=500).interactive()

                st.altair_chart(chart, use_container_width=True)

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
