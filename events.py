import datetime
from time import sleep

def main():
    while True:
        now = datetime.datetime.now()
        daysofweek = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

        courses = ["OSYS 1000", "PROG 2007","SAAD 1001", "PROG 2700", "PROG 1400", "ICOM 2701"]

        classSchedule = {
            "Monday": [courses[0], courses[1], "BREAK", courses[1], courses[2]],
            "Tuesday": [courses[1], courses[3], "BREAK", courses[3], courses[4]],
            "Wednesday": [courses[3], courses[4], "BREAK", courses[4], courses[2]],
            "Thursday": [courses[3], courses[0], "BREAK", courses[0], courses[5]],
            "Friday": "No Classes on Friday"
        }



        today = classSchedule[now.strftime("%A")]
        tommorow = classSchedule[daysofweek[1 + daysofweek.index(now.strftime("%A"))]]
        currTime = float(now.strftime("%H.%M"))


        print(now.strftime("%A"))
        print(currTime)
        print(today)

        if 0 < currTime < 10.30:
            print(today[0])
        elif 10.30 < currTime < 11.30:
            print(today[1])
        elif 11.30 < currTime < 12.30:
            print(today[2])
        elif 12.30 < currTime < 13.30:
            print(today[3])
        elif 13.30 < currTime < 15.30:
            print(today[4])
        break
        print(tommorow[0])
        # sleep(600)


if __name__ == '__main__':
    main()