import streamlit as st
import pandas as pd
import altair as alt
from sqlalchemy import create_engine

# SQLAlchemy 엔진 설정
engine = create_engine("mysql+pymysql://test:1111@192.168.0.12:3306/projet_1st")

# # 질문별 SQL 쿼리
# q1_query = """
# SELECT accident_type_name, count 
# FROM accidentstatsage 
# WHERE age_group_range = '65세이상'
# """

# q2_query = """
# SELECT time_slot_range, accident_cause_type_list, count 
# FROM accidentstatstime 
# WHERE time_slot_range IN ('08~10시', '18~20시')
# """

# q3_query = """
# SELECT age_group_range, accident_type_name, count 
# FROM accidentstatsage
# """

# q4_query = """
# SELECT accident_type_name, count 
# FROM accidentstatsage 
# WHERE age_group_range = '20세이하'
# """

# q5_query = """
# SELECT accident_cause_type_name, accident_cause_type_list, count 
# FROM accidentstatstime 
# WHERE time_slot_range IN ('00~02시', '02~04시', '04~06시')
# """

# q6_query = """
# SELECT time_slot_range, count 
# FROM accidentstatstime 
# WHERE accident_cause_type_name = '차대사람' AND accident_cause_type_list = '횡단중'
# """

# FAQ 1
q1_query = """
SELECT accident_type_name, age_group_range, count 
FROM accidentstatsage 
WHERE age_group_range = '65세이상'
"""

# FAQ 2
q2_query = """
SELECT time_slot_id, accident_cause_type_list, count
FROM accidentstatstime 
WHERE accident_cause_type_name = '차대차' AND accident_cause_type_list = '추돌'
"""

# FAQ 3
q3_query = """
SELECT age_group_range, accident_type_name, count 
FROM accidentstatsage
"""

# FAQ 4
q4_query = """
SELECT accident_type_name, count 
FROM accidentstatsage 
WHERE age_group_range = '20세이하'
"""

# FAQ 5
q5_query = """
SELECT accident_cause_type_name, accident_cause_type_list, count 
FROM accidentstatstime 
WHERE time_slot_id IN ('00~02시', '02~04시', '04~06시')
"""

# FAQ 6
q6_query = """
SELECT time_slot_id, count 
FROM accidentstatstime 
WHERE accident_cause_type_name = '차대사람' AND accident_cause_type_list = '횡단중'
"""

# Streamlit 타이틀
st.title('자주 묻는 질문')

# 질문 리스트
faq_question_list = [
    "65세 이상 고령층은 어떤 유형의 교통사고에 가장 많이 노출되나요?",
    "출퇴근 시간대에 많이 발생하는 교통사고 유형은 무엇인가요?",
    "연령대에 따라 가장 흔한 교통사고 유형은 어떻게 다르게 나타나나요?",
    "20세 이하 연령층에서 주로 발생하는 사고는 어떤 유형인가요?",
    "새벽 시간대(00~06시)에 자주 발생하는 사고 유형은 무엇인가요?",
    "보행자 사고는 어떤 시간대에 집중되나요?"
]

# 답변 리스트
faq_answer_list = [
    """65세 이상 연령대에서는 차대사람 사고가 가장 많이 발생합니다.
이는 고령 보행자들이 도로 이용 시 주로 보행자로 활동하며, 판단력과 반응 속도의 저하 등으로 인해 사고 위험에 더 쉽게 노출되는 경향이 있음을 보여줍니다.""",

    """18`~`20시 퇴근 시간대에 차대차 사고가 가장 많이 발생하며, 이 시간대는 사고 건수가 12,000건 이상으로 가장 높은 수치를 기록했습니다.
차량 혼잡, 급정거, 차선 변경 등이 집중되는 시간대이므로, 운전자들의 주의가 특히 필요합니다.""",

    """61세 이상 고령층과 20세 이하 연령층에서는 차대사람 사고가 가장 많이 발생한 반면,
21세부터 50세까지의 연령층에서는 차대차 사고가 가장 높은 비율을 차지합니다.
이는 각 연령대별 이동 방식과 생활 패턴이 사고 유형에 영향을 미치는 것을 보여줍니다.""",

    """20세 이하 연령층에서는 차대사람 사고 비중이 가장 높습니다.
보행 중 등하교 활동이 많은 나이대이기 때문에 보행자 사고가 두드러지게 나타납니다.""",

    """새벽 시간대에는 '차대차' 사고가 가장 많이 발생합니다.
도로가 한산한 시간임에도 불구하고 졸음운전, 과속 등으로 인한 사고가 빈번히 발생합니다.""",

    """보행자 사고는 18`~`20시에 가장 많이 발생합니다.
이 시간대는 퇴근 및 통학 시간이 겹치며, 차량과 보행자의 혼잡도가 높아지는 시점입니다."""
]

