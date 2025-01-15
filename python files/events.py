import datetime
import os
from time import sleep

import mysql.connector
from dotenv import load_dotenv

def currclassT(db):


    mycursor = db.cursor(dictionary=True)

    current = datetime.datetime.now()  # Gets info about the current day "YYYY-MM-DD HH:MM:SS.milliseconds"

    currDOW = current.strftime("%A")  # Extracts day of week from current
    currTime = (current.strftime("%H:%M:%S"))  # Extracts the current time in specified format



    query = f"""SELECT course.code_name as 'c_id', course.name as 'c_name'
                from times 
                join course 
                on course.id = times.course_id 
                where dayOfWeek = '{currDOW}' 
                and '11:30:00' between startTime and endTime;"""

    mycursor.execute(query)

    result = mycursor.fetchone()
    return f"You currently have {result['c_id']} - {result['c_name']}"


    # td_Schdl = classSchedule[currDOW]  # Uses currentDow as a key to retrieve day's schedule

    # print(f"Today is a {currDOW}\n" +
    #       f"The current time is {currTime}\n" +
    #       f"The Classes lined up for the day are {str(td_Schdl)}\n")
    #
    # if 0 < currTime < 10.30:  # 12AM - 10:30AM
    #     return f"You are currently in {td_Schdl[0]}"
    #
    # elif 10.30 < currTime < 11.30:  # 10:30AM - 11:30AM
    #     return f"You are currently in {td_Schdl[1]}"
    #
    # elif 11.30 < currTime < 12.30:  # 11:30AM - 12:30AM
    #     return f"You are currently in {td_Schdl[2]}"
    #
    # elif 12.30 < currTime < 13.30:  # 12:30AM - 1:30PM
    #     return f"You are currently in {td_Schdl[3]}"
    #
    # elif 13.30 < currTime < 15.30:  # 12:30AM - 3:30PM
    #     return f"You are currently in {td_Schdl[4]}"
    #
    # return "The day is over, try !nextclass, !assignments, !duedates or !commands for a list of my commands^^"

def main():

    load_dotenv()

    mydb = mysql.connector.connect(
        host=os.getenv('HOST'),
        user=os.getenv('USER'),
        password=os.getenv('PASS'),
        database=os.getenv('DATABASE'))


    assignments = "assignments"
    course = "course"
    tests = "tests"
    times = "times"

    print(currclassT(mydb))


if __name__ == '__main__':
    main()