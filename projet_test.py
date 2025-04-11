# import pandas as pd
# from sqlalchemy import create_engine

# # 1. CSV 파일 읽기
# csv_path = r"C:\Users\mycom\Downloads\accidents_by_age_and_type2014.csv"  # 파일 경로에 맞게 수정
# df = pd.read_csv(csv_path)
# print(df.head())
# # 2. MySQL 접속 정보 설정
# user = 'root'
# password = '1111'
# host = 'localhost'
# port = 3306
# database = 'crawl'

# # 3. SQLAlchemy 엔진 생성
# engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}')

# # 4. 테이블에 데이터 삽입 (if_exists='append'로 설정하여 데이터를 추가)
# table_name = 'accidentstatsage'
# try:
#     # 데이터를 추가하기 전에 기존 테이블에서 컬럼 정보 확인
#     df.to_sql(table_name, con=engine, index=False, if_exists='append')  
#     print(f"✅ '{table_name}' 테이블로 데이터가 정상적으로 추가되었습니다!")
# except Exception as e:
#     print(f"오류 발생: {e}")


import pandas as pd
from sqlalchemy import create_engine

# CSV 파일 경로
csv_path = r"C:\Users\mycom\Downloads\accidents_by_age_and_type2023.csv"

# CSV 읽기
df = pd.read_csv(csv_path)

# 컬럼명 정리
df.columns = ['id', 'year_type_id', 'age_group_range', 'accident_type_name', 'indicator', 'value']

# 공백 제거
df['indicator'] = df['indicator'].str.strip()
df['accident_type_name'] = df['accident_type_name'].str.strip()
df['age_group_range'] = df['age_group_range'].str.strip()

# 사고건수(사고[건])만 필터링
df_accident = df[df['indicator'] == '사고[건]']

# 컬럼명 정리
df_accident = df_accident.rename(columns={
    'value': 'accident_count'
})

# 필요한 컬럼만 추출
df_accident = df_accident[['id', 'age_group_range', 'year_type_id', 'accident_type_name', 'accident_count']]

# id와 year_type_id를 str로 변환 (VARCHAR 컬럼 맞춤)
df_accident['id'] = df_accident['id'].astype(str)
df_accident['year_type_id'] = df_accident['year_type_id'].astype(str)

# DB 연결 설정
user = 'root'
password = '1111'
host = 'localhost'
port = 3306
database = 'crawl'

engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}')

# 테이블명
table_name = 'accidentstatsage'

# 삽입 시도
try:
    df_accident.to_sql(table_name, con=engine, index=False, if_exists='append')
    print("✅ 데이터 삽입 성공!")
except Exception as e:
    print(f"❌ 삽입 실패: {e}")
