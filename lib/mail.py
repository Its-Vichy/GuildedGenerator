from imap_tools import MailBox
import random, string

class Gmail:
    def get_mail(mail_base: str):        
        return mail_base + "+" + "".join([random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(10)]) + "@gmail.com"

    def get_verif_token(fake_mail: str, mail: str, password: str):
        with MailBox('imap.gmail.com', '993').login(mail, password, 'INBOX') as mailbox:
            for msg in mailbox.fetch():
                if str(msg.to[0]).lower() == fake_mail.lower():
                    body = msg.html
                    verif = body.split('https://www.guilded.gg/api/email/verify?token=')[1].split('"')[0]
                    return verif
