from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()


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