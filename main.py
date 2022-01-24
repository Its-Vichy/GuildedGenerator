from lib import guildead, mail
import json, threading, httpx, random, string, time, binascii, os

__THREAD__, __INVITE__, __REFERRER__ = 1, "2ZvgQvy2", "d5D2Q0V4"

class Creator(threading.Thread):
    def __init__(self, proxy: str):
        self.api = guildead.Guilded(proxy)
        self.mail = mail.Gmail
        self.proxy = proxy

        threading.Thread.__init__(self)

    def create_account(self, username: str, mail: str, password: str):
        data = {"extraInfo":{"platform":"electron", "referrerId": __REFERRER__}, "name": username, "email": mail,"password": password,"fullName": username}

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
            'guilded-stag': 'c4740afd3f3e4d63d365d826139de166',
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

        with httpx.Client(proxies= self.proxy, headers= h) as client:
            client.cookies = client.put('https://www.guilded.gg/api/data/event').cookies
            
            client.headers['content-length'] = str(len(json.dumps(data)))
            r= client.post(f'{self.api.base_url}/users?type=email', json= data)
            print(r.json())    
            success, cookies = self.api.login(mail, password)
            
            if success:
                print(f'[+] {username} has been created.')

                data_mail= {"email": mail}
                client.headers['content-lenght'] = str(len(json.dumps(data_mail)))
                client.post(f'{self.api.base_url}/email/verify', json= data_mail, cookies= cookies)

                verif_token= None 
                while verif_token == None:
                    try:
                        verif_token = self.mail.get_verif_token(mail)
                    except:
                        pass

                print(f'[*] Verification token found: {verif_token}')
                client.get('https://www.guilded.gg/api/email/verify?token=' + verif_token, cookies= cookies).text

                if self.api.check_mail_verified()['email'] == True:
                    print(f'[+] Email verified: {username}')
                    self.api.join_server(__INVITE__)

                    with open('./data/account.txt', 'a+') as f:
                        f.write(f'{mail}:{password}\n')
            else:
                print('[-] Error', success)

    def run(self):
        while True:
            self.create_account("".join([random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(10)]), self.mail.get_mail(), "".join([random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(10)]))

proxies= open('./data/proxies.txt').read().split('\n')
for _ in range(__THREAD__):
    Creator('http://'+ random.choice(proxies).split('\n')[0]).start()