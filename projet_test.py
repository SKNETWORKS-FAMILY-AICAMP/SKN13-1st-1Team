import pandas as pd
from sqlalchemy import create_engine

# 1. CSV 파일 읽기
csv_path = r"C:\Users\mycom\Downloads\2023년_시간대별_사고통계.csv"  # 파일 경로에 맞게 수정
df = pd.read_csv(csv_path)
print(df.head())
# 2. MySQL 접속 정보 설정
user = 'root'
password = '1111'
host = 'localhost'
port = 3306
database = 'crawl'

# 3. SQLAlchemy 엔진 생성
engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}')

# 4. 테이블에 데이터 삽입 (if_exists='append'로 설정하여 데이터를 추가)
table_name = 'accidentstatstime'
try:
    # 데이터를 추가하기 전에 기존 테이블에서 컬럼 정보 확인
    df.to_sql(table_name, con=engine, index=False, if_exists='append')  
    print(f"✅ '{table_name}' 테이블로 데이터가 정상적으로 추가되었습니다!")
except Exception as e:
    print(f"오류 발생: {e}")
