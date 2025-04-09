import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import streamlit as st

st.title('FAQ')

# 10대 이하
st.markdown('### 10대 이하 어린이의 주요 교통사고 유형과 시간대는 무엇인가요?')
button1 = st.button('10대 이하 - 답변')
if button1:
    st.markdown(
        """
        **- 주요 사고유형:** 차대사람 사고 중 **횡단 중 사고**가 가장 많습니다.  
        **- 주요 시간대:** 오전 7`~`9시 (등교 시간), 오후 2`~`5시 (하교 시간)  
        **- 특징:** 보호자 없이 보행 중인 사고 비율이 높으며, **어린이 보호구역 내 사고**도 빈번합니다.
        """
    )


# 20대
st.markdown('### 20대 운전자는 어떤 사고유형이 많고 언제 발생하나요?')
button2 = st.button('20대 - 답변')
if button2:
    st.markdown(
        """
        **- 주요 사고유형:** 차대차 사고 중 **충돌과 추돌**, 차단독 사고 중 **도로이탈이나 전복사고**도 많은 편입니다.  
        **- 주요 시간대:** **야간 시간대(오후 8시~새벽 2시)**  
        **- 특징:** 과속, 졸음, 음주운전 등 위험요소가 많고, **주말에 집중**되는 경향이 있습니다.
        """
    )

