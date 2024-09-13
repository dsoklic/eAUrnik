#
#  Timetable.py
#  eAUrnik
#

import Parser
import Calendar
import requests
import datetime

def get(school, class_):
    today = datetime.date.today()
    monday = today + datetime.timedelta(days = -today.weekday())
    if today.weekday() == 5 or today.weekday() == 6: # Saturday or Sunday
        monday += datetime.timedelta(weeks = 1)

    schoolyear = today.year
    if today.month < 8:
        schoolyear -= 1
    schoolyearStart = datetime.date(schoolyear, 9, 1)
    while schoolyearStart.weekday() == 5 or schoolyearStart.weekday() == 6:
        schoolyearStart += datetime.timedelta(days = 1)

    week = 1
    for i in range((monday - schoolyearStart).days):
        if (schoolyearStart + datetime.timedelta(days = i + 1)).weekday() == 0:
            week += 1
            
    session = requests.Session()
    session.get("https://www.easistent.com")
    
    # Remove all cookies except "vxcaccess", as they cause further requests to be rejected.
    for cookie in session.cookies:
        name = cookie.name
        if name != "vxcaccess":
            session.cookies.pop(name)
            
    URL = "https://www.easistent.com/urniki/izpis/" + school + "/" + str(class_) + "/0/0/0/" + str(week)
    response = session.get(URL)
    
    lessons = Parser.lessons(response.content)
    timetable = Calendar.make(lessons, monday)
    
    return timetable

def get_teacher(school, teacher):
    today = datetime.date.today()
    monday = today + datetime.timedelta(days = -today.weekday())
    if today.weekday() == 5 or today.weekday() == 6: # Saturday or Sunday
        monday += datetime.timedelta(weeks = 1)
            
    session = requests.Session()
    session.get("https://www.easistent.com")
    
    # Remove all cookies except "vxcaccess", as they cause further requests to be rejected.
    for cookie in session.cookies:
        name = cookie.name
        if name != "vxcaccess":
            session.cookies.pop(name)
            
    URL = "https://www.easistent.com/urniki/izpis/" + school
    response = session.get(URL)
    
    (durations, lessons) = Parser.lessons(response.content)

    lessons_copy = []

    for day in lessons:
        lessons_copy.append([])

        for slot in day:
            lessons_copy[-1].append([(subject, teach) for (subject, teach) in slot if teach == teacher])
            
    timetable = Calendar.make((durations, lessons_copy), monday)
    
    return timetable
