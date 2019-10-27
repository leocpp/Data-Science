import sqlite3
import pickle
import predict
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sportsreference.nba.roster import Roster, Player
from sportsreference.nba.player import AbstractPlayer
from sportsreference.nba.teams import Teams


def create_app()
    APP = Flask(__name__)
    APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///current.sqlite3'
    APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    DB = SQLAlchemy(APP)


    @APP.route('/')
    def root():
        return "Hi"

    @APP.route('/predict', methods=['GET', 'POST'])
    model = pickle.load(open('model.pkl', 'rb'))
    compare = compare.load(open('compare.pkl', 'rb'))
    # conn = sqlite3.connect('nbadb.sqlite3')
    # cursor = conn.cursor()
    # nbads = pd.read_sql("select * from nba_players;", conn)
    # renamedict = {'name': 'Player', 'FG_Pct': 'FG_Percentage', 'TP_Pct': 'TP_Percentage', 'FT_Pct': 'FT_Percentage', 
    #               'Min_per_game': 'Minutes.per.Game', 'Pts_per_game': 'Points.per.Game', 'TRB_per_game': 'TRB.per.game',
    #               'Asts_per_game': 'Assits.per.Game'}
    # nbads = nbads.rename(columns=renamedict)
    # reorderlist = ['Team', 'FG_Percentage', 'TP_Percentage', 'FT_Percentage', 'Minutes.per.Game', 'Points.per.Game' ,'TRB.per.game',
    #                'Assits.per.Game', 'WS_per_game', 'BPM', 'VORP', 'Player']
    # nbads = nbads[reorderlist]
    
    def predict():
        askname = request.get_json[force=True, silent=True]
        chkdata = nbads[nbads['Player'] == askname]
        xtestencoded = encoder.transform(chkdata.drop(columns=['Player', 'VORP']))
        longevity = model.predict(xtestencoded)
        output1 = longevity[0]
        distances, index = compare.kneighbors(xtestencoded)
        comparable = comppast.iloc[index[0]]
        output2 = comparable[['Player', 'Yrs']]
        return jsonify (output1, output2)

    return APP
