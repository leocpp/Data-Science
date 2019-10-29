import pickle
import pandas as pd
from predict import feats, comparrison
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sportsreference.nba.roster import Roster, Player
from sportsreference.nba.player import AbstractPlayer
from sportsreference.nba.teams import Teams


APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///current.sqlite3'
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
DB = SQLAlchemy(APP)


@APP.route('/')
def hi_there():
    return "Hello, how's it going?"

@APP.route('/predict', methods=['GET', 'POST'])
def prediction():
    xgbpipe = pickle.load(open('xgbpipe.pkl', 'rb'))
    askname = request.get_json(force=True, silent=True)
    print(askname)
    nbads = pd.read_csv('nbads.csv')
    chkdata = nbads[nbads['Player'] == askname['Player']]
    print(chkdata)
    longevity = xgbpipe.predict(chkdata[feats])
    output1 = {'Longevity' : str(longevity[0])}
    comp = comparrison(chkdata)
    result = comp.to_dict('index')
    output2 = result
    return jsonify(output1, output2)


if __name__ == '__main__':
    APP.run()