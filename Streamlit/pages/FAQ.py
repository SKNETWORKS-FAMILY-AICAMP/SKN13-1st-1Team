import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import streamlit as st

st.title('자주 묻는 질문')

# Q1
st.subheader('[FAG1]')
st.markdown('### Q. 하루 중 어떤 시간대에 교통사고가 가장 많이 발생하나요?')
button1 = st.button('Q1 - 답변')
if button1:
    st.markdown(
        """
        A. 일반적으로 18`~`20시와 16`~`18시 사이에 사고 건수가 가장 많습니다. 이 시간대는 퇴근 시간대와 겹치며 차량 및 보행자 통행량이 증가하는 시간입니다.  
        """
        # 데이터: 시간대별 교통사고량
    )


# Q2
st.subheader('[FAG2]')
st.markdown('### Q. 연령대별로 가장 많은 사고가 발생하는 시간대는 언제인가요?')
button2 = st.button('Q2 - 답변')
if button2:
    st.markdown(
        """
        A. 20세 이하는 08`~`10시에 사고가 많으며, 주로 등교 시간대입니다.  
         > 61세 이상은 10`~`12시에 사고가 많은 편으로, 비교적 한산한 시간에 활동하는 경향이 반영된 것으로 보입니다.
         > 21~50세 연령대는 **출퇴근 시간대(08`~`10시, 18`~`20시)**에 사고가 집중됩니다.
        """
        # 데이터: 연령별 시간대별 막대 그래프 -> 시간대를 checkbox로
    )

# Q3
st.subheader('[FAG3]')
st.markdown('### Q. 사고 유형 중 ‘차대사람’ 사고는 어떤 시간대에 가장 많이 발생하나요?')
button1 = st.button('Q3 - 답변')
if button1:
    st.markdown(
        """
        A. ‘차대사람’ 사고는 **출근(08`~`10시)**과 퇴근(18`~`20시) 시간대에 집중적으로 발생합니다. 이 시간대에는 보행자와 차량의 혼잡도가 높기 때문에 사고 위험도 올라갑니다.
        """
        # 데이터: 차대사람 대분류의 시간대별
    )

# Q4
st.subheader('[FAG4]')
st.markdown('### Q. **횡단 중** 보행자 사고는 어느 시간대에 가장 많이 발생하나요?')
button1 = st.button('Q4 - 답변')
if button1:
    st.markdown(
        """
        A. ‘횡단 중’ 사고는 주로 18`~`20시에 발생합니다. 퇴근길 보행자와 차량이 복잡하게 얽히는 시간대이기 때문입니다. 이때는 특히 보행자 보호의무 위반으로 인한 사고 비율이 높습니다.  
        """
        # 데이터: 차대사람 대분류의 횡단중 소분류의 시간대별
    )

# Q5
st.subheader('[FAG5]')
st.markdown('### 61세 이상 고령자는 언제 교통사고를 가장 많이 당하나요?')
button1 = st.button('Q5 - 답변')
if button1:
    st.markdown(
        """
        A. 오전 10시부터 낮 4시 사이(10`~`16시)에 사고가 가장 많이 발생합니다. 이 시간대는 고령자들이 주로 외출하는 시간대로, 보행 중 사고가 특히 많습니다.
        """
        # 데이터: 61세 이상 연령의 시간대별
    )

# Q6
st.subheader('[FAG6]')
st.markdown('### Q. 차량단독 사고는 어떤 시간대에 많이 발생하나요?')
button1 = st.button('Q6 - 답변')
if button1:
    st.markdown(
        """
        A. ‘차량단독’ 사고는 주로 **야간 시간대(00`~`06시)**에 집중됩니다. 이 시간대에는 졸음운전, 음주운전, 시야 확보 부족 등의 요인으로 인해 사고 위험이 증가합니다.
        """
        # 데이터: 차량단독 대분류의 시간대별
    )