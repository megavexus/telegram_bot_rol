import os
from configparser import ConfigParser

def get_token():
    dir_path = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(dir_path, "..", "..", "token.ini")
    parser = ConfigParser()
    parser.read(config_path)
    token = parser.get('telegram', 'TOKEN')
    return token
