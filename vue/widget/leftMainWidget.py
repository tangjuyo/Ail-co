from PySide6.QtWidgets import QWidget
from vue.widget.customTreeWidget import CustomTreeWidget
from models.jsonConfigs.readVariables import readVariables

class leftMainWidget(QWidget):
    def __init__(self, controller,emails,show_selected_mails_callback):
        super().__init__()
        self.categories_to_try = [
            readVariables.lire_variable("CustomTreeWidget","Boîte de réception"),
            readVariables.lire_variable("CustomTreeWidget","Éléments envoyés"),
            readVariables.lire_variable("CustomTreeWidget","Éléments supprimés"),
            readVariables.lire_variable("CustomTreeWidget","Spam")
            ]
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
        self.customTreeWidget = CustomTreeWidget(self.controller)
        self.category_tree = self.customTreeWidget.getCategory_tree()
        self.category_tree.itemClicked.connect(self.expand_categories)
        self.category_tree.setFixedWidth(int(self.customTreeWidget.width()*0.45))
        self.customTreeWidget.setMaximumWidth(int(self.customTreeWidget.width()*0.45))
    
    def loadEmails(self):
        self.all_emails = self.controller.getLoadedMails()

    def expand_categories(self, item):
        # Implémentez la logique pour l'expansion des catégories ici
        if item.parent() is not None:
            parent_text = item.parent().text(0)
            item_text = item.text(0)
            if parent_text == readVariables.lire_variable("CustomTreeWidget","GeneralBox"):
                self.emails = self.all_emails.loc[(self.all_emails['folder'] == str(readVariables.lire_global_variable_from_language(item_text)))]
            else:
                if item_text in self.categories_to_try:
                    self.emails = self.all_emails.loc[(self.all_emails['folder'] == str(readVariables.lire_global_variable_from_language(item_text))) & (self.all_emails['mail'] == parent_text)]
            self.show_selected_mails_callback(self.emails)
        if item.childCount() > 0:
            item.setExpanded(not item.isExpanded())
            
    def getCustomTree(self):
        return self.customTreeWidget
    
    def update_tree(self):
        self.loadEmails()
        self.customTreeWidget.update()