# Table: accidentstatstime
# id
# year_type_id
# accident_cause_type_name // 사고유형 대분류
# accident_cause_type_list // 사고유형 중분류
# time_slot_id
# count

# Table: accidentstatsage
# id
# year_type_id
# age_group_range
# accident_type_name
# measure
# count

# FAQ 렌더링 함수
def faq_item(question: str, answer: str, index: int, expanded: bool = False):
    with st.expander(f"❓ Q. {question}", expanded=expanded):
        st.markdown(answer)

        if index == 0:
            df = pd.read_sql(q1_query, con=engine)
            chart = alt.Chart(df).mark_bar(size=80).encode(
                x=alt.X('accident_type_name:N', title='사고유형'),
                y=alt.Y('count:Q', title='사고건수'),
                tooltip=['accident_type_name', 'count']
            ).properties(title="65세 이상 교통사고 유형")
            st.altair_chart(chart, use_container_width=True)

        elif index == 1:
            df = pd.read_sql(q2_query, con=engine)
            chart = alt.Chart(df).mark_bar(size=30).encode(
                x=alt.X('time_slot_id:O', title='시간대'),
                y=alt.Y('count:Q', title='사고건수'),
                color=alt.Color('accident_cause_type_list:N', title='사고유형'),
                tooltip=['time_slot_id', 'accident_cause_type_list', 'count']
            ).properties(title="출퇴근 시간대 사고 유형")
            st.altair_chart(chart, use_container_width=True)

        elif index == 2:
            df = pd.read_sql(q3_query, con=engine)
            chart = alt.Chart(df).mark_bar().encode(
                x=alt.X('age_group_range:N', title='연령대'),
                y=alt.Y('count:Q', title='사고건수'),
                color=alt.Color('accident_type_name:N', title='사고유형'),
                tooltip=['age_group_range', 'accident_type_name', 'count']
            ).properties(title="연령대별 사고 유형")
            st.altair_chart(chart, use_container_width=True)

        elif index == 3:
            df = pd.read_sql(q4_query, con=engine)
            chart = alt.Chart(df).mark_bar(size=80).encode(
                x=alt.X('accident_type_name:N', title='사고유형'),
                y=alt.Y('count:Q', title='사고건수'),
                tooltip=['accident_type_name', 'count']
            ).properties(title="20세 이하 주요 사고 유형")
            st.altair_chart(chart, use_container_width=True)

        elif index == 4:
            df = pd.read_sql(q5_query, con=engine)
            chart = alt.Chart(df).mark_bar().encode(
                x=alt.X('accident_cause_type_name:N', title='사고유형(대분류)'),
                y=alt.Y('count:Q', title='사고건수'),
                color=alt.Color('accident_cause_type_list:N', title='사고유형(중분류)'),
                tooltip=['accident_cause_type_name', 'accident_cause_type_list', 'count']
            ).properties(title="새벽 시간대 사고 유형")
            st.altair_chart(chart, use_container_width=True)

        elif index == 5:
            df = pd.read_sql(q6_query, con=engine)
            chart = alt.Chart(df).mark_bar(size=30).encode(
                x=alt.X('time_slot_id:N', title='시간대'),
                y=alt.Y('count:Q', title='사고건수'),
                tooltip=['time_slot_id', 'count']
            ).properties(title="보행자 사고 시간대")
            st.altair_chart(chart, use_container_width=True)


# FAQ 전체 출력
for idx in range(len(faq_question_list)):
    faq_item(
        question=faq_question_list[idx],
        answer=faq_answer_list[idx],
        index=idx
    )

