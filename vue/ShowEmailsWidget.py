from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QListWidget, QListWidgetItem, QPushButton,QHBoxLayout,QToolButton,QMenu
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont,QIcon, QPixmap
from vue.AddEmailsWidget import AddEmailsWidget
from models.provider import Provider
from vue.CustomListWidgetItem import CustomListWidgetItem 
from vue.HtmlViewWidget import HtmlViewWidget
from vue.LoadingWidget import LoadingWidget
from vue.CustomTreeWidget import CustomTreeWidget
from models.RefreshThreadEmail import RefreshWorker

class MailListWidget(QWidget):
    
    def __init__(self,controller):
        super().__init__()
        self.setWindowTitle('Liste des Mails')
        self.setWindowFlags(self.windowFlags() | Qt.WindowCloseButtonHint)
        self.resize_to_half_screen()  # Redimensionne la fenêtre à la moitié de l'écran
        self.layout = QHBoxLayout()
        self.layout.stretch(5)
        self.controller = controller
        self.emails = []
        self.intOrdreMails = 1
        self.inbox_to_try = ["Inbox", "INBOX"]
        self.sent_to_try = ["INBOX/OUTBOX", "Sent"]
        self.deleted_to_try = ["INBOX/TRASH", "Deleted"]
        self.spam_to_try = ["Junk","[Gmail]/Spam"]
        
        #barre latérale de gauche
        self.customTreeWidget = CustomTreeWidget(self.controller.bdd)

        self.category_tree = self.customTreeWidget.getCategory_tree()
        self.category_tree.itemClicked.connect(self.expand_categories)
        self.category_tree.setFixedWidth(int(self.customTreeWidget.width()*0.41))
        self.customTreeWidget.setMaximumWidth(int(self.customTreeWidget.width()*0.41))
        self.layout.addLayout(self.customTreeWidget.layout)
        
        

        #barre latérale de droite
        layoutRight = QVBoxLayout()
        # Liste des mails
        self.mail_list = QListWidget(self)
        self.mail_list.itemClicked.connect(self.display_mail_content)
        
        #a faire mieux // il a pas a populate de lui meme au début sauf si des comptes sont enregistrés
        self.populate_launch_mail_list()
        #provisoire pour mettre les mails dans l'ordre date plus recent
        self.sortByRecentDate()
        

        #gestion du bandeau au dessus des mails
        self.bandeauLayout  = QHBoxLayout()

        #Bouton pour refresh les mails
        self.button_refresh = QToolButton(self)
        self.button_refresh.setIcon(QIcon(QPixmap("vue/image/refresh.png")))
        self.button_refresh.clicked.connect(self.refresh_mails)
        self.bandeauLayout.addWidget(self.button_refresh)

        # Bouton pour ouvrir l'interface AddEmailsWidget
        self.add_emails_button = QPushButton('Ajouter des adresses mails')
        self.add_emails_button.clicked.connect(self.open_add_emails_window)
        self.bandeauLayout.addWidget(self.add_emails_button)

        

        #Bouton pour afficher options de trie
        self.button_trie = QToolButton(self)
        self.button_trie.setIcon(QIcon(QPixmap("vue/image/trie.png")))
        self.button_trie.clicked.connect(self.show_menu)
        self.bandeauLayout.addWidget(self.button_trie)
        # Créer le menu déroulant du bouton de trie
        self.menu = QMenu(self)
        self.menu.addAction("Trier par date")
        self.menu.addAction("Trier par expéditeur")
        self.menu.addAction("Trier par sujet")
        self.menu.addSeparator()
        self.menu.addAction("Ordre croissant",self.sortByOldDate)
        self.menu.addAction("Ordre décroissant",self.sortByRecentDate)
        layoutRight.addLayout(self.bandeauLayout)
        
    
        #affichage des mails
        self.showSelectedMails()
        # Ajout de la liste des mails au layout
        layoutRight.addWidget(self.mail_list)
        #ajout layout de droite à la vue
        self.layout.addLayout(layoutRight)
        self.layout.setStretchFactor(self.customTreeWidget.layout,2)
        self.layout.setStretchFactor(layoutRight,8)

        self.setLayout(self.layout)
    

    def refresh_mails(self):
        #création du widget de loading
        self.loadingWidget = LoadingWidget()
        self.loadingWidget.loadMovie()

        self.thread = RefreshWorker(self.controller,self.controller.refreshEmails)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(self.loadingWidget.close)
        self.thread.finished.connect(self.loadingWidget.deleteLater)
        self.thread.start()
        # Affichez le widget de chargement
        self.loadingWidget.show()


    def expand_categories(self, item):

        if item.parent() is not None:
            if item.parent().text(0) == "Général":
                if item.text(0) == "Boîte de réception":
                    self.emails = self.controller.getAllStoreMail(self.inbox_to_try)
                    self.mail_list.clear()
                    self.showSelectedMails()
                if item.text(0) == "Éléments envoyés":
                    self.emails = self.controller.getAllStoreMail(self.sent_to_try)
                    self.mail_list.clear()
                    self.showSelectedMails()
                if item.text(0) == "Élements supprimés":
                    self.emails = self.controller.getAllStoreMail(self.deleted_to_try)
                    self.mail_list.clear()
                    self.showSelectedMails()
            else :
                if item.text(0) == "Boîte de réception":
                    for inbox in self.inbox_to_try:
                        self.emails = self.controller.getMailsFromAdress(item.parent().text(0),inbox)
                        if len(self.emails) > 0:
                            break
                    self.mail_list.clear()
                    self.showSelectedMails()
                if item.text(0) == "Éléments envoyés":
                    for sent in self.sent_to_try:
                        self.emails = self.controller.getMailsFromAdress(item.parent().text(0),sent)
                        if len(self.emails) > 0:
                            break
                    self.mail_list.clear()
                    self.showSelectedMails()
                if item.text(0) == "Élements supprimés":
                    for deleted in self.deleted_to_try:
                        self.emails = self.controller.getMailsFromAdress(item.parent().text(0),deleted)
                        if len(self.emails) > 0:
                            break
                    self.mail_list.clear()
                    self.showSelectedMails()
                if item.text(0) == "Spam":
                    for spam in self.spam_to_try:
                        self.emails = self.controller.getMailsFromAdress(item.parent().text(0),spam)
                        if len(self.emails) > 0:
                            break
                    self.mail_list.clear()
                    self.showSelectedMails()
        if item.childCount() > 0:
            if item.isExpanded():
                item.setExpanded(False)
            else:
                item.setExpanded(True)

    def show_menu(self):
        # Afficher le menu déroulant au-dessus du bouton
        self.menu.popup(self.button_trie.mapToGlobal(self.button_trie.rect().bottomLeft()))

    def populate_launch_mail_list(self):
        self.emails += self.controller.getAllStoreMail(self.inbox_to_try)

    def sortByRecentDate(self):
        self.intOrdreMails = 1
        # Trier les e-mails par date du plus récent au plus vieux
        self.emails = sorted(self.emails, key=lambda x: x.date, reverse=True)
        self.mail_list.clear()
        self.showSelectedMails()

    def sortByOldDate(self):
        self.intOrdreMails = 0
        # Trier les e-mails par date du plus vieux au plus récent
        self.emails = sorted(self.emails, key=lambda x: x.date)
        self.mail_list.clear()
        self.showSelectedMails()

    def showSelectedMails(self):
        #appliquer le trie croissant/décroissant
        if self.intOrdreMails == 1:
            self.emails = sorted(self.emails, key=lambda x: x.date, reverse=True)
        else:
            self.emails = sorted(self.emails, key=lambda x: x.date)

        # Ajouter les e-mails triés à la liste
        for email in self.emails:
            mail_item = CustomListWidgetItem()
            mail_item.setSender(email.get_sender())
            mail_item.setSubject(email.get_subject())
            try :
                mail_item.setIcon("vue/image/" + email.get_mail().split("@")[1].split(".")[0] + ".png")
            except :
                mail_item.setIcon("vue/image/email.png")

            mail_item.setDate(email.get_date())
            mail_item.setFont(QFont('Arial', 8))
            myQListWidgetItem = QListWidgetItem(self.mail_list)
            myQListWidgetItem.setSizeHint(mail_item.sizeHint())
            self.mail_list.addItem(myQListWidgetItem)
            self.mail_list.setItemWidget(myQListWidgetItem, mail_item)
            myQListWidgetItem.setData(Qt.UserRole, email.get_body())


    def display_mail_content(self, item):

        content = item.data(Qt.UserRole)
        self.central_widget = HtmlViewWidget()
        self.central_widget.setWindowTitle("Lecteur de Mail")
        self.central_widget.load_html(content)
        self.central_widget.show()

    def resize_to_half_screen(self):
        desktop = QApplication.desktop()
        screen_rect = desktop.screenGeometry()
        half_width = screen_rect.width() / 1.25
        half_height = screen_rect.height() / 1.25
        self.resize(int(half_width), int(half_height))

    def open_add_emails_window(self):
        self.add_emails_window = AddEmailsWidget(self.controller.getBdd())
        self.add_emails_window.email_added.connect(self.handle_new_email)
        self.add_emails_window.show()

    def handle_new_email(self, email, password, provider):
        self.add_emails_window.close()
        #création du widget de loading
        self.loadingWidget = LoadingWidget()
        self.loadingWidget.loadMovie()
        self.thread = RefreshWorker(self.controller,self.controller.parseAllEmailsFromAdress,email,password,Provider(provider).getProvider())
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(self.update_tree)
        self.thread.finished.connect(self.loadingWidget.close)
        self.thread.finished.connect(self.loadingWidget.deleteLater)
        
        self.thread.start()
        # Affichez le widget de chargement
        self.loadingWidget.show()
        
    def update_tree(self):
        self.customTreeWidget.update()
        self.loadingWidget.hide_loading()