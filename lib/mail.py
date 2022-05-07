import random, string, threading, time, json, httpx
from lib.console import Console
from imap_tools import MailBox

__config__ = json.load(open('./script/config.json', 'r+'))

class Gmail:
    def __init__(self, mail: str, password: str) -> None:
        self.mail = mail
        self.password = password
        self.blacklist = []
        self.mail_list = {}

        threading.Thread(target= self.parser_thread).start()
    
    def parser_thread(self) -> None:
        while True:
            try:
                with MailBox('imap.gmail.com', '993').login(self.mail, self.password, 'INBOX') as mailbox:
                    for msg in mailbox.fetch():
                        try:
                            body = msg.html
                            to = str(msg.to[0]).lower()

                            if to not in self.blacklist:
                                verif = body.split('https://www.guilded.gg/api/email/verify?token=')[1].split('"')[0]
                                self.mail_list[to] = verif
                                self.blacklist.append(to)

                                if __config__['delete_verification_email']:
                                    mailbox.delete(msg.uid)
                                    Console.debug(f'[>] Delete email: {msg.uid}')
                        except Exception as e:
                            Console.debug(f'[-] Mail error: {e}')
                time.sleep(1)
            except Exception as e:
                Console.debug(f'[-] Error when connecting to imap server: {e}')
    
    @staticmethod
    def get_mail(mail_base: str) -> str:        
        return mail_base + "+" + "".join([random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(10)]) + "@gmail.com"

class MailGwApi:
    def __init__(self, proxy: str= None, timeout: int=15) -> None:
        self.session = httpx.Client(headers={'content-type': 'application/json'}, timeout=timeout, proxies=proxy)
        self.base_url = 'https://api.mail.tm'
    
    def get_domains(self) -> list:
        domains: list = []
        
        for item in self.session.get(f'{self.base_url}/domains').json()['hydra:member']:
            domains.append(item['domain'])

        return domains

    def get_mail(self, password: str= None, domain: str = None) -> str:
        mail: str =  f'{"".join(random.choice(string.ascii_lowercase) for _ in range(15))}@{domain if domain is not None else self.get_domains()[0]}'
        response: httpx.Response = self.session.post(f'{self.base_url}/accounts', json={'address': mail, 'password': mail if password is None else password})

        try:
            if response.status_code == 201:
                token = self.session.post(f'{self.base_url}/token', json={'address': mail, 'password': mail if password is None else password}).json()['token']
                self.session.headers['authorization'] = f'Bearer {token}'
                return mail
        except Exception as e:
            return f'Email creation error. ({e})'
    
    def fetch_inbox(self):
        response = self.session.get(f'{self.base_url}/messages').json()['hydra:member']
        return response
    
    def get_message(self, message_id: str):
        response = self.session.get(f'{self.base_url}/messages/{message_id}').json()
        return response
    
    def get_message_content(self, message_id: str):
        response = self.get_message(message_id)['text']
        return response