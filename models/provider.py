class Provider:

    dict_provider = {
    "gmail": "imap.gmail.com",
    "outlook": "imap-mail.outlook.com",
    "yahoo": "imap.mail.yahoo.com",
    "iCloud": "imap.mail.me.com",
    "AOL": "imap.aol.com",
    "zoho": "imap.zoho.com",
    "GMX": "imap.gmx.com",
    "yandex": "imap.yandex.com",
    "mail": "imap.mail.com",
    "orange": "imap.orange.fr"
    }
    
    def __init__(self,provider) -> None:
        self.provider=provider
        

    def getProvider(self):
        return self.dict_provider[self.provider]