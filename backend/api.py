# ./python_code/api.py
import os
from flask import Flask, request, abort
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS, cross_origin
import numpy as np
from get_tweet_data_webscrape import main as get_tweet_data_from_user


app = Flask(__name__)
cors = CORS(app, resources={r"/predict": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'



@app.route("/predict", methods=['POST', 'OPTIONS'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def predict():
    user=request.values.get("twitter_handle")

    print("Requested user", user)
    output = get_tweet_data_from_user(user, only_get_info_from_db = True)
    # change to second parameter to False to get updated results
    print(output)

    if output == -1:
        return abort(400, 'User Not Found')

    return output

if __name__ == "__main__":
  app.run(debug=True)
