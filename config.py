import os
import json


basedir = os.path.abspath(os.path.dirname(__file__))


try:
    with open('/etc/config.json') as config_file:
        config = json.load(config_file)
except:
    config = {}

class Config(object):
    SECRET_KEY = config.get('SECRET_KEY') or 'secret-af'
    SQLALCHEMY_DATABASE_URI = config.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
