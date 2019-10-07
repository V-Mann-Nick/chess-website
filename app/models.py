from app import db
from chess.pgn import read_game
from io import StringIO
from dateutil.parser import parse


# Takes chess.pgn.Game object and a string from the opening table
def opening_matches(game, opening):
    num_moves = len(opening.split(' '))
    opening = read_game(StringIO(opening))
    for i, move in enumerate(game.mainline()):
        if i + 1 == num_moves:
            return opening.end().board().fen() == move.board().fen()


def new_game(pgn_string):
    game = read_game(StringIO(pgn_string))
    white_player = game.headers.get('White')
    black_player = game.headers.get('Black')
    game_date = parse(game.headers.get('Date')).date() if game.headers.get('Date') else None
    eco_matches = Opening.query.filter_by(eco_code=game.headers.get('ECO'))
    # if ECO is ambigious it will explore the moves for a match
    if eco_matches.count() > 1:
        for eco_match in eco_matches:
            if opening_matches(game, eco_match.moves):
                opening_id = eco_match.id
                break
    elif eco_matches.count() == 1:
        opening_id = eco_matches.first().id
    else:
        opening_id = None
    return Game(pgn=pgn_string,
                white_player=white_player,
                black_player=black_player,
                date=game_date,
                opening_id=opening_id)


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pgn = db.Column(db.String(), index=True, unique=True)
    white_player = db.Column(db.String(64), index=True, unique=False)
    black_player = db.Column(db.String(64), index=True, unique=False)
    date = db.Column(db.Date(), index=True, unique=False)
    result = db.Column(db.String(16), index=True, unique=False)
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
