import datetime
bot_functions = {
    "!curr": "Get the current class",
    "!next": "Get the next class",
    "!assignments": "Get all assignments due within two weeks",
    "!duedates": "Get all due dates for the sem",
    "!list": "list all commands"
}


daysofweek = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

#            0              1            2           3            4             5
courses = ["OSYS 1000", "PROG 2007","SAAD 1001", "PROG 2700", "PROG 1400", "ICOM 2701"]

classSchedule = dict(Monday=[courses[0], courses[1], "BREAK", courses[1], courses[2]],
                     Tuesday=[courses[1], courses[3], "BREAK", courses[3], courses[4]],
                     Wednesday=[courses[3], courses[4], "BREAK", courses[4], courses[2]],
                     Thursday=[courses[3], courses[0], "BREAK", courses[0], courses[5]],
                     Friday="No Classes on Friday")

def currclass() -> str:
    """

    :return: The Current Class based on the time
    """

    current = datetime.datetime.now() # Gets info about the current day "YYYY-MM-DD HH:MM:SS.milliseconds"
    
    currDOW = current.strftime("%A") # Extracts day of week from current
    currTime = float(current.strftime("%H.%M")) # Extracts the current time from current as a decimal number i.e 12:34 -> 12.34
    td_Schdl = classSchedule[currDOW] #Uses currentDow as a key to retrieve day's schedule
    
    print(f"Today is a {currDOW}\n"+
          f"The current time is {currTime}\n"+
          f"The Classes lined up for the day are {str (td_Schdl)}\n")

    if 0 < currTime < 10.30: # 12AM - 10:30AM
        return f"You are currently in {td_Schdl[0]}"

    elif 10.30 < currTime < 11.30: # 10:30AM - 11:30AM
        return f"You are currently in {td_Schdl[1]}"

    elif 11.30 < currTime < 12.30: # 11:30AM - 12:30AM
        return f"You are currently in {td_Schdl[2]}"

    elif 12.30 < currTime < 13.30: #12:30AM - 1:30PM
        return f"You are currently in {td_Schdl[3]}"

    elif 13.30 < currTime < 15.30: #12:30AM - 3:30PM
        return f"You are currently in {td_Schdl[4]}"

    return "The day is over, try !nextclass, !assignments, !duedates or !commands for a list of my commands^^"

def nextclass():

    current = datetime.datetime.now() # Gets info about the current day "YYYY-MM-DD HH:MM:SS.milliseconds"

    currDOW = current.strftime("%A") # Extracts day of week from current
    currTime = float(current.strftime("%H.%M")) # Extracts the current time from current as a decimal number i.e 12:34 -> 12.34
    td_Schdl = classSchedule[currDOW] #Uses currentDow as a key to retrieve day's schedule
    tmr_Schdl = classSchedule[daysofweek[1 + daysofweek.index(currDOW)]]


    if 0 < currTime < 8.30:
        return f"Your next class is {td_Schdl[0]}"
    elif 8.30 < currTime < 10.30:
        return f"Your next class is {td_Schdl[1]}"
    elif 10.30 < currTime < 11.30:
        return f"Your next class is {td_Schdl[2]}"
    elif 11.30 < currTime < 12.30:
        return f"Your next class is {td_Schdl[3]}"
    elif 12.30 < currTime < 13.30:
        return f"Your next class is {td_Schdl[4]}"
    elif currTime > 13.30:
        return f"Your next class is {tmr_Schdl[0]}"

#TODO
def assignments():
    pass

def duedates():
    pass

def commands():
    item = ""
    for commands, desc in bot_functions.items():
        item += f"{commands} - {desc}\n"
    return item

print(currclass())
print(nextclass())
print(commands())