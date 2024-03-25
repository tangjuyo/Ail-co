from PyQt5.QtWidgets import QVBoxLayout,QHBoxLayout,QPushButton,QTreeWidget,QTreeWidgetItem,QWidget,QLabel,QSizePolicy
from PyQt5.QtGui import QFont,QIcon
from models.utils.utils import Utils
from PyQt5.QtCore import Qt

class CustomTreeWidget(QWidget):
    def __init__ (self,bdd, parent = None):
        super(CustomTreeWidget, self).__init__(parent)
        self.setStyleSheet("background-color: #333333; color: white;")
        self.inbox_to_try = ["Inbox", "INBOX"]
        self.sent_to_try = ["INBOX/OUTBOX", "Sent"]
        self.deleted_to_try = ["INBOX/TRASH", "Deleted"]
        self.spam_to_try = ["Junk","[Gmail]/Spam"]

        #barre du haut
        self.layout = QVBoxLayout()
        self.bdd = bdd
        # Barre de recherche
        self.search_bar()
        # Arbre des catégories d'e-mails
        self.category_tree = QTreeWidget()
        self.category_tree.setStyleSheet("QTreeWidget::item { padding: 3px;  font-size: 50pt;}")
        self.category_tree.setHeaderHidden(True)
        self.category_tree.setColumnCount(2)
        self.category_tree.setColumnWidth(0,int(self.frameSize().width()/2.77))
        #set de la taille au minimum possible pour ne pas prendre de la size inutile
        self.category_tree.setColumnWidth(1,1)
        self.createAllTree()

    def search_bar(self):
        search_layout = QHBoxLayout()
        search_button = QPushButton("Rechercher")
        search_layout.addWidget(search_button)
        self.layout.addLayout(search_layout)

    def createAllTree(self):
        # Définir le padding avec une feuille de style CSS
        
        self.layout.addWidget(self.category_tree)

        #création branche générale
        self.general_Tree()
        #création de l'arbre de chaque adresse
        for mail in self.bdd.get_all_email_addresses():
            self.email_branch_tree(mail)

        self.category_tree.setExpandsOnDoubleClick(False)
        self.category_tree.expandAll()
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.category_tree.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def general_Tree(self):

        #création du général
        general_mail_tree_widget = QTreeWidgetItem()
        icon_mail = QIcon("vue/image/favorite.png")
        general_mail_tree_widget.setIcon(0,icon_mail)
        general_mail_tree_widget.setText(0,"Général")
        font = QFont()
        font.setBold(True)
        general_mail_tree_widget.setFont(0,font)
        # Ajouter les catégories à l'arbre
        self.category_tree.addTopLevelItem(general_mail_tree_widget)

        received_category = QTreeWidgetItem()
        icon_inbox = QIcon("vue/image/inbox.png")
        received_category.setIcon(0,icon_inbox)
        received_category.setText(0,"Boîte de réception")
        received_category.setText(1,str(self.bdd.count_all_emails(self.inbox_to_try)))
        sent_category = QTreeWidgetItem()
        icon_sent = QIcon("vue/image/send.png")
        sent_category.setIcon(0,icon_sent)
        sent_category.setText(0,"Éléments envoyés")
        sent_category.setText(1,str(self.bdd.count_all_emails(self.sent_to_try)))
        remove_category = QTreeWidgetItem()
        icon_remove = QIcon("vue/image/delete.png")
        remove_category.setIcon(0,icon_remove)
        remove_category.setText(0,"Élements supprimés")
        remove_category.setText(1,str(self.bdd.count_all_emails(self.deleted_to_try)))

        #ajouter catégories principales au mail
        general_mail_tree_widget.addChild(received_category)
        general_mail_tree_widget.addChild(sent_category)
        general_mail_tree_widget.addChild(remove_category)


    def email_branch_tree(self,mail):

        mail_tree_widget = QTreeWidgetItem()
        icon_mail = QIcon("vue/image/favorite.png")
        mail_tree_widget.setIcon(0,icon_mail)
        mail_tree_widget.setText(0,mail)
        font = QFont()
        font.setBold(True)
        mail_tree_widget.setFont(0,font)


        

        # Catégories principales
        received_category = QTreeWidgetItem()
        icon_inbox = QIcon("vue/image/inbox.png")
        received_category.setIcon(0,icon_inbox)
        received_category.setText(0,"Boîte de réception")
        for folder in self.inbox_to_try:
            count = self.bdd.count_emails_in_mailbox_folder(mail,folder)
            received_category.setText(1,str(count))
            if count > 0:
                break
        sent_category = QTreeWidgetItem()
        icon_sent = QIcon("vue/image/send.png")
        sent_category.setIcon(0,icon_sent)
        sent_category.setText(0,"Éléments envoyés")
        for sent in self.sent_to_try:
            count = self.bdd.count_emails_in_mailbox_folder(mail,sent)
            sent_category.setText(1,str(count))
            if count > 0:
                break
        
        remove_category = QTreeWidgetItem()
        icon_remove = QIcon("vue/image/delete.png")
        remove_category.setIcon(0,icon_remove)
        remove_category.setText(0,"Élements supprimés")
        for deleted in self.deleted_to_try:
            count = self.bdd.count_emails_in_mailbox_folder(mail,deleted)
            remove_category.setText(1,str(count))
            if count > 0:
                break
        spam_category = QTreeWidgetItem()
        icon_spam = QIcon("vue/image/spam.png")
        spam_category.setIcon(0,icon_spam)
        spam_category.setText(0,"Spam")
        for spam in self.spam_to_try:
            count = self.bdd.count_emails_in_mailbox_folder(mail,spam)
            spam_category.setText(1,str(count))
            if count > 0:
                break
        
        
        #ajouter catégories principales au mail
        mail_tree_widget.addChild(received_category)
        mail_tree_widget.addChild(sent_category)
        mail_tree_widget.addChild(remove_category)
        mail_tree_widget.addChild(spam_category)

        # Ajouter les catégories à l'arbre
        self.category_tree.addTopLevelItem(mail_tree_widget)
        
    def getCategory_tree(self):
        return self.category_tree
    
    def update(self):
        self.category_tree.clear()
        self.createAllTree()