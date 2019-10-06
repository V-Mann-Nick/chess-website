from app import db
from chess.pgn import read_game
from io import StringIO
from datetime import date
from dateutil.parser import parse


class PgnFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pgn = db.Column(db.String(), index=True, unique=True)
    white_player = db.Column(db.String(64), index=True, unique=False)
    black_player = db.Column(db.String(64), index=True, unique=False)
    date = db.Column(db.Date(), index=True, unique=False)

    def __repr__(self):
        return f'<{self.white_player} - {self.black_player} ({self.date})>'


def new_PgnFile(pgn_string):
    game = read_game(StringIO(pgn_string))
    white_player = game.headers.get('White')
    black_player = game.headers.get('Black')
    game_date = parse(game.headers.get('Date')).date() if game.headers.get('Date') else None
    return PgnFile(pgn=pgn_string,
                   white_player=white_player,
                   black_player=black_player,
                   date=game_date)
