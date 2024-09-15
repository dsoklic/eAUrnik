#
#  API.py
#  eAUrnik
#

import Timetable
from flask import Flask, make_response
from flask_restful import Api
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)

CORS(app)

@app.errorhandler(404)
def page_not_found(e):
    response = make_response("This request could not be processed. Check the provided information and try again.", 400)
    response.headers["content-type"] = "application/json"
    return response

@app.route("/urniki/<string:school>/razredi/<int:class_>/dijak/<int:student>")
def get_student(school, class_, student):
    """Parse a student's calendar."""
    timetable = Timetable.get_student(school, class_, student)
    response = make_response(timetable, 200)
    response.headers["content-type"] = "text/calendar"
    return response

@app.route("/urniki/<string:school>/razredi/<int:class_>")
def get_class(school, class_):
    """Parse a class's calendar."""
    timetable = Timetable.get_class(school, class_)
    response = make_response(timetable, 200)
    response.headers["content-type"] = "text/calendar"
    return response

@app.route("/urniki/<string:school>/ucitelj/<int:teacher>")
@app.route("/urniki/<string:school>/ucitelj/<int:teacher>/tednov/<int:weeks>")
def get_teacher_weeks(school, teacher, weeks=1):
    """Parse a teacher's calender for multiple weeks ahead. If number of weeks isn't specified, defaults to 1."""
    timetable = Timetable.get_teacher(school, teacher, weeks)
    response = make_response(timetable, 200)
    response.headers["content-type"] = "text/calendar"
    return response

if __name__ == "__main__":
    app.run(host = "::")
