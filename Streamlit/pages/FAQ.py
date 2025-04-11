import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import streamlit as st
import pymysql
from typing import Callable

conn = pymysql.connect(
    host="localhost",    # DBMS 의 ip(host) : str
    port=3306,           # DBMS의 port 번호: int
    user='root',        # username: str
    password="1234",    # password: str
    db="crawl"
)
cursor = conn.cursor()
# 질문 1~6 sql select query
####### 수정 필요 #######
q1_query = """
select 사고유형대분류, 사고유형중분류, 연령대, 값 from accidentstatsage where 연령대 = '65세이상'
"""
q2_query = """
select 시간대, 사고유형중분류, 값 from accidentstatstime where 사고유형대분류 = "차대차" and 사고유형중분류 = "충돌"
"""
# 수정 필요?
q3_query = """
select 연령대, 사고유형대분류, 사고유형중분류, 값 from accidentstatsage
"""
q4_query = """
select 사고유형대분류, 사고유형중분류, 값 from accidentstatsage where 연령대 = '20세이하'
"""
q5_query = """
select 사고유형대분류, 사고유형중분류, 값 from accidentstatstime where 시간대 in ('00~02시', '02~04시', '04~06시')
"""
q6_query = """
select 시간대, 값 from accidentstatstime where 사고유형대분류 = '차대사람' and 사고유형중분류 = '횡단중'
"""


# 상단 고정 제목
st.title('자주 묻는 질문')


# FAQ 질문과 답변을 expander로 출력하는 함수
def faq_item(question: str, answer: str, index: int, expanded: bool = False):
  
    q1_df = pd.DataFrame(rows, columns=["연령대", "사고유형", "값"])
    q2_df = pd.DataFrame(rows, columns=["시간대", "사고유형중분류", "값"])
    q3_df = pd.DataFrame(rows, columns=["연령대", "사고유형대분류", "값"])
    q4_q5_df = pd.DataFrame(rows, columns=["사고유형대분류", "사고유형중분류", "값"])
    q6_df = pd.DataFrame(rows, columns=["시간대", "값"])
    
    # q1 그래프
    q1_chart = alt.Chart(q1_df).mark_bar(size=50).encode(
        x=alt.X('시간대:N', title='시간대'),
        y=alt.Y('값:Q', title='사고건수'),
        color=alt.Color('사고유형:N', title='사고유형'),
        tooltip=['시간대', '사고유형', '값']
    ).properties(
        width=100,
        height=450,
        title='65세 이상 교통사고 유형'
    ).interactive()

    # q2 그래프
    q2_chart = alt.Chart(q2_df).mark_bar(size=50).encode(
        x=alt.X('시간대:N', title='시간대'),
        y=alt.Y('값:Q', title='사고건수'),
        color=alt.Color('사고유형:N', title='사고유형'),
        tooltip=['시간대', '사고유형', '값']
    ).properties(
        width=100,
        height=450,
        title='차대차 - 추돌 교통사고 주요 시간대'
    ).interactive()

    # q3 그래프
    q3_chart = alt.Chart(q3_df).mark_bar(size=50).encode(
        x=alt.X('연령대:N', title='연령대'),
        y=alt.Y('값:Q', title='사고건수'),
        color=alt.Color('사고유형:N', title='사고유형(중분류)'),
        tooltip=['시간대', '사고유형', '값']
    ).properties(
        width=100,
        height=450,
        title='연령대별 주요 교통사고 유형'
    ).interactive()

    # q4 그래프
    q4_chart = alt.Chart(q4_q5_df).mark_bar(size=50).encode(
        x=alt.X('사고유형대분류:N', title='사고유형(대분류)'),
        y=alt.Y('값:Q', title='사고건수'),
        color=alt.Color('사고유형중분류:N', title='사고유형(중분류)'),
        tooltip=['사고유형', '사고건수', '사고유형중분류']
    ).properties(
        width=100,
        height=450,
        title='20세 이하 주요 교통사고 유형'
    ).interactive()
    
    # q5 그래프
    q5_chart = alt.Chart(q4_q5_df).mark_bar(size=50).encode(
        x=alt.X('사고유형대분류:N', title='사고유형(대분류)'),
        y=alt.Y('값:Q', title='사고건수'),
        color=alt.Color('사고유형중분류:N', title='사고유형(중분류)'),
        tooltip=['사고유형대분류', '사고유형', '값']
    ).properties(
        width=100,
        height=450,
        title='새벽 시간대 주요 교통사고 유형'
    ).interactive()

    # q6 그래프
    q6_chart = alt.Chart(q6_df).mark_bar(size=50).encode(
        x=alt.X('시간대:N', title='시간대'),
        y=alt.Y('값:Q', title='사고건수'),
        tooltip=['시간대', '사고유형', '값']
    ).properties(
        width=100,
        height=450,
        title='보행자 교통사고 주요 시간대'
    ).interactive()

    with st.expander(f"❓ Q. {question}", expanded=expanded):
        st.markdown(answer)

    with conn.cursor() as cursor:
      if index == 0:
          cursor.execute(q1_query)
          rows = cursor.fetchall()
          st.altair_chart(q1_chart, use_container_width=True)
      elif index == 1:
          cursor.execute(q2_query)
          rows = cursor.fetchall()
          st.altair_chart(q2_chart, use_container_width=True)
      elif index == 2:
          cursor.execute(q3_query)
          rows = cursor.fetchall()
          st.altair_chart(q3_chart, use_container_width=True)
      elif index == 3:
          cursor.execute(q4_query)
          rows = cursor.fetchall()
          st.altair_chart(q4_chart, use_container_width=True)
      elif index == 4:
          cursor.execute(q5_query)
          rows = cursor.fetchall()
          st.altair_chart(q5_chart, use_container_width=True)
      else:
          cursor.execute(q6_query)
          rows = cursor.fetchall()
          st.altair_chart(q6_chart, use_container_width=True)


