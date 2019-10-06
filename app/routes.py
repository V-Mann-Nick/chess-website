from app import app
from app.pgn_pretty_print import GamePrinter
from app.player_pictures import get_player_picture_urls
from flask import render_template, url_for, session, redirect
from werkzeug.utils import secure_filename
from app.forms import Options, Upload
import os
from base64 import b64encode

# TODO
# - implement space before and after?
# - clk in pgns
# - upload directly
# - change page-title
# - timeout for pictures
# - revise background-images
# - think about error handling
# - more comments

SAVED_PGNS_PATH = 'app/static/pgns/'
PGNS_PATH = 'app/static/game_viewer_pgns/'


# notworthy games will be automatically generated depending on the contents of PGNS_PATH
# Searches PGNS_PATH and creates following structure:
# [(folder1, [(file1_name, file1_label), ...]), (folder2, [(file1_name, file1_label), ...])]
def generate_game_nav():
    nav_dirs = list()
    for folder in os.listdir(PGNS_PATH):
        folder_elems = list()
        for game in os.listdir(os.path.join(PGNS_PATH, folder)):
            game = game[:game.find('.pgn')]
            parts = game.split('_')
            folder_elems.append((game, '-'.join([part.capitalize() for part in parts])))
        nav_dirs.append((folder, folder_elems))
    return nav_dirs


# Generates a unique filename for the uploaded pgns
def unique_filename():
    global file_it
    if 'file_it' not in globals():
        file_it = 0
    filename = f'{file_it}.pgn'
    while os.path.exists(os.path.join(SAVED_PGNS_PATH, filename)):
        file_it += 1
        filename = f'{file_it}.pgn'
    return filename


@app.route('/')
def index():
    return render_template('index.html', game_nav=generate_game_nav())


@app.route('/games/<folder>/<game_name>')
def game_viewer(folder, game_name):
    # interacts with wikipedia api
    player_image_urls = get_player_picture_urls(os.path.join(PGNS_PATH, f'{folder}/{game_name}.pgn'))
    return render_template('game_viewer.html',
                           game_path=url_for('static', filename=f'game_viewer_pgns/{folder}/{game_name}.pgn'),
                           game_nav=generate_game_nav(),
                           player_image_urls=player_image_urls)


@app.route('/puzzles')
def puzzles():
    return render_template('puzzles.html', game_nav=generate_game_nav())


# tool_target is either 'pdf_printer' or 'custom_game_viewer'
@app.route('/tools/<tool_target>_upload&reset=<reset>', methods=['GET', 'POST'])
def uploader(tool_target, reset):
    if tool_target == 'pdf_printer':
        filename_key = 'pp_filename'
        original_filename_key = 'pp_original_filename'
    else:
        filename_key = 'cgv_filename'
        original_filename_key = 'cgv_original_filename'
    # If tool should not be reset and a file_path is in cookie send to tool
    if reset == 'False' and session.get(filename_key):
        return redirect(url_for('chess_print_ui' if tool_target == 'pdf_printer' else 'custom_game_viewer'))
    # Reset cookies
    session.pop(filename_key, None)
    session.pop(original_filename_key, None)
    form = Upload()
    if form.validate_on_submit():
        # file uploaded
        if form.upload.data and not form.pgn_text.data:
            f = form.upload.data
            session[filename_key] = unique_filename()
            session[original_filename_key] = secure_filename(f.filename)
            f.save(os.path.join(SAVED_PGNS_PATH, session[filename_key]))
        # pgn text provided
        elif form.pgn_text.data and not form.upload.data:
            session[filename_key] = unique_filename()
            session[original_filename_key] = 'pgn text'
            with open(os.path.join(SAVED_PGNS_PATH, session[filename_key]), 'w') as pgn:
                pgn.write(form.pgn_text.data)
        # nothing or both provided
        else:
            return render_template('pgn_upload.html',
                                   error=True,
                                   is_for_ppTool=tool_target == 'pdf_printer',
                                   game_nav=generate_game_nav(),
                                   form=form)
        return redirect(url_for('chess_print_ui' if tool_target == 'pdf_printer' else 'custom_game_viewer'))
    return render_template('pgn_upload.html',
                           error=False,
                           is_for_ppTool=tool_target == 'pdf_printer',
                           game_nav=generate_game_nav(),
                           form=form)


@app.route('/tools/pdf_printer', methods=['GET', 'POST'])
def chess_print_ui():
    if not session.get('pp_filename'):
        return redirect(url_for('uploader', tool_target='pdf_printer', reset='True'))
    form = Options()
    if form.validate_on_submit():
        printer = GamePrinter(os.path.join(SAVED_PGNS_PATH, session['pp_filename']),
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
        if form.page_margin.data:
            printer.page_margin = form.page_margin.data
        if form.font_size.data:
            printer.font_size = form.font_size.data
        if form.column_gap.data:
            printer.col_gap = form.column_gap.data
        pdf = printer.build_and_return_document().getvalue()
        form.halfmoves.choices = [(i, move.san()) for i, move in enumerate(printer.game.mainline())]
    else:
        printer = GamePrinter(os.path.join(SAVED_PGNS_PATH, session['pp_filename']))
        pdf = printer.build_and_return_document().getvalue()
        form.halfmoves.choices = [(i, move.san()) for i, move in enumerate(printer.game.mainline())]
    return render_template('chess_print.html',
                           form=form,
                           pgn_parse_errors=printer.game.errors,
                           game_nav=generate_game_nav(),
                           original_filename=session['pp_original_filename'],
                           pdf_filename=printer.filename,
                           pdf_output=str(b64encode(pdf))[2:-1] if pdf else '')


@app.route('/tools/custom_pgn_viewer')
def custom_game_viewer():
    # interacts with wikipedia api
    player_image_urls = get_player_picture_urls(os.path.join(SAVED_PGNS_PATH, session['cgv_filename']))
    return render_template('game_viewer.html',
                           game_path=os.path.join(SAVED_PGNS_PATH[3:], session['cgv_filename']),  # for html-files '/' is '/app'
                           game_nav=generate_game_nav(),
                           player_image_urls=player_image_urls)


@app.route('/impressum')
def impressum():
    return render_template('impressum.html',
                           game_nav=generate_game_nav())

@app.route('/privacy_statement')
def privacy_statement():
    return render_template('privacy_statement.html',
                           game_nav=generate_game_nav())
