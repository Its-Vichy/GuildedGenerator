import json, threading, httpx, random, string, time, binascii, os, json, itertools
from lib.guildead import Guilded
from lib.console import Console
from lib.data import Data

__config__ = json.load(open('./config.json', 'r+'))


class Creator(threading.Thread):
    def __init__(self, proxy: str, data: Data) -> None:
        self.api = Guilded(proxy)
        self.proxy = proxy
        self.data = data

        threading.Thread.__init__(self)

    def create_account(self, username: str, mail: str, password: str) -> None:
        data = {"extraInfo":{"platform": "electron", "referrerId": __config__['referer']}, "name": username, "email": mail,"password": password,"fullName": username}

        h = {
            'authority': 'www.guilded.gg',
            'method': 'POST',
            'path': '/api/users?type=email',
            'scheme': 'https',

            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'fr-FR,fr;q=0.9',
            'content-type': 'application/json',
            'guilded-client-id': 'e9a9790a-32b9-4217-997e-d0ea56ee5675',
            'guilded-device-id': str(binascii.b2a_hex(os.urandom(64)).decode('utf-8')),
            'guilded-device-type': 'desktop',
            'guilded-stag': str(binascii.b2a_hex(os.urandom(32)).decode('utf-8')),
            'origin': 'https://www.guilded.gg',
            'referer': 'https://www.guilded.gg/',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
            'dnt': '1',
            "Sec-Ch-Ua": '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
            "Sec-Ch-Ua-Mobile": '?0',
            "Sec-Ch-Ua-Platform": "macOS",
        }

        try:
            with httpx.Client(proxies= self.proxy, headers= h) as client:
                client.cookies = client.put('https://www.guilded.gg/api/data/event').cookies
                
                #client.headers['content-length'] = str(len(json.dumps(data)))
                r= client.post(f'{self.api.base_url}/users?type=email', json= data)
                Console.debug(f'[>] {r.json()}')

                success, cookies = self.api.login(mail, password)
                
                if success:
                    Console.printf(f'[+] {username} has been created.')

                    data_mail= {"email": mail}
                    client.headers['content-lenght'] = str(len(json.dumps(data_mail)))
                    client.post(f'{self.api.base_url}/email/verify', json= data_mail, cookies= cookies)

                    verif_token= None 
                    while verif_token == None:
                        time.sleep(1)
                        try:
                            verif_token = self.data.email.mail_list[mail.lower()]
                        except:
                            pass
                    self.data.email.mail_list.pop(mail.lower())

                    Console.printf(f'[*] Verification token found: {verif_token}')
                    client.get('https://www.guilded.gg/api/email/verify?token=' + verif_token, cookies= cookies).text

                    if self.api.check_mail_verified()['email'] == True:
                        Console.printf(f'[>] Email verified: {username}')

                        if __config__['invite_code'] != '':
                            self.api.join_server(__config__['invite_code'])

                        with open('./data/account.txt', 'a+') as f:
                            f.write(f'{mail}:{password}:{cookies.get("hmac_signed_session")}\n')
                        
                        if __config__['save_cookies_separated'] == True:
                            with open('./data/cookies.txt', 'a+') as f:
                                f.write(f'{cookies.get("hmac_signed_session")}\n')
                else:
                    Console.debug('[-] Error', success)
        except Exception as e:
            Console.debug(f'[*] Creation error: {e}')

    def run(self) -> None:
        self.create_account(next(self.data.usernames) if __config__['custom_usernames'] == True else "".join([random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(10)]), self.data.email.get_mail(__config__['mail'].split('@')[0]), "".join([random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(10)]))

if __name__ == '__main__':
    proxies= itertools.cycle(open('./data/proxies.txt').read().splitlines())
    Console.print_logo()
    data = Data()

    while True:
        while threading.active_count() >= __config__['threads']:
            time.sleep(1)
        
        Creator(f'http://{next(proxies)}', data).start()