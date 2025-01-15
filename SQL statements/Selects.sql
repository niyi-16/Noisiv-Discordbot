
SELECT * from course;

select curdate(), (curdate() + interval 2 week );

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
where dayOfWeek = dayname(current_date)
and current_time between startTime and endTime;

# Selects next class on a given day
SELECT course.code_name, times.startTime, times.endTime
from times
join course
on course.id = times.course_id
where dayOfWeek = dayname(current_date)
  and startTime > current_time
limit 1;


SELECT course.code_name as 'c_code',
                        assignments.assignmentName as 'a_name',
                        DATE_FORMAT(assignments.dateDue,'%W, %D of %b')  as 'a_due',
                        time_format(assignments.timeDue, '%h:%i') as 'a_time'
from assignments
join course on course.id = assignments.course_id
where course_id is not null
and dateDue <= (curdate() + interval 2 week)
order by dateDue;