use courses;

UPDATE assignments
set course_id = 1
where assignmentName like '%icom%';

UPDATE assignments
set course_id = 2
where assignmentName like '%1000%';

UPDATE assignments
set course_id = 3
where assignmentName like '%1400%';

UPDATE assignments
set course_id = 4
where assignmentName like '%2007%';

UPDATE assignments
set course_id = 5
where assignmentName like '%2700%';

UPDATE assignments
set course_id = 6
where assignmentName like '%saad%';