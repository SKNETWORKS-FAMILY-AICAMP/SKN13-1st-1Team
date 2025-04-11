import streamlit as st
import pandas as pd
import pymysql
import altair as alt

# DB 연결 함수
def get_connection():
    return pymysql.connect(
        host="192.168.0.12",    # DBMS 의 ip(host) : str
        port=3306,           # DBMS의 port 번호: int
        user='test',        # username: str
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
with tab2:
    st.subheader("📋 시간대별 사고유형별 교통사고 지표")

    # 연도 선택
    year_type = st.selectbox("연도 선택", list(range(2014, 2024)), index=9, key="year_type_select")

    # 사고유형 대분류 선택
    accident_group = st.selectbox("사고유형 대분류 선택", ['차대사람', '차대차', '차량단독', '철길건널목'], key="accident_group_select")

    # 사고유형 중분류 선택
    selected_subtypes = []
    st.text("사고유형 중분류 선택")
    subtypes = ['횡단중', '차도통행중', '보도통행중', '기타'] if accident_group == '차대사람' else ['충돌', '추돌', '기타']
    cols = st.columns(len(subtypes))
    for i, stype in enumerate(subtypes):
        if cols[i].checkbox(stype, value=True):
            selected_subtypes.append(stype)

    if selected_subtypes:
        try:
            conn = get_connection()

            # 쿼리 조건이 잘 적용되는지 확인
            placeholders = ', '.join(['%s'] * len(selected_subtypes))
            query = f"""
                SELECT accident_cause_type_name, accident_cause_type_list, time_slot_id, count
                FROM accidentstatstime
                WHERE accident_cause_type_name = %s
                  AND accident_cause_type_list IN ({placeholders})
                  AND year_type_id = %s
            """
            with conn.cursor() as cursor:
                cursor.execute(query, (accident_group, *selected_subtypes, year_type))
                rows = cursor.fetchall()

            # 데이터가 없을 경우 확인
            if not rows:
                st.warning(f"선택한 연도({year_type})와 사고유형에 대한 데이터가 없습니다.")
            else:
                df = pd.DataFrame(rows)

                # 데이터 처리
                # df['사고건수'] = pd.to_numeric(df['값'], errors='coerce')
                df['count'] = pd.to_numeric(df['값'], errors='coerce')

                # 그래프 출력
                chart = alt.Chart(df).mark_bar().encode(
                    x=alt.X('time_slot_id:O', title='시간대', sort=time_slots),
                    y=alt.Y('count:Q', title='사고건수'),
                    color='accident_cause_type_list:N',
                    tooltip=['accident_cause_type_list', 'time_slot_id', 'count']
                ).properties(width=1000, height=500).interactive()

                st.altair_chart(chart, use_container_width=True)

                # 피벗 테이블 출력
                melt = pd.melt(df,
                               id_vars=['사고유형중분류', '시간대'],
                               value_vars=['사고건수'],
                               var_name='지표',
                               value_name='사고건수_값')

                pivot_df = melt.pivot_table(
                    index=['사고유형중분류', '지표'],
                    columns='시간대',
                    values='사고건수_값'
                )
                # melt = pd.melt(df,
                #                id_vars=['accident_cause_type_list', 'time_slot_id'],
                #                value_vars=['count'],
                #                var_name='지표',
                #                value_name='사고건수_값')

                # pivot_df = melt.pivot_table(
                #     index=['accident_cause_type_list', '지표'],
                #     columns='시간대',
                #     values='사고건수_값'
                # )
                # pivot_df = pivot_df.astype(int)
                # st.dataframe(pivot_df, use_container_width=True, height=600)

        except Exception as e:
            st.error(f"DB 조회 중 오류: {e}")
    else:
        st.warning("사고유형 중분류를 하나 이상 선택해 주세요.")
