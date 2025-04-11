CREATE DATABASE CRAWL;
use crawl;

-- AccidentType 테이블 생성 및 데이터 대입
CREATE TABLE AccidentType (
    type_name VARCHAR(30) PRIMARY KEY not null
);

insert into accidenttype(type_name)
select distinct
사고유형대분류 as type_name
from accident_by_time;

select * from accidenttype;
###################################
-- AccidentCause 테이블 생성 및 데이터 대입 
create table accidentcause(
type_name varchar(30) not null,
type_list varchar(100) not null,
primary key (type_name, type_list),   # 복합 PK  
foreign key (type_name) references accidenttype(type_name));
# accidentstatstime이 type_name을 참조하려면 unique(제약) / (단일)PK가 있어야한다. 


insert into accidentcause(type_name,type_list)
select distinct
사고유형대분류 as type_name,
사고유형중분류 as type_list
from accident_by_time;

delete from	accidentcause
where type_name is null and type_list is null;
select * from accidentcause;

#######################################
-- timeslot 테이블 생성 및 데이터 기입
CREATE TABLE TimeSlot (
    time_range VARCHAR(30) PRIMARY KEY
);

insert into TimeSlot(time_range)
select distinct
시간대 as time_range
from accident_by_time ;


###########################################
-- yeartype 생성 및 데이터 기입
CREATE TABLE YEARTYPE (
	ID VARCHAR(30) PRIMARY KEY);
    
insert into yeartype(ID)
Values
('2014'),('2015'),('2016'),('2017'),('2018'),
('2019'),('2020'),('2021'),('2022'),('2023');

###########################################
-- accidentstatstime table 생성 및 데이터 기입

CREATE TABLE AccidentStatsTime (
    id VARCHAR(50) PRIMARY KEY not null,
    accident_cause_type_name varchar(100) not null,
    accident_cause_type_list VARCHAR(30) not null,
    time_slot_id VARCHAR(30) not null,
    year_type_id VARCHAR(30) not null,
    accident_count INT not null,
    injury_count INT not null,
    death_count INT not null,
    FOREIGN KEY (accident_cause_type_name,accident_cause_type_list) REFERENCES accidentcause(type_name,type_list) ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (time_slot_id) REFERENCES timeslot(time_range) ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (year_type_id) REFERENCES yeartype(id) ON UPDATE CASCADE ON DELETE RESTRICT
);


INSERT INTO Accidentstatstime (
    id,
    year_type_id,
    accident_cause_type_name,
    accident_cause_type_list,
    time_slot_id,
    accident_count,
    injury_count,
    death_count
)
SELECT
	ROW_NUMBER() OVER () AS id,
    '2014' as year_type_id,
    사고유형대분류 AS accident_cause_type_list,
    사고유형중분류 AS accident_cause_type_name,
    시간대 AS time_slot_id,
    CAST(MAX(CASE WHEN 구분 = '사고[건]' THEN 값 END) AS UNSIGNED) AS accident_count,
    CAST(MAX(CASE WHEN 구분 = '부상[명]' THEN 값 END) AS UNSIGNED) AS injury_count,
    CAST(MAX(CASE WHEN 구분 = '사망[명]' THEN 값 END) AS UNSIGNED) AS death_count
FROM accident_by_time
GROUP BY 사고유형대분류, 사고유형중분류, 시간대;


select * from Accidentstatstime order by 1;
