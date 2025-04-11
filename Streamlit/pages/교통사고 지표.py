import streamlit as st
import pandas as pd
import pymysql
import altair as alt

# DB 연결 함수
def get_connection():
    return pymysql.connect(
        host="localhost",    # DBMS 의 ip(host) : str
        port=3306,           # DBMS의 port 번호: int
        user='root',        # username: str
        password="1111",    # password: str
        db="projet_1st"
    )

# 공통 설정
time_slots = ['00~02시', '02~04시', '04~06시', '06~08시', '08~10시', '10~12시',
              '12~14시', '14~16시', '16~18시', '18~20시', '20~22시', '22~24시']

age_groups = ['20세 이하', '21~30세', '31~40세', '41~50세', '51~60세', '61~64세', '65세 이상', '연령불명']

# 탭 설정
tab1, tab2 = st.tabs(['연령대별', '시간대별'])

# ---------------- 연령대별 탭 ----------------
with tab1:
    st.subheader("📋 연령대별 사고유형별 교통사고 지표")

    # 연도 선택
    age_col1, age_col2 = st.columns([1, 5])
    with age_col1:
        year_age = st.selectbox("연도 선택", list(range(2014, 2024)), index=9, key="year_age")

    # 연령대 체크박스
    selected_ages = []
    with age_col2:
        st.text("연령 선택")
        age_cols = st.columns(len(age_groups))
        for i, age in enumerate(age_groups):
            if age_cols[i].checkbox(age, value=True, key=f"age_{age}"):
                selected_ages.append(age)

    if selected_ages:
        try:
            conn = get_connection()
            placeholders = ', '.join(['%s'] * len(selected_ages))
            query = f"""
                SELECT age_group_range AS 연령대, accident_type_name AS 사고유형,
                       count AS 사고건수
                FROM accidentstatsage
                WHERE year_type_id = %s
                  AND age_group_range IN ({placeholders})
                ORDER BY age_group_range, accident_type_name
            """
            with conn.cursor() as cursor:
                cursor.execute(query, (year_age, *selected_ages))
                rows = cursor.fetchall()

            df = pd.DataFrame(rows, columns=['연령대', '사고유형', '사고건수'])

            if df.empty:
                st.warning("선택한 조건에 해당하는 데이터가 없습니다.")
            else:
                # 그래프 출력
                chart = alt.Chart(df).mark_bar().encode(
                    x=alt.X('사고유형:N'),
                    y='사고건수:Q',
                    color='연령대:N',
                    tooltip=['연령대', '사고유형', '사고건수']
                ).properties(width=1000, height=500).interactive()

                st.altair_chart(chart, use_container_width=True)

                # 표 출력
                st.dataframe(df, use_container_width=True, height=600)

        except Exception as e:
            st.error(f"DB 조회 중 오류: {e}")
    else:
        st.warning("하나 이상의 연령대를 선택해 주세요.")

# ---------------- 사고유형별 탭 ----------------
# ---------------- 시간대별 탭 ----------------
with tab2:
    st.subheader("⏰ 시간대별 사고유형별 교통사고 지표")

    # UI 정렬
    time_col1, time_col2, time_col3 = st.columns([1, 2, 2])

    with time_col1:
        year_time = st.selectbox("연도 선택", list(range(2014, 2024)), index=9, key="year_time")

    with time_col2:
        measure = st.selectbox("측정항목 선택", ["사고[건]", "부상[명]", "사망[명]"], key="measure")

    with time_col3:
        st.text("사고유형 선택")
        selected_types = []
        type_options = ['차대사람', '차대차', '차량단독']  # 필요시 동적 로딩 가능
        type_cols = st.columns(len(type_options))
        for i, type_name in enumerate(type_options):
            if type_cols[i].checkbox(type_name, value=True, key=f"type_{type_name}"):
                selected_types.append(type_name)

    if selected_types:
        try:
            conn = get_connection()
            placeholders = ', '.join(['%s'] * len(selected_types))

            query = f"""
                SELECT accident_cause_type_name AS 사고유형대분류,
                       accident_cause_type_list AS 사고유형중분류,
                       time_slot_id AS 시간대,
                       count AS 값
                FROM accidentstatstime
                WHERE year_type_id = %s
                  AND measure = %s
                  AND accident_cause_type_name IN ({placeholders})
                ORDER BY 사고유형대분류, 사고유형중분류, 시간대
            """
            with conn.cursor() as cursor:
                cursor.execute(query, (year_time, measure, *selected_types))
                rows = cursor.fetchall()

            df_time = pd.DataFrame(rows, columns=['사고유형대분류', '사고유형중분류', '시간대', '값'])

            if df_time.empty:
                st.warning("선택한 조건에 해당하는 데이터가 없습니다.")
            else:
                # 시각화
                chart = alt.Chart(df_time).mark_bar().encode(
                    x=alt.X('시간대:N', sort=time_slots),
                    y='값:Q',
                    color='사고유형중분류:N',
                    column='사고유형대분류:N',
                    tooltip=['사고유형대분류', '사고유형중분류', '시간대', '값']
                ).properties(width=250, height=500).configure_view(stroke=None)

                st.altair_chart(chart, use_container_width=True)

                # 표 출력
                st.dataframe(df_time, use_container_width=True, height=600)

        except Exception as e:
            st.error(f"DB 조회 중 오류: {e}")
    else:
        st.warning("하나 이상의 사고유형 대분류를 선택해 주세요.")
