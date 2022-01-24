from imap_tools import MailBox
import random, string

class Gmail:
    def get_mail():
        def insert_dots(s, k):
            indices = sorted(random.sample(range(1, len(s) - 1), k))
            intervals = []

            for i, j in zip([0] + indices, indices + [len(s)]):
                intervals.append(s[i:j])

            return '.'.join(intervals) + "@gmail.com"

        # return insert_dots(s, random.randint(1, len(s) - 3))

        s = 'nokdsfuihdsufgnzeuifhiuezfbifr+'
        return s + "".join([random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(10)]) + "@gmail.com"

    def get_verif_token(mail: str):
        with MailBox('imap.gmail.com', '993').login('email@gmail.com', 'password', 'INBOX') as mailbox:
            for msg in mailbox.fetch():
                if msg.to[0] == mail:
                    body = msg.html
                    verif = body.split('https://www.guilded.gg/api/email/verify?token=')[1].split('"')[0]
                    return verif