from imap_tools import MailBox
import random, string, threading, time

class Gmail:
    def __init__(self, mail: str, password: str) -> None:
        self.mail = mail
        self.password = password
        self.blacklist = []
        self.mail_list = {}

        threading.Thread(target= self.parser_thread).start()
    
    def parser_thread(self) -> None:
        while True:
            with MailBox('imap.gmail.com', '993').login(self.mail, self.password, 'INBOX') as mailbox:
                for msg in mailbox.fetch():
                    try:
                        body = msg.html
                        to = str(msg.to[0]).lower()

                        if to not in self.blacklist:
                            verif = body.split('https://www.guilded.gg/api/email/verify?token=')[1].split('"')[0]
                            self.mail_list[to] = verif
                            self.blacklist.append(to)
                    except Exception as e:
                        print(e)
            time.sleep(1)
    
    @staticmethod
    def get_mail(mail_base: str) -> str:        
        return mail_base + "+" + "".join([random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(10)]) + "@gmail.com"