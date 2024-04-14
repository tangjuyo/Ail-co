from models.SQliteDAO import SQLiteDAO
from models.email_parser import Email_Parser
from models.provider import Provider
import pandas as pd

class EmailManager:
    
    def __init__(self, db_file,password):
        self.dao = SQLiteDAO(db_file,password)        
        self.loadEmails()
    
    def getLoadedMails(self):
        return self.emails_df
    
    def addEmails(self,adresse,password):
        self.dao.add_email_password(adresse,password)
    
    def getMailsFromAdress(self,adresse,folder):
        return self.dao.get_emails_for_address(adresse,folder)
    
    def loadEmails(self):
        all_emails = []
        all_emails.extend(self.dao.get_emails())
        # Créer un DataFrame avec les e-mails chargés
        self.emails_df = pd.DataFrame(all_emails)
        if len(self.emails_df) != 0 :
            column_names  = ['sender', 'subject', 'body', 'folder', 'mail','date','uid']
            # Set the index
            self.emails_df.columns = column_names

    def count_emails_in_mailbox_folder(self, emailname,category_name):
        try :
            return len(self.emails_df[(self.emails_df['mail'] == emailname) & (self.emails_df['folder'] == category_name)])
        except :
            return 0

    def count_all_emails(self,category):
        try:
            return len(self.emails_df[self.emails_df['folder'] == category])
        except:
            return 0
        
    def parseAllEmailsFromAdress(self,adresse,mdp,provider):
        #dire au Parser de récupérer tout les mails disponibles sur la boite mail
        email_Parser = Email_Parser(adresse,mdp,provider)
        allNewEmails = email_Parser.getAllMails()
        #email_Parser.close()
        for email in allNewEmails :
            self.dao.add_email(email)
        self.loadEmails()

    def refreshEmails(self):
        infos = self.dao.get_all_identifications()
        for info in infos:
            self.parseAllEmailsFromAdress(info[0],info[1],Provider(info[0].split("@")[1].split(".")[0]).getProvider())
    
    def get_all_email_addresses(self):
        return self.dao.get_all_email_addresses()