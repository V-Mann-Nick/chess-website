from app import app, db
from app.models import Game, new_game, Opening


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Game': Game, 'new_game': new_game, 'Opening': Opening}


if __name__ == '__main__':
    app.run(host='0.0.0.0',
            debug=True)
