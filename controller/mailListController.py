from models.RefreshThreadEmail import RefreshWorker
from PySide6.QtWidgets import QWidget
from models.provider import Provider
from PySide6.QtCore import Signal

class mailListController(QWidget):
    add_email_thread_finished_signal = Signal()
    
    def __init__(self,emailManager):
        super().__init__()
        self.emailManager = emailManager

    def getLoadedMails(self):
        return self.emailManager.getLoadedMails()
    
    def count_emails_in_mailbox_folder(self,mail,category):
        print(str(self.emailManager.count_emails_in_mailbox_folder(mail,category)))
        return self.emailManager.count_emails_in_mailbox_folder(mail,category)
    
    def count_all_emails(self,category):
        return self.emailManager.count_all_emails(category)
    
    def searchItem(self,texte):
        pass
    def refreshEmails(self):
        self.emailManager.refreshEmails()
    
    def getMailsFromAdress(self,adresse,folder):
        return self.emailManager.getMailsFromAdress(adresse,folder)
    
    def add_email_password(self,adresse,password):
        self.emailManager.addEmails(adresse,password)
    
    def addEmailsThread(self,loadingWidget,email,password,provider):
        self.thread = RefreshWorker(self.emailManager,self.emailManager.parseAllEmailsFromAdress,email,password,Provider(provider).getProvider())
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(loadingWidget.close)
        self.thread.finished.connect(self.add_email_thread_finished_signal)
        self.thread.start()
        
    def refreshEmailsThread(self,loadingWidget):
        self.thread = RefreshWorker(self.emailManager,self.emailManager.refreshEmails)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(loadingWidget.close)
        self.thread.finished.connect(self.add_email_thread_finished_signal)
        self.thread.start()
        
    def get_all_email_addresses(self):
        return self.emailManager.get_all_email_addresses()