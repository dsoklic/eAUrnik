#
#  API.py
#  eAUrnik
#

import Timetable
from flask import Flask, request, make_response
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

@app.errorhandler(404)
def page_not_found(e):
    response = make_response("This request could not be processed. Check the provided information and try again.", 400)
    response.headers["content-type"] = "application/json"
    return response

@app.route("/urniki/<string:school>/razredi/<int:class_>")
def get(school, class_):
        response = make_response(timetable, 200)
        response.headers["content-type"] = "text/calendar"
        return response

if __name__ == "__main__":
    app.run(host = "::")
