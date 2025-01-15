import datetime
import os
import mysql.connector
from dotenv import load_dotenv

def currclassT():

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



    query = f"""SELECT course.code_name as 'c_id', course.name as 'c_name'
                from times 
                join course 
                on course.id = times.course_id 
                where dayOfWeek = '{currDOW}' 
                and '{currTime}' between startTime and endTime;"""

    mycursor.execute(query)

    result = mycursor.fetchone()
    if result is None:
        return "Schools over, GO HOME!!"

    mycursor.close()
    mydb.close()

    return f"You currently have {result['c_id']} - {result['c_name']}"

def assignments():


def main():
    assignments = "assignments"
    course = "course"
    tests = "tests"
    times = "times"

    print(currclassT())

if __name__ == '__main__':
    main()