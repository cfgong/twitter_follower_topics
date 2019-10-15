# ./python_code/api.py
import os
from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
import numpy as np

app = Flask(__name__)
CORS(app)
api = Api(app)
# Require a parser to parse our POST request.
parser = reqparse.RequestParser()
parser.add_argument("twitter_handle")

class Predict(Resource):
  def post(self):
    args = parser.parse_args()
    _y = args["twitter_handle"] * 2
    return {"class": _y}

api.add_resource(Predict, "/predict")
if __name__ == "__main__":
  app.run(debug=True)
