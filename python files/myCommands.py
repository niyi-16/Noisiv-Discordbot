import datetime
import os

import mysql.connector
import random
from dotenv import load_dotenv

##TODO Polish code its messy!


# dict of bot functions
bot_functions_call = {
    "!curr": "Get the current class",  #Done
    "!next": "Get the next class", # Done
    "!assignments": "Get all assignments due within two weeks",
    "!duedates": "Get all due dates for the rest of the sem",
    "!list": "list all commands"
}

bot_functions_auto = {
    "!remind": "Send a reminder that something is due depending on week",
}

def currclass() -> str:
    load_dotenv()

    mydb = mysql.connector.connect(
        host=os.getenv("HOST"),
        user=os.getenv("USER"),
        password=os.getenv("PASS"),
        database=os.getenv("DATABASE"))

    mycursor = mydb.cursor(dictionary=True)

    current = datetime.datetime.now()  # Gets info about the current day "YYYY-MM-DD HH:MM:SS.milliseconds"

    currDOW = current.strftime("%A")  # Extracts day of week from current
    currTime = (current.strftime("%H:%M:%S"))  # Extracts the current time in specified format



    query = f"""SELECT course.code_name as 'c_code', course.name as 'c_name'
                    from times 
                    join course 
                    on course.id = times.course_id 
                    where dayOfWeek = '{currDOW}' 
                    and '{currTime}' between startTime and endTime;"""

    mycursor.execute(query)

    result = mycursor.fetchone()

    if result is None:
        response = ["The day is over, try !next, !assignments, !duedates or !list for a list of my commands^^",
                "Schools over, GO HOME!!"]

        return response[random.randint(0,1)]

    mycursor.close()
    mydb.close()

    return f"You currently have {result['c_code']} - {result['c_name']}"


def nextclass():

    load_dotenv()

    mydb = mysql.connector.connect(
        host=os.getenv("HOST"),
        user=os.getenv("USER"),
        password=os.getenv("PASS"),
        database=os.getenv("DATABASE"))

    mycursor = mydb.cursor(dictionary=True)

    current = datetime.datetime.now() # Gets info about the current day "YYYY-MM-DD HH:MM:SS.milliseconds"

    currDOW = current.strftime("%A")  # Extracts day of week from current
    currTime = (current.strftime("%H:%M:%S"))  # Extracts the current time in specified format

    query = f"""SELECT course.code_name as 'c_code', course.name as 'c_name'
                from times
                join course
                on course.id = times.course_id
                where dayOfWeek = '{currDOW}'
                  and startTime > '{currTime}'
                limit 1;"""
    mycursor.execute(query)

    result = mycursor.fetchone()

    if result is None:
        return "Next Class is tommorow!"

    #TODO some thing about the next day
    #tmr_Schdl = classSchedule[daysofweek[1 + daysofweek.index(currDOW)]]

    return f"The Next class is {result['c_code']} - {result['c_name']}"


def assignments() -> dict:
    load_dotenv()
    mydb = mysql.connector.connect(
        host=os.getenv("HOST"),
        user=os.getenv("USER"),
        password=os.getenv("PASS"),
        database=os.getenv("DATABASE")
    )

    mycursor = mydb.cursor(dictionary=True)

    query = '''SELECT course.code_name as 'c_code', course.name as 'c_name',
                        assignments.assignmentName as 'a_name', 
                         DATE_FORMAT(assignments.dateDue,'%W, %D of %b') as 'a_due',
                        time_format(assignments.timeDue, '%h:%i') as 'a_time'
                from assignments
                join course on course.id = assignments.course_id
                where course_id is not null
                and dateDue between curdate() and (curdate() + interval 2 week) 
                order by dateDue;'''

    mycursor.execute(query)
    result = mycursor.fetchall()

    return result

def duedates():
    pass

def commands():
    item = ""
    for commands, desc in bot_functions_call.items():
        item += f"{commands} - {desc}\n"
    return item
