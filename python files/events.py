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
                and dateDue <= (curdate() + interval 2 week)
                order by dateDue;'''

    mycursor.execute(query)
    result = mycursor.fetchall()

    return result

def duedates() -> dict:
    load_dotenv()
    mydb = mysql.connector.connect(
        host=os.getenv("HOST"),
        user=os.getenv("USER"),
        password=os.getenv("PASS"),
        database=os.getenv("DATABASE")
    )

    mycursor = mydb.cursor(dictionary=True)

    query  = ""

def main():
    #Table Names
    assignment = assignments()
    course = "course"
    tests = "tests"
    times = "times"

    for item in assignment:
        print(f"{item["c_code"]} {item['a_name']} is due {item['a_due']} by {item['a_time']}")

if __name__ == '__main__':
    main()