
SELECT * from course;

SELECT * from assignments
where course_id is not null
order by dateDue;


select * from times;

select * from tests;

select dateDue, count(dateDue) as 'c' from tests
group by dateDue
having c >1 ;

# Selects current class on a given day
SELECT course.code_name, times.startTime, times.endTime
from times
join course
on course.id = times.course_id
where dayOfWeek = 'Monday'
and '09:00:00' between startTime and endTime;

# Selects next class on a given day
SELECT course.code_name, times.startTime, times.endTime
from times
join course
on course.id = times.course_id
where dayOfWeek = 'Tuesday'
  and startTime > '09:00:00'
limit 1;