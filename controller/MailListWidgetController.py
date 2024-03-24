from models.email_client.email_parser import Email_Parser
from models.email_client.gmail_parser import Gmail_Parser
from models.provider import Provider

class MailListWidgetController:
    def __init__(self,bdd):
        self.bdd = bdd


    def refreshEmails(self):
        attachments = []
        infos = self.bdd.get_all_identifications()
        for info in infos:
            files = self.parseAllEmailsFromAdress(info[0],info[1],Provider(info[0].split("@")[1].split(".")[0]).getProvider())
            if files is not None :
                attachments += files
        for attachment_name in attachments:
            #print(attachment_name)
            pass
            
    def parseAllEmailsFromAdress(self,adresse,mdp,provider):
        #dire au Parser de récupérer tout les mails disponibles sur la boite mail
        if "gmail" in adresse:
            email_Parser = Gmail_Parser(adresse,mdp,provider,self.bdd)
        else :
            email_Parser = Email_Parser(adresse,mdp,provider,self.bdd)
        attachments = email_Parser.getAllMails()
        email_Parser.close()
        return attachments
        

    def getAllStoreMail(self,list_tags):
        bdd_list = []
        for tag in list_tags:
            bdd_list += self.bdd.get_emails(tag)
        
        return bdd_list
    
    def getMailsFromAdress(self,adresse,folder):
        return self.bdd.get_emails_for_address(adresse,folder)
    
    def getBdd(self):
        return self.bdd