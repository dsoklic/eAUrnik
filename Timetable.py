#
#  Timetable.py
#  eAUrnik
#

import Parser
import Calendar
import requests
from datetime import date, timedelta

def get_monday(today):
    """Returns the upcoming Monday. If today is Saturday or Sunday, return next Monday."""
    monday = today - timedelta(days=today.weekday())  # Get current week's Monday
    
    # If it's the weekend, take next week.
    if today.weekday() >= 5:
        monday += timedelta(weeks=1)

    return monday

def get_schoolyear_start(schoolyear):
    """Returns the start of the school year, adjusting if it starts on a weekend."""
    schoolyear_start = date(schoolyear, 9, 1)
    # If it falls on a weekend, move to the next Monday
    while schoolyear_start.weekday() >= 5:
        schoolyear_start += timedelta(days=1)
    return schoolyear_start

def calculate_week(today):
    """Calculates the week number in the school year."""
    monday = get_monday(today)
    
    # Determine the school year based on the current date
    schoolyear = today.year - 1 if today.month < 8 else today.year # If the month is before September, take previous year.
    schoolyear_start = get_schoolyear_start(schoolyear)
    
    # Calculate the number of Mondays between the school year start and current Monday
    delta_days = (monday - schoolyear_start).days
    return delta_days // 7 + 1


def get_session():
    session = requests.Session()
    session.get("https://www.easistent.com")
    
    # Remove all cookies except "vxcaccess", as they cause further requests to be rejected.
    for cookie in session.cookies:
        name = cookie.name
        if name != "vxcaccess":
            session.cookies.pop(name)

    return session

def get_lessons(session, schoolId, classId=0, professorId=0, classroomId=0, week=0, studentId=0):
    # The IDs used in the API call are in the following order:
    #   1. School
    #   2. Class
    #   3. Professor/teacher
    #   4. Classroom
    #   5. Not sure
    #   6. Week
    #   7. Student
    #
    # Setting any of these IDs (except the school) to 0 returns all.
    URL = f"https://www.easistent.com/urniki/izpis/{schoolId}/{classId}/{professorId}/{classroomId}/0/{week}/{studentId}"
    response = session.get(URL)
    
    return Parser.lessons(response.content)

def get_student(school, class_, student):
    today = date.today()
    monday = get_monday(today)
    week = calculate_week(today)
            
    session = get_session()
            
    lessons = get_lessons(session, schoolId=school, classId=class_, week=week, studentId=student)
    timetable = Calendar.make(lessons, monday)
    
    return timetable

def get_class(school, class_):
    today = date.today()
    monday = get_monday(today)
    week = calculate_week(today)
            
    session = get_session()
            
    lessons = get_lessons(session, schoolId=school, classId=class_, week=week)
    timetable = Calendar.make(lessons, monday)
    
    return timetable

def get_teacher(school, teacher, weeks = 1):
    today = date.today()
    monday = get_monday(today)
    current_week = calculate_week(today)
            
    session = get_session()
    
    lessons = get_lessons(session, schoolId=school, professorId=teacher, week=current_week)
            
    timetable = Calendar.make(lessons, monday)
    
    return timetable
