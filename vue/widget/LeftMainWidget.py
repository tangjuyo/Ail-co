from PyQt5.QtWidgets import QWidget, QVBoxLayout
from vue.widget.customTreeWidget import CustomTreeWidget

class LeftMainWidget(QWidget):
    def __init__(self, controller,emails,show_selected_mails_callback):
        super().__init__()
        
        self.boîte_de_réception_to_try = ["Inbox", "INBOX"]
        self.éléments_envoyés_to_try = ["INBOX/OUTBOX", "Sent"]
        self.éléments_supprimés_to_try = ["INBOX/TRASH", "Deleted"]
        self.spam_to_try = ["Junk","[Gmail]/Spam"]
        self.controller = controller
        self.emails = emails
        self.show_selected_mails_callback = show_selected_mails_callback
        self.all_emails = {}
        self.loadEmails()
        
        
        # Ajoutez ici tout le contenu de la partie gauche de votre application
        self.customTreeWidget = CustomTreeWidget(self.controller.bdd)
        self.category_tree = self.customTreeWidget.getCategory_tree()
        self.category_tree.itemClicked.connect(self.expand_categories)
        self.category_tree.setFixedWidth(int(self.customTreeWidget.width()*0.41))
        self.customTreeWidget.setMaximumWidth(int(self.customTreeWidget.width()*0.41))
        
        layout = QVBoxLayout()
        layout.addWidget(self.customTreeWidget)
        self.setLayout(layout)

    
    def loadEmails(self):
        
        emailsNames = self.controller.bdd.get_all_email_addresses()
        
        categories_to_try = ["Boîte de réception","Éléments envoyés","Éléments supprimés","Spam"]
        
        for emailname in emailsNames :
            emaildict = {}
            for category_name in categories_to_try:
                emails = []
                for mailbox in getattr(self, f"{category_name.lower().replace(' ', '_')}_to_try"):
                    emails.extend(self.controller.getMailsFromAdress(emailname, mailbox))
                emaildict[category_name] = emails
            self.all_emails[emailname] = emaildict
            
        general_dict = {}
        for category_name,_ in categories_to_try:
            general_dict[category_name] = self.controller.getAllStoreMail(getattr(self, f"{category_name.lower().replace(' ', '_')}_to_try"))
        self.all_emails["Général"] = general_dict


    def expand_categories(self, item):
        # Implémentez la logique pour l'expansion des catégories ici
        if item.parent() is not None:
            parent_text = item.parent().text(0)
            item_text = item.text(0)
                        
            if parent_text == "Général":
                if item_text in ["Boîte de réception", "Éléments envoyés", "Éléments supprimés"]:
                    self.emails = self.all_emails["Général"][item_text.lower()]
            else:
                if item_text in ["Boîte de réception", "Éléments envoyés", "Éléments supprimés", "Spam"]:
                    self.emails = self.all_emails[parent_text.lower()][item_text.lower()]

            self.show_selected_mails_callback(self.emails)
            
        if item.childCount() > 0:
            item.setExpanded(not item.isExpanded())
            
    def getCustomTree(self):
        return self.customTreeWidget
    
    def update_tree(self):
        self.customTreeWidget.update()