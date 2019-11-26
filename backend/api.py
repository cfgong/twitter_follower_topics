# ./python_code/api.py
import os
from flask import Flask, request, abort
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
import numpy as np
#from notebook_to_script import main
from get_tweet_data import main as get_tweet_data_from_user

app = Flask(__name__)
CORS(app)
api = Api(app)

@app.route("/")
def hello():
    return "ok"

@app.route("/predict", methods=['POST'])
def action ():
    user=request.values.get("twitter_handle")

    print("Requested user", user)

    # output = main(user)
    output = get_tweet_data_from_user(user, True)
    # change to second parameter to False to get updated results
    print(output)

    if output == -1:
        return abort(400, 'User Not Found')

    return output

if __name__ == "__main__":
  app.run(debug=True)
