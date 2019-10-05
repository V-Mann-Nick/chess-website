import requests
from chess.pgn import read_game


IMAGE_MISSING_URL = '/static/images/players/no-picture/question-mark.jpg'


def get_wikipicture_url(name):
    url = 'http://en.wikipedia.org/w/api.php?'
    params = {'action': 'query',
              'format': 'json',
              'list': 'search',
              'srsearch': name,
              'srlimit': 1}
    try:
        response = requests.get(url=url, params=params, timeout=5)
        if response.status_code >= 400:
            print(f'Getting image for player {name} resulted in {response.status_code}')
            return IMAGE_MISSING_URL
    except:
        print(f"Connection to {url} failed.")
        return IMAGE_MISSING_URL
    try:
        pagetitle = response.json()['query']['search'][0]['title']
    except KeyError as e:
        print(f'Getting image for player {name} resulted in a key error: {e} is not a valid key for this request: {response.url}')
        return IMAGE_MISSING_URL
    params = {'action': 'query',
              'format': 'json',
              'prop': 'pageimages',
              'piprop': 'original',
              'titles': pagetitle}
    try:
        response = requests.get(url=url, params=params, timeout=5)
        if response.status_code >= 400:
            print(f'Getting image for player {name} resulted in {response.status_code}')
            return IMAGE_MISSING_URL
    except:
        print(f"Connection to {url} failed.")
        return IMAGE_MISSING_URL
    name_parts = name.split(' ')
    try:
        pages = response.json()['query']['pages']
    except KeyError as e:
        print(f'Getting image for player {name} resulted in a key error: {e} is not a valid key for this request: {response.url}')
        return IMAGE_MISSING_URL
    for key in pages.keys():
        page = pages[key]
        try:
            image_url = page['original']['source']
        except KeyError as e:
            print(f'Getting image for player {name} resulted in a key error: {e} is not a valid key for this request: {response.url}')
            return IMAGE_MISSING_URL
        if any([name_part in image_url for name_part in name_parts]):
            return image_url
    return IMAGE_MISSING_URL


def get_player_picture_urls(pgn_path):
    with open(pgn_path) as pgn:
        game = read_game(pgn)
    return {'White': get_wikipicture_url(game.headers['White']),
            'Black': get_wikipicture_url(game.headers['Black'])}
