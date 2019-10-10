from app import app, db
from app.pgn_pretty_print import GamePrinter
from app.player_pictures import get_wikipicture_url
from app.models import Game, new_game
from flask import render_template, url_for, redirect
from app.forms import Options, Upload
from base64 import b64encode
import random

# TODO
# - implement space before and after?
# - clk in pgns
# - timeout for pictures
# - revise background-images
# - think about error handling
# - more comments

# notworthy navigation games will be generated
# [(category, [id1, id2, id3, ...]), ...]
GAME_NAV = [('Bobby Fischer', [1, 2, 3, 4, 5, 6]),
            ('Alexander Alekhine', [8, 9, 10, 11, 12]),
            ('Garry Kasparov', [13, 14, 15, 16])]  # EDIT!
# [(category1, [(game1_label, game1_id), ...]), (cateogry2, [(game1_label, game1_id), ...])]
GAME_NAV = [(category[0], [(f"{Game.query.get(i).white_player.split(' ')[-1]}-"  # NOEDIT!
                          + f"{Game.query.get(i).black_player.split(' ')[-1]} "
                          + f"({Game.query.get(i).date.split('/')[0]})", i) for i in category[1]]) for category in GAME_NAV]


@app.route('/')
def index():
    game1, game2 = random.sample(list(Game.query.filter_by(is_from_user=False)), k=2)
    game1 = {'White': game1.white_player,
             'Black': game1.black_player,
             'Date': game1.date,
             'Result': game1.result,
             'WPic': get_wikipicture_url(game1.white_player),
             'BPic': get_wikipicture_url(game1.black_player),
             'Opening': game1.opening.name,
             'id': game1.id}
    game2 = {'White': game2.white_player,
             'Black': game2.black_player,
             'Date': game2.date,
             'Result': game2.result,
             'WPic': get_wikipicture_url(game2.white_player),
             'BPic': get_wikipicture_url(game2.black_player),
             'Opening': game2.opening.name,
             'id': game2.id}
    return render_template('index.html',
                           game_nav=GAME_NAV,
                           game1=game1,
                           game2=game2)


@app.route('/game_viewer_id=<id>')
def game_viewer(id):
    # interacts with wikipedia api
    game = Game.query.get(int(id))
    player_image_urls = {'White': get_wikipicture_url(game.white_player),
                         'Black': get_wikipicture_url(game.black_player)}
    pgn_b64 = b64encode(game.pgn.encode('utf-8')).decode('utf-8')
    return render_template('game_viewer.html',
                           pgn_text=game.pgn,
                           game_nav=GAME_NAV,
                           white_player=game.white_player,
                           black_player=game.black_player,
                           game_date=game.date,
                           opening=game.opening.name,
                           result=game.result,
                           player_image_urls=player_image_urls,
                           pgn_b64=pgn_b64,
                           pgn_filename='{}_{}.pgn'.format(game.white_player.split(' ')[-1],
                                                           game.black_player.split(' ')[-1]),
                           game_id=id)


@app.route('/puzzles')
def puzzles():
    return render_template('puzzles.html', game_nav=GAME_NAV)


# tool_target is either 'pdf_printer' or 'game_viewer'
@app.route('/tools/<tool_target>_upload', methods=['GET', 'POST'])
def uploader(tool_target):
    form = Upload()
    if form.validate_on_submit():
        if form.upload.data and not form.pgn_text.data:  # file uploaded
            f = form.upload.data
            pgn_text = f.read().decode('utf-8')
        elif form.pgn_text.data and not form.upload.data:  # pgn text provided
            pgn_text = form.pgn_text.data
        # nothing or both provided
        else:
            return render_template('pgn_upload.html',
                                   error=True,
                                   is_for_ppTool=tool_target == 'pdf_printer',
                                   game_nav=GAME_NAV,
                                   form=form)
        query = Game.query.filter_by(pgn=pgn_text)
        if query.count():  # if pgn is already in db
            id = query.first().id
        else:  # else add to db
            pgn = new_game(pgn_text)
            db.session.add(pgn)
            db.session.commit()
            id = pgn.id
        return redirect(url_for('chess_print_ui' if tool_target == 'pdf_printer' else 'game_viewer', id=id))
    return render_template('pgn_upload.html',
                           error=False,
                           is_for_ppTool=tool_target == 'pdf_printer',
                           game_nav=GAME_NAV,
                           form=form)


@app.route('/tools/pdf_printer_id=<id>', methods=['GET', 'POST'])
def chess_print_ui(id):
    form = Options()
    game = Game.query.get(int(id))
    if form.validate_on_submit():
        printer = GamePrinter(game.pgn,
                              halfmoves_to_be_printed=form.halfmoves.data,
                              page_format=form.page_format.data,
                              font_name=form.font_name.data)
        if form.color_custom_light.data and form.color_custom_dark.data:
            printer.light_tile_color = form.color_custom_light.data
            printer.dark_tile_color = form.color_custom_dark.data
        elif form.color.data != 'None':
            light_tile_color, dark_tile_color = form.color.data.split('/')
            printer.light_tile_color = light_tile_color
            printer.dark_tile_color = dark_tile_color
        if form.paragraph_arrangement.data != 'None':
            printer.elements_arrange = form.paragraph_arrangement.data
        if form.page_margin.data:
            printer.page_margin = form.page_margin.data
        if form.font_size.data:
            printer.font_size = form.font_size.data
        if form.column_gap.data:
            printer.col_gap = form.column_gap.data
        pdf = printer.build_and_return_document().getvalue()
        form.halfmoves.choices = [(i, move.san()) for i, move in enumerate(printer.game.mainline())]
    else:
        printer = GamePrinter(game.pgn)
        pdf = printer.build_and_return_document().getvalue()
        form.halfmoves.choices = [(i, move.san()) for i, move in enumerate(printer.game.mainline())]
    return render_template('chess_print.html',
                           form=form,
                           pgn_parse_errors=printer.game.errors,
                           game_nav=GAME_NAV,
                           game_name=f'{game.white_player} - {game.black_player}',
                           pdf_filename=printer.filename,
                           pdf_output=b64encode(pdf).decode('utf-8') if pdf else '')


@app.route('/impressum')
def impressum():
    return render_template('impressum.html',
                           game_nav=GAME_NAV)


@app.route('/privacy_statement')
def privacy_statement():
    return render_template('privacy_statement.html',
                           game_nav=GAME_NAV)
