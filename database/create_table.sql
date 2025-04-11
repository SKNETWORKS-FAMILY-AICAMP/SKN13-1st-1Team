CREATE TABLE AccidentStatsAge (
    id VARCHAR(50) PRIMARY KEY,
    year_type_id VARCHAR(30) not null,
    age_group_range VARCHAR(50) not null,
    accident_type_name varchar(30) not null,
    measure varchar(30) not null,
    count INT not null,
    FOREIGN KEY (age_group_range) REFERENCES AgeGroup(age_range),
    FOREIGN KEY (accident_type_name) REFERENCES AccidentType(type_name),
    FOREIGN KEY (year_type_id) REFERENCES YearType(id)
);


CREATE TABLE AccidentStatsTime (
    id VARCHAR(50) PRIMARY KEY,
    year_type_id VARCHAR(30) not null,
    accident_cause_type_name varchar(100) not null,
    accident_cause_type_list VARCHAR(30) not null,
    measure VARCHAR(30) not null,
    time_slot_range VARCHAR(30) not null,
    count INT not null,
    FOREIGN KEY (accident_cause_type_name, accident_cause_type_list) REFERENCES AccidentCause(type_name, type_list) ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (time_slot_range) REFERENCES TimeSlot(time_range) ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (year_type_id) REFERENCES YearType(id) ON UPDATE CASCADE ON DELETE RESTRICT
);



CREATE TABLE TimeSlot (
    time_range VARCHAR(30) PRIMARY KEY
);


CREATE TABLE AgeGroup (
    age_range VARCHAR(50) PRIMARY KEY
);


CREATE TABLE YearType (
    id VARCHAR(30) PRIMARY KEY
);


CREATE TABLE AccidentCause (
    type_name VARCHAR(30),
    type_list VARCHAR(100),
    PRIMARY KEY (type_name, type_list),
    Foreign key (type_name) REFERENCES AccidentType(type_name)
);


CREATE TABLE AccidentType (
    type_name VARCHAR(30) PRIMARY KEY
)