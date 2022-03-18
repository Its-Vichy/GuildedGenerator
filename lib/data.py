import json, itertools, threading, time, os
from lib import mail

__config__ = json.load(open('./config.json', 'r+'))

class Data:
    def __init__(self) -> None:
        self.generated = 0
        self.verified  = 0

        self.email = mail.Gmail(__config__['mail'], __config__['password'])
        self.usernames = itertools.cycle(open('./data/usernames.txt', 'r+', encoding= 'utf-8', errors= 'ignore').read().splitlines())

        threading.Thread(target= self.update_title_thread).start()

    def update_title_thread(self) -> None:
        if os.name == 'nt':
            while True:
                os.system(f'title GuildeadGen - github.com/its-vichy ^| Generated: {self.generated} - Verified: {self.verified}')
                time.sleep(1)