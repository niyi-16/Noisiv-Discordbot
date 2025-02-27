import datetime
import os

import mysql.connector
import random
from dotenv import load_dotenv

##TODO Polish code its messy!


# dict of bot functions

bot_functions_call = [
    {"command": "!curr", "description": "Get the current class"},  # Done
    {"command": "!next", "description": "Get the next class"},  # Done
    {"command": "!assignments", "description": "Get all assignments due within a week"},
    {"command": "!tests", "description": "Get all tests due within a week"},
    {"command": "!duedates", "description": "Get all due dates for the rest of the semester"},
    {"command": "!list", "description": "List all commands"},
    {"command": "!courses", "description": "Get all courses for the current semester"},
    {"command": "!remind <COURSE-ID>", "description": "Subscribe to reminders about a course for th week"},
]
bot_functions_auto = {
    "!remind": "Send a reminder that something is due depending on week",
}

load_dotenv()

mydb = mysql.connector.connect(
    host=os.getenv("HOST"),
    user=os.getenv("USER"),
    password=os.getenv("PASS"),
    database=os.getenv("DATABASE"))


def currclass() -> str:
    my_cursor = mydb.cursor(dictionary=True)

    current = datetime.datetime.now()  # Gets info about the current day "YYYY-MM-DD HH:MM:SS.milliseconds"

    current_day_of_week = current.strftime("%A")  # Extracts day of week from current
    current_time = (current.strftime("%H:%M:%S"))  # Extracts the current time in specified format

    query = f"""SELECT course.code_name as 'c_code', course.name as 'c_name'
                    from times 
                    join course 
                    on course.id = times.course_id 
                    where dayOfWeek = '{current_day_of_week}' 
                    and '{current_time}' between start and end;"""

    my_cursor.execute(query)

    result = my_cursor.fetchone()

    if result is None:
        response = ["The day is over, try !next, !assignments, !duedates or !list for a list of my commands^^",
                    "Schools over, GO HOME!!"]

        return response[random.randint(0, 1)]

    my_cursor.close()
    mydb.close()

    return f"You currently have {result['c_code']} - {result['c_name']}"


def nextclass():
    my_cursor = mydb.cursor(dictionary=True)

    current = datetime.datetime.now() # Gets info about the current day "YYYY-MM-DD HH:MM:SS.milliseconds"

    current_day_of_week = current.strftime("%A") # Extracts day of week from current
    current_time = (current.strftime("%H:%M:%S"))  # Extracts the current time in specified format

    if current_day_of_week in ["Saturday", "Sunday"]:
        return "The week is over, try /assignments, /duedates or /list for a list of my commands^^"


    query = f"""SELECT course.code_name as 'c_code', course.name as 'c_name', times.dayOfWeek as 'dow', start
                from times
                join course
                on course.id = times.course_id
                where dayOfWeek = '{current_day_of_week}'
                  and start > '{current_time}'
                limit 1;"""
    my_cursor.execute(query)

    result = my_cursor.fetchone()
    print(result)

    if result is None:
        return "The day is over, try !next, !assignments, !duedates or !list for a list of my commands^^"

    return result
    # return f"The Next class is {result['c_code']} - {result['c_name']}"


def assignments() -> list:
    my_cursor = mydb.cursor(dictionary=True)

    query = '''SELECT course.code_name as 'c_code', course.name as 'c_name',
                        assignments.assignmentName as 'a_name', 
                         DATE_FORMAT(assignments.dateDue,'%Y/%m/%d') as 'a_due',
                         # DATE_FORMAT(assignments.dateDue,'%W, %D of %b') as 'a_due',
                        time_format(assignments.timeDue, '%H:%i:%s') as 'a_time'
                from assignments
                join course on course.id = assignments.course_id
                where course_id is not null
                and dateDue between curdate() and (curdate() + interval 2 week) 
                order by dateDue;'''

    my_cursor.execute(query)
    result = my_cursor.fetchall()

    return result

def duedates():
    my_cursor = mydb.cursor(dictionary=True)

    query = '''
  SELECT combined.name, due, time, code_name
FROM (
         SELECT tests.testName AS `name`,
                tests.course_id as id,
                tests.dateDue as `due`,
                tests.timeStart AS `time`
         FROM tests

         UNION

         SELECT assignments.assignmentName AS `name`,
                assignments.course_id as id,
            assignments.dateDue  AS `due`,
                assignments.timeDue  AS `time`
         FROM assignments
     ) AS combined
join course on combined.id = course.id
WHERE combined.name IS NOT NULL
order by due asc
    '''

    my_cursor.execute(query)
    result = my_cursor.fetchall()
    return result


def tests():
    my_cursor = mydb.cursor(dictionary=True)

    query = '''SELECT course.code_name as 'c_code', course.name as 'c_name',
                    tests.testName as 't_name', 
                         DATE_FORMAT(tests.dateDue,'%W, %D of %b') as 't_due',
                        time_format(tests.timeStart, '%h:%i') as 't_time'
                from tests
                join course on course.id = tests.course_id
                where course_id is not null
                and dateDue between curdate() and (curdate() + interval 1 week) 
                order by dateDue;'''

    my_cursor.execute(query)
    result = my_cursor.fetchall()

    return result


def courses() -> list:
    my_cursor = mydb.cursor(dictionary=True)

    query = '''
    Select code_name as 'c_code', name 
    from course; 
    '''

    my_cursor.execute(query)
    result = my_cursor.fetchall()

    return result

def commands():
    item = ""
    for commands, desc in bot_functions_call.items():
        item += f"{commands} - {desc}\n"
    return item
