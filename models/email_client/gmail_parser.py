from models.email_client.email_parser import Email_Parser
import imapclient
from email.header import decode_header
import email,os
from models.utils import utils
from models.email import Email

class Gmail_Parser(Email_Parser):
    def __init__(self, address_mail, mdp, provider, bdd) -> None:
        super().__init__(address_mail, mdp, provider, bdd)


    def getAllMails(self):

        for folder in self.mail.list_folders():
            if folder[-1] != "[Gmail]"  :
                if folder[-1] != "[Gmail]/Tous les messages" :
                    self.getAllMailsFromFolder(folder[-1])
