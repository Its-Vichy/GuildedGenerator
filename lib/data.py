import json, itertools 
from lib import mail

__config__ = json.load(open('./config.json', 'r+'))

class Data:
    def __init__(self) -> None:
        self.email = mail.Gmail(__config__['mail'], __config__['password'])
        self.usernames = itertools.cycle(open('./data/usernames.txt', 'r+', encoding= 'utf-8', errors= 'ignore').read().splitlines())