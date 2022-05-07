import json, itertools, threading, time, os, httpx
from lib import mail

__config__ = json.load(open('./script/config.json', 'r+'))

class Data:
    def __init__(self) -> None:
        self.generated = 0
        self.verified  = 0
        self.banned    = 0

        self.email = mail.Gmail(__config__['mail'], __config__['password']) if __config__['use_tempmail'] == False else None
        self.usernames = itertools.cycle(self.load_usernames())
        self.status = itertools.cycle(open('./script/data/status.txt', 'r+', encoding= 'utf-8', errors= 'ignore').read().splitlines())
        self.bio = itertools.cycle(open('./script/data/bio.txt', 'r+', encoding= 'utf-8', errors= 'ignore').read().splitlines())
        self.pfp = itertools.cycle(open('./script/data/pfp.txt', 'r+', encoding= 'utf-8', errors= 'ignore').read().splitlines())

        threading.Thread(target= self.update_title_thread).start()
    
    def load_usernames(self) -> list:
        users = []

        with open('./script/data/usernames.txt', 'r+', errors= 'ignore') as f:
            try:
                for line in f:
                    users.append(line.split('\n')[0])
            except:
                pass
        
        return list(set(users))       

    def get_bio(self, proxy: str=None) -> str:
        return httpx.get('https://free-quotes-api.herokuapp.com', proxies=proxy, timeout=30).json()['quote']

    def update_title_thread(self) -> None:
        if os.name == 'nt':
            while True:
                os.system(f'title GuildeadGen - github.com/its-vichy ^| Generated: {self.generated} - Verified: {self.verified} - Banned: {self.banned} - Threads: {threading.active_count()}')
                time.sleep(1)