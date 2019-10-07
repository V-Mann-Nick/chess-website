from app import app, db
from app.models import PgnFile, new_PgnFile


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'PgnFile': PgnFile, 'new_PgnFile': new_PgnFile}


if __name__ == '__main__':
    app.run(host='0.0.0.0',
            debug=True)
