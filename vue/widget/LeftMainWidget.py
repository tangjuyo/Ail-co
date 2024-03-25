from PyQt5.QtWidgets import QWidget, QVBoxLayout
from vue.widget.customTreeWidget import CustomTreeWidget

class LeftMainWidget(QWidget):
    def __init__(self, controller,emails,show_selected_mails_callback):
        super().__init__()
        
        self.boîte_de_réception_to_try = ["Inbox", "INBOX"]
        self.éléments_envoyés_to_try = ["INBOX/OUTBOX", "Sent"]
        self.élements_supprimés_to_try = ["INBOX/TRASH", "Deleted"]
        self.spam_to_try = ["Junk","[Gmail]/Spam"]
        self.controller = controller
        self.emails = emails
        self.show_selected_mails_callback = show_selected_mails_callback
        
        # Ajoutez ici tout le contenu de la partie gauche de votre application
        self.customTreeWidget = CustomTreeWidget(self.controller.bdd)
        self.category_tree = self.customTreeWidget.getCategory_tree()
        self.category_tree.itemClicked.connect(self.expand_categories)
        self.category_tree.setFixedWidth(int(self.customTreeWidget.width()*0.41))
        self.customTreeWidget.setMaximumWidth(int(self.customTreeWidget.width()*0.41))
        
        layout = QVBoxLayout()
        layout.addWidget(self.customTreeWidget)
        self.setLayout(layout)

    def expand_categories(self, item):
        # Implémentez la logique pour l'expansion des catégories ici
        if item.parent() is not None:
            parent_text = item.parent().text(0)
            item_text = item.text(0)
            self.emails.clear()
            
            if parent_text == "Général":
                if item_text in ["Boîte de réception", "Éléments envoyés", "Élements supprimés"]:
                    if item_text == "Boîte de réception":
                        self.emails = self.controller.getAllStoreMail(self.boîte_de_réception_to_try)
                    elif item_text == "Éléments envoyés":
                        self.emails = self.controller.getAllStoreMail(self.éléments_envoyés_to_try)
                    elif item_text == "Élements supprimés":
                        self.emails = self.controller.getAllStoreMail(self.élements_supprimés_to_try)
                else:
                    for mailbox in self.boîte_de_réception_to_try + self.éléments_envoyés_to_try + self.élements_supprimés_to_try + self.spam_to_try:
                        self.emails = self.controller.getMailsFromAdress(parent_text, mailbox)
                        if len(self.emails) > 0:
                            break
            else:
                if item_text in ["Boîte de réception", "Éléments envoyés", "Élements supprimés", "Spam"]:
                    if hasattr(self, f"{item_text.lower().replace(' ', '_')}_to_try"):
                        for mailbox in getattr(self, f"{item_text.lower().replace(' ', '_')}_to_try"):
                            self.emails = self.controller.getMailsFromAdress(parent_text, mailbox)
                            if len(self.emails) > 0:
                                break
                            
            self.show_selected_mails_callback(self.emails)
            
        if item.childCount() > 0:
            item.setExpanded(not item.isExpanded())
            
    def getCustomTree(self):
        return self.customTreeWidget
    
    def update_tree(self):
        self.customTreeWidget.update()