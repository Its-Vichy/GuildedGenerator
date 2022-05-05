import json, threading, httpx, random, string, time, binascii, os, json, itertools
from lib.guildead import Guilded
from lib.console import Console
from lib.mail import MailGwApi
from lib.data import Data

__config__ = json.load(open('./config.json', 'r+'))


class Creator(threading.Thread):
    def __init__(self, proxy: str, data: Data) -> None:
        self.api = Guilded(proxy)
        self.proxy = proxy
        self.data = data

        threading.Thread.__init__(self)

    def get_rstr(self, lenght: int) -> str:
        return str(binascii.b2a_hex(os.urandom(lenght)).decode('utf-8'))

    def create_account(self, username: str, mail: str, password: str, tp: MailGwApi=None) -> None:
        data = {"extraInfo":{"platform": "desktop", "referrerId": __config__['referer']}, "name": username, "email": mail,"password": password,"fullName": username}

        h = {
            'authority': 'www.guilded.gg',
            'method': 'POST',
            'path': '/api/users?type=email',
            'scheme': 'https',

            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'fr-FR,fr;q=0.9',
            'content-type': 'application/json',
            'guilded-client-id': f'{self.get_rstr(8)}-{self.get_rstr(4)}-{self.get_rstr(4)}-{self.get_rstr(4)}-{self.get_rstr(12)}',
            'guilded-device-id': self.get_rstr(64),
            'guilded-device-type': 'desktop',
            'guilded-stag': self.get_rstr(32),
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

                if 'You have been banned.' in r.text:
                    self.data.banned += 1
                    Console.debug(f'[>] Banned')
                    return
                else:
                    Console.debug(f'[>] {r.json()}')

                success, cookies = self.api.login(mail, password)
                
                if success:
                    Console.printf(f'[+] {username} has been created.')
                    self.data.generated += 1

                    data_mail= {"email": mail}
                    #client.headers['content-lenght'] = str(len(json.dumps(data_mail)))
                    client.post(f'{self.api.base_url}/email/verify', json= data_mail, cookies= cookies)
                    
                    #client.headers.pop('content-lenght')

                    verif_token= None 
                    while verif_token == None:
                        time.sleep(1)
                        try:
                            if tp == None:
                                verif_token = self.data.email.mail_list[mail.lower()]
                            else:
                                for mail in tp.fetch_inbox():
                                    content = str(tp.get_message(mail['id'])['html'])
                                    verif_token = content.split('https://www.guilded.gg/api/email/verify?token=')[1].split('"')[0]
                        except:
                            pass
                    
                    if tp == None:
                        self.data.email.mail_list.pop(mail.lower())

                    Console.printf(f'[*] Verification token found: {verif_token}')
                    client.get('https://www.guilded.gg/api/email/verify?token=' + verif_token, cookies= cookies).text

                    if self.api.check_mail_verified()['email']:
                        Console.printf(f'[>] Email verified: {username}')
                        self.data.verified += 1

                        if __config__['invite_code'] != '':
                            self.api.join_server(__config__['invite_code'])

                        with open('./data/account.txt', 'a+') as f:
                            f.write(f'{mail}:{password}:{cookies.get("hmac_signed_session")}\n')
                        
                        if __config__['save_cookies_separated']:
                            with open('./data/cookies.txt', 'a+') as f:
                                f.write(f'{cookies.get("hmac_signed_session")}\n')
                        
                        if __config__['set_online']:
                            Console.printf(f'[~] Set online: {username}')
                            self.api.set_activity(random.randint(1, 3))
                            self.api.ping()

                        if __config__['set_status']:
                            Console.printf(f'[~] Set status: {username}')
                            self.api.set_status(next(self.data.status) if __config__['custom_status'] else 'GuildeadGen - github.com/its-vichy')
                        
                        if __config__['set_bio']:
                            Console.printf(f'[~] Set bio: {username}')
                            self.api.set_bio(next(self.data.bio) if __config__['custom_bio'] else self.data.get_bio(self.proxy))
                        
                        if __config__['set_pfp']:
                            Console.printf(f'[~] Set pfp: {username}')
                            self.api.add_pfp(next(self.data.pfp))
                else:
                    Console.debug(f'[-] Error when logged in: {success}')
        except Exception as e:
            Console.debug(f'[*] Creation error: {e}')

    def run(self) -> None:
        password = "".join([random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(10)])

        if __config__['use_tempmail']:
            api = MailGwApi(proxy= self.proxy, timeout=30)

            email = api.get_mail(domain='bluebasketbooks.com.au')
            
            if email == None:
                return

            self.create_account(next(self.data.usernames) if __config__['custom_usernames'] == True else "".join([random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(10)]), email, password, api)
        else:
            email    = self.data.email.get_mail(__config__['mail'].split('@')[0])
            self.create_account(next(self.data.usernames) if __config__['custom_usernames'] == True else "".join([random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(10)]), email, password)


if __name__ == '__main__':
    proxies= itertools.cycle(open('./data/proxies.txt').read().splitlines())
    Console.print_logo()
    data = Data()
    
    while True:
        while threading.active_count() >= __config__['threads']:
            time.sleep(1)
        
        Creator(f'http://{next(proxies)}' if __config__['proxyless'] == False else None, data).start()