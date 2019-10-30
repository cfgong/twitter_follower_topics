# ./python_code/api.py
import os
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
import numpy as np
from notebook_to_script import main

app = Flask(__name__)
CORS(app)
api = Api(app)

@app.route("/")
def hello():
    return "ok"

@app.route("/predict", methods=['POST'])
def action ():
    user=request.values.get("twitter_handle")

    print("RESULT in api", user)
    # users.insert_one({ "user":user})
    return main()

if __name__ == "__main__":
  app.run(debug=True)
