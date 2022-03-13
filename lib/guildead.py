# Lasted wrapper version: https://github.com/Its-Vichy/Guildead

import requests, uuid, random, string

class Exploit:
    def blank_message():
        return [random.choice(string.ascii_letters + string.ascii_uppercase + string.digits) for _ in range(random.randint(1000, 1000))]

class Guilded:
    def __init__(self, proxy: str= None):
        self.base_url = "https://www.guilded.gg/api"
        self.session = requests.Session()
        self.session.proxies = {"http": proxy, "https": proxy} if proxy else None

        self.user = None

    def login(self, email: str, password: str):
        r = self.session.post(f'{self.base_url}/login', json={'email': email, 'password': password, 'getMe': True})
        
        try:
            self.user= r.json()['user']
        except:
            pass

        return (False, {'error': 'Email or password is incorrect.'}) if 'Email or password is incorrect.' in r.text or r.cookies.get('guilded_mid') == None else (True, {'mid': r.cookies.get('guilded_mid'), 'hmac_signed_session': r.cookies.get('hmac_signed_session')})
    
    def login_from_token(self, token: str):
        self.session.cookies.set('hmac_signed_session', token)

    def send_message(self, channel_id: str, message: str, confirmed: bool= False, isSilent: bool= False, isPrivate: bool= False, repliesTo: list= []):
        r = self.session.post(f'{self.base_url}/channels/{channel_id}/messages', json={
            "messageId": str(uuid.uuid1()),
            "content": {
                "object": "value",
                "document": {
                    "object": "document",
                    "data": {},
                    "nodes": [
                        {
                            "object": "block",
                            "type": "paragraph",
                            "data": {},
                            "nodes": [
                                {
                                    "object": "text",
                                    "leaves": [
                                        {
                                            "object": "leaf",
                                            "text": message,
                                            "marks": []
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            },
            "repliesToIds": repliesTo,
            "confirmed": confirmed,
            "isSilent": isSilent,
            "isPrivate": isPrivate
        })
        return r.json()
    
    def edit_message(self, channel_id: str, message_id: str, message: str, confirmed: bool= False, isSilent: bool= False, isPrivate: bool= False, repliesTo: list= []):
        r = self.session.put(f'{self.base_url}/channels/{channel_id}/messages/{message_id}', json={
            "messageId": message_id,
            "content": {
                "object": "value",
                "document": {
                    "object": "document",
                    "data": {},
                    "nodes": [
                        {
                            "object": "block",
                            "type": "paragraph",
                            "data": {},
                            "nodes": [
                                {
                                    "object": "text",
                                    "leaves": [
                                        {
                                            "object": "leaf",
                                            "text": message,
                                            "marks": []
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            },
            "repliesToIds": repliesTo,
            "confirmed": confirmed,
            "isSilent": isSilent,
            "isPrivate": isPrivate
        })
        return r.json()
    
    def delete_message(self, channel_id: str, message_id: str):
        r = self.session.delete(f'{self.base_url}/channels/{channel_id}/messages/{message_id}')
        return r.json()
    
    def join_server(self, invite_code: str):
        r = self.session.put(f'{self.base_url}/invites/{invite_code}')
        return r.json()
    
    def add_friend(self, ids: list):
        r = self.session.post(f'{self.base_url}/users/me/friendrequests', json={"friendUserIds": ids})
        return r.json()
    
    def check_mail_verified(self):
        r = self.session.get(f'{self.base_url}/users/me/verification')
        return r.json()
    
    def get_server_info(self, invite_code: str):
        r = self.session.get(f'{self.base_url}/content/route/metadata?route=/{invite_code}')
        return r.json()

    def join_team(self, invite_code: str):
        team_id = self.get_server_info(invite_code)['metadata']['team']['id']
        user_id = self.user['id']
        
        r = self.session.put(f'{self.base_url}/teams/{team_id}/members/{user_id}/join', json={'inviteId': None})
        return r.json()

    # not working for the moment
    def add_pfp(self, image_path):
        return self.session.post('https://media.guilded.gg/media/upload?dynamicMediaTypeId=UserAvatar', files={'file': open(image_path, 'rb').read()}, headers={'content-type': 'multipart/form-data; boundary=----WebKitFormBoundary47tZnndaOSKfxxSv'}, stream=True)