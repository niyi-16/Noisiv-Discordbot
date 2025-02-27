CREATE schema courses;
Use courses;

DROP TABLE if exists course;
CREATE TABLE course
(
    id        int not null auto_increment primary key,
    name      VARCHAR(255),
    code_name VARCHAR(10)
);

DROP TABLE if exists times;
CREATE TABLE times
(
    course_id int not null,
    dayOfWeek VARCHAR(9),
    start     TIME,
    end       TIME,
    foreign key (course_id) references course (id)
);

DROP TABLE assignments;
CREATE TABLE assignments
(
    course_id      int not null,
    assignmentName VARCHAR(255),
    dateDue        DATE,
    timeDue        TIME default '23:59:59',
    foreign key (course_id) references course (id)
);

CREATE TABLE tests
(
    course_id int not null,
    testName  VARCHAR(255),
    dateDue   DATETIME,
    timeStart TIME,
    foreign key (course_id) references course (id)
);

CREATE TABLE holidays
(
    name            varchar(255) DEFAULT NULL,
    date            date         DEFAULT NULL,
    type            varchar(3)   DEFAULT NULL,
    class_scheduled tinyint      DEFAULT NULL
)

