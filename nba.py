from flask import Flask, request, jasonify
from flask_sqlalchemy import SQLAlchemy
from sportsreference.nba.roster import Roster, Player
from sportsreference.nba.player import AbstractPlayer
from sportsreference.nba.teams import Teams

APP = FLASK(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///current.sqlite3'
DB = SQLAlchemy(APP)


class NBATeam(DB.Model):
    abbr = DB.Column(DB.String(4), unique=True, nullable=False)
    name = DB.Column(DB.String(30), unique=True, nullable=False)


class NBAPlayer(DB.Model):
    ref_id = DB.Column(DB.String(10), unique=True, nullable=False)
    name = DB.Column(DB.String(30), nullable=False)
    Team = DB.Column(DB.String(4), DB.ForeignKey('NBATeam.abbr'), nullable=False)
    FG_Pct = DB.Column(DB.Float, nullable=False)
    TP_Pct = DB.Column(DB.Float, nullable=False)
    FT_Pct = DB.Column(DB.Float, nullable=False)
    Min_per_game = DB.Column(DB.Float, nullable=False)
    Pts_per_game = DB.Column(DB.Float, nullable=False)
    TRB_per_game = DB.Column(DB.Float, nullable=False)
    Asts_per_game = DB.Column(DB.Float, nullable=False)
    WS_per_game = DB.Column(DB.Float, nullable=False)
    BPM = DB.Column(DB.Float, nullable=False)
    VORP = DB.Column(DB.Float, nullable=False)
    team = DB.relationship('NBATeam', backref='player')


######################
teams = Teams()
player = Player()
teamabbs = []
for team in teams:
    teamabbs.append(team.abbreviation)

for abb in teamabbs:
    squad = Roster(abb, slim)
    squaddict = squad.players
    squadIDs = list(squaddict.keys())

######################


def add_teams(teams):
    for team in teams:
        nbateam = NBATeam(abbr=team.abbreviation,
                          name=team.name)
        DB.session.add(nbateam)


def add_players(squadIDs):
    for id in squadIDs:
        nbaplayer = NBAPlayer(ref_id=player.player_id,
                              name=player.name,
                              Team=player.team_abbreviation,
                              FG_Pct=player.field_goal_percentage,
                              TP_Pct=player.three_point_percentage,
                              FT_Pct=player.free_throw_percentage,
                              Min_per_game=(player.minutes_played/player.games_played),
                              Pts_per_game=(player.points/player.games_played),
                              TRB_per_game=(player.total_rebounds/player.games_played),
                              Asts_per_game=(player.assists/player.games_played),
                              WS_per_game=player.win_shares_per_48_minutes,
                              BPM=player.box_plus_minus,
                              VORP=player.value_over_replacement_player
                              )
        DB.session.add(nbaplayer)


def predict_longevity()