# faq 질문 list
faq_question_list = [
    "65세 이상 고령층은 어떤 유형의 교통사고에 가장 많이 노출되나요?", # 65세 이상 유형별 교통사고
    "출퇴근 시간대에 많이 발생하는 교통사고 유형은 무엇인가요?", # 08시 ~ 10시/ 18~20시 유형별 교통사고
    "연령대에 따라 가장 흔한 교통사고 유형은 어떻게 다르게 나타나나요?", # 연령대별 교통사고 유형
    "20세 이하 연령층에서 주로 발생하는 사고는 어떤 유형인가요?", # 20세 이하 
    "새벽 시간대(00`~`06시)에 자주 발생하는 사고 유형은 무엇인가요?",
    "보행자 사고는 어떤 시간대에 집중되나요?"
]


# faq 답변 list
faq_answer_list = [
    """그래프를 보면 61세 이상 연령대에서는 차대사람 - 횡단중 사고가 가장 높은 비율을 차지하고 있습니다.
다른 유형보다 확연히 높은 건수를 기록하며 눈에 띄는 차이를 보입니다.
이 결과는 고령 보행자들이 도로 횡단 시 판단력 저하, 반응 속도 감소 등으로 인해
사고 위험에 더욱 쉽게 노출되는 경향을 나타내는 것으로 해석할 수 있습니다.""",

    """18`~`20시 퇴근 시간대에 차대차 - 추돌 사고가 가장 많이 발생한 것으로 나타났습니다.
이 시간대는 사고 건수가 12,000건을 넘는 유일한 구간으로, 전체 시간대 중 가장 높은 수치를 기록했습니다.

퇴근 시간에는 차량 밀집, 급정거, 차선 변경 등이 빈번하게 발생하면서 추돌 사고 위험이 급격히 높아지는 경향을 보입니다.""",

    """그래프를 보면 61세 이상은 보행 중 사고(특히 횡단 중 사고)가 두드러지고,
20세 이하는 역시 보행 중 사고 비율이 높지만 전반적인 사고 건수는 적은 편입니다.
반면 21세에서 50세까지의 연령대는 차대차 사고, 특히 추돌 사고가 가장 많게 나타납니다.

이러한 차이는 각 연령대의 이동 수단과 생활 패턴이 사고 유형에 반영된 것으로 보입니다.
고령층과 청소년은 보행자 사고에 더 취약하고, 운전 활동이 많은 중년층은 차량 간 충돌 사고 위험이 높은 것으로 해석할 수 있습니다.""",

    """20세 이하에서는 차대사람 - 횡단중 사고 비중이 가장 높습니다.
차량 간 충돌보다 보행 중 사고가 더 많은 것으로 나타났습니다.

이는 해당 연령대가 차량 운전자보다는 보행자로서 도로를 이용할 가능성이 크며,
특히 등하교 시간대 도로 횡단 중 사고가 집중되는 경향을 반영하는 것으로 볼 수 있습니다.""",

    """차량단독 - 도로이탈 사고가 새벽 시간대에서 가장 높게 나타납니다.
특히 02`~`04시 구간에서 두드러집니다.

이는 졸음운전, 야간 시야 부족, 음주운전 등과 관련된 단독 사고의 가능성을 시사합니다.""",

    """차대사람 - 횡단중 사고는 08`~`10시와 18`~`20시 시간대에서 가장 많이 발생했습니다.

이 시간대는 통학 및 퇴근 시간과 겹치며,
보행자와 차량 간 충돌 위험이 커지는 시기임을 나타냅니다."""
]


for v in range(len(faq_question_list)):
        faq_item(question=faq_question_list[v], answer=faq_answer_list[v], index = v)
