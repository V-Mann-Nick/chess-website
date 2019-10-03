import requests
from chess.pgn import read_game


def get_wikipicture_url(name):
    image_missing_url = '/static/images/players/no-picture/question-mark.jpg'
    url = 'http://en.wikipedia.org/w/api.php?'
    params = {'action': 'query',
              'format': 'json',
              'prop': 'pageimages',
              'piprop': 'original',
              'titles': name}
    try:
        response = requests.get(url=url, params=params, timeout=5)
        if response.status_code >= 400:
            print(f'Getting image for player {name} resulted in {response.status_code}')
            return image_missing_url
    except:
        print(f"Connection to {url} failed.")
        return image_missing_url
    name_parts = name.split(' ')
    try:
        pages = response.json()['query']['pages']
    except KeyError as e:
        print(f'Getting image for player {name} resulted in a key error: {e} is not a valid key for this request: {response.url}')
        return image_missing_url
    for key in pages.keys():
        page = pages[key]
        try:
            image_url = page['original']['source']
        except KeyError as e:
            print(f'Getting image for player {name} resulted in a key error: {e} is not a valid key for this request: {response.url}')
            return image_missing_url
        if any([name_part in image_url for name_part in name_parts]):
            return image_url
    return image_missing_url


def get_player_picture_urls(pgn_path):
    with open(pgn_path) as pgn:
        game = read_game(pgn)
    return {'White': get_wikipicture_url(game.headers['White']),
            'Black': get_wikipicture_url(game.headers['Black'])}
