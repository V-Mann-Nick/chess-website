from app import db
from chess.pgn import read_game
from io import StringIO
from datetime import datetime


# takes a ches.pgn.game-object and a list of app.model.Opening-objects
# returns the best match or None (app.model.Opening-object)
def best_matching_opening(game, openings):
    longest = (0, None)  # (move_count, Opening-object)
    for opening in openings:
        num_moves = len(opening.moves.split(' '))
        if num_moves > longest[0]:
            opening_pgn = read_game(StringIO(opening.moves))  # make chess.pgn.game-object
            for i, move in enumerate(game.mainline()):
                if i + 1 == num_moves:  # stop when at same move number
                    if opening_pgn.end().board().fen() == move.board().fen():  # compare position
                        longest = (num_moves, opening)
    return longest[1]


def new_game(pgn_string, is_from_user=True):
    game = read_game(StringIO(pgn_string))
    eco_matches = Opening.query.filter_by(eco_code=game.headers.get('ECO'))
    if eco_matches.count() > 1:  # if ECO is ambigious it will explore the moves for a match
        best_match = best_matching_opening(game, eco_matches)
        opening_id = best_match.id if best_match else None
    elif eco_matches.count() == 1:
        opening_id = eco_matches.first().id
    else:  # if pgn has no ECO
        best_match = best_matching_opening(game, Opening.query.all())
        opening_id = best_match.id if best_match else None
    return Game(pgn=pgn_string,
                white_player=game.headers.get('White'),
                black_player=game.headers.get('Black'),
                result=game.headers.get('Result'),
                is_from_user=is_from_user,
                date=game.headers.get('Date').replace('-', '/').replace('.', '/'),
                opening_id=opening_id)


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pgn = db.Column(db.String(), index=True, unique=True)
    white_player = db.Column(db.String(64), index=True, unique=False)
    black_player = db.Column(db.String(64), index=True, unique=False)
    date = db.Column(db.String(16), index=True, unique=False)
    result = db.Column(db.String(16), index=True, unique=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    is_from_user = db.Column(db.Boolean)
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
