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

@app.route("/predict", methods=['POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def predict():
    user=request.values.get("twitter_handle")

    print("Requested user", user)
    '''
    output = get_tweet_data_from_user(user, only_get_info_from_db = True)
    # change to second parameter to False to get updated results
    print(output)

    if output == -1:
        return abort(400, 'User Not Found')
    '''
    output = {'token_labels': ['photo', 'que', 'people', 'time', 'thank', 'day', 'pas', 'twitter', 'gold', 'god', 'today', 'coins', 'food', 'trump', 'way'], 'token_counts': [37, 26, 25, 21, 18, 17, 16, 16, 15, 15, 14, 14, 13, 12, 12], 'hash_labels': ['#ipadgames', '#gameinsight', '#ipad', '#starleaf', '#bestfiends', '#newprofilepic', '#yanggang', '#trump2020', '#narendramodi', '#voicesavekorin', '#np', '#yangforyourbuck', '#elfyourself', '#xbox360', '#amitabhbachchan'], 'hash_counts': [29, 29, 27, 7, 7, 5, 3, 3, 3, 3, 2, 2, 2, 2, 2]}

    return output

if __name__ == "__main__":
  app.run(debug=True)
