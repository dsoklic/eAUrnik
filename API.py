#
#  API.py
#  eAUrnik
#

import Timetable
from flask import Flask, request, make_response
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)

CORS(app)

@app.errorhandler(404)
def page_not_found(e):
    response = make_response("This request could not be processed. Check the provided information and try again.", 400)
    response.headers["content-type"] = "application/json"
    return response

@app.route("/urniki/<string:school>/razredi/<int:class_>")
def get(school, class_):
    timetable = Timetable.get_class(school, class_)
    response = make_response(timetable, 200)
    response.headers["content-type"] = "text/calendar"
    return response

@app.route("/urniki/<string:school>/ucitelj/<int:teacher>")
def get_teacher(school, teacher):
        timetable = Timetable.get_teacher(school, teacher)
        response = make_response(timetable, 200)
        response.headers["content-type"] = "text/calendar"
        return response

if __name__ == "__main__":
    app.run(host = "::")
