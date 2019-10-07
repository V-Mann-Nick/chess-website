from app import db
from chess.pgn import read_game
from io import StringIO
from dateutil.parser import parse


def new_game(pgn_string):
    game = read_game(StringIO(pgn_string))
    white_player = game.headers.get('White')
    black_player = game.headers.get('Black')
    game_date = parse(game.headers.get('Date')).date() if game.headers.get('Date') else None
    opening = Opening.query.filter_by(eco_code=game.headers.get('ECO')).first()
    return Game(pgn=pgn_string,
                white_player=white_player,
                black_player=black_player,
                date=game_date,
                opening_id=opening.id)


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pgn = db.Column(db.String(), index=True, unique=True)
    white_player = db.Column(db.String(64), index=True, unique=False)
    black_player = db.Column(db.String(64), index=True, unique=False)
    date = db.Column(db.Date(), index=True, unique=False)
    opening_id = db.Column(db.Integer, db.ForeignKey('opening.id'))

    def __repr__(self):
        return f'<{self.white_player} - {self.black_player} ({self.date})>'


class Opening(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    eco_code = db.Column(db.String(4), index=True, unique=False)
    name = db.Column(db.String(128), index=True, unique=False)
    moves = db.Column(db.String(256), index=True, unique=False)
    games = db.relationship('Game', backref='opening', lazy='dynamic')

    def __repr__(self):
        return f'<{self.eco_code} - {self.name}>'
