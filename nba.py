import pickle
import pandas as pd
from predict import encoder, coder, nbads
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sportsreference.nba.roster import Roster, Player
from sportsreference.nba.player import AbstractPlayer
from sportsreference.nba.teams import Teams


APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///current.sqlite3'
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
DB = SQLAlchemy(APP)


@APP.route('/', methods=['GET', 'POST'])
def prediction():
    model = pickle.load(open('model.pkl', 'rb'))
    compare = pickle.load(open('compare.pkl', 'rb'))
    askname = request.get_json(force=True, silent=True)
    chkdata = nbads[nbads['Player'] == askname]
    xtestencoded = encoder.transform(chkdata.drop(columns=['Player', 'VORP']))
    longevity = model.predict(xtestencoded)
    output1 = {longevity[0]}
    distances, index = compare.kneighbors(xtestencoded)
    comparable = comppast.iloc[index[0]]
    output2 = {comparable[['Player', 'Yrs']]}
    return jsonify(output1, output2)


if __name__ == '__main__':
    APP.run(port = 5000, debug=True)