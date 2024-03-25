from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QListWidget, QListWidgetItem, QPushButton,QHBoxLayout,QToolButton,QMenu
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont,QIcon, QPixmap
from vue.subscribeEmailPage import subscribeEmailPage
from vue.widget.customListWidgetItem import CustomListWidgetItem 
from vue.emailViewPage import emailViewPage
from vue.widget.loadingWidget import LoadingWidget
from vue.widget.customTreeWidget import CustomTreeWidget
from vue.widget.LeftMainWidget import LeftMainWidget
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

        # Liste des mails
        self.mail_list = QListWidget(self)
        self.mail_list.itemClicked.connect(self.display_mail_content)
        
        
        #barre latérale de gauche
        self.left_panel = LeftMainWidget(controller,self.emails,self.showSelectedMails)
        self.layout.addLayout(self.left_panel.getCustomTree().layout)
        
        #barre latérale de droite
        layoutRight = QVBoxLayout()
        
        
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
        
        # Ajout de la liste des mails au layout
        layoutRight.addWidget(self.mail_list)
        #ajout layout de droite à la vue
        self.layout.addLayout(layoutRight)
        
        self.layout.setStretchFactor(self.left_panel,2)
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

    def show_menu(self):
        # Afficher le menu déroulant au-dessus du bouton
        self.menu.popup(self.button_trie.mapToGlobal(self.button_trie.rect().bottomLeft()))

    def sortByRecentDate(self):
        self.intOrdreMails = 1
        # Trier les e-mails par date du plus récent au plus vieux
        self.emails = sorted(self.emails, key=lambda x: x.date, reverse=True)
        self.mail_list.clear()
        self.showSelectedMails(self.emails)

    def sortByOldDate(self):
        self.intOrdreMails = 0
        # Trier les e-mails par date du plus vieux au plus récent
        self.emails = sorted(self.emails, key=lambda x: x.date)
        self.mail_list.clear()
        self.showSelectedMails()

    def showSelectedMails(self,emails):
        self.mail_list.clear()
        self.emails = emails
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
        self.central_widget = emailViewPage()
        self.central_widget.load_html(content)
        self.central_widget.show()

    def resize_to_half_screen(self):
        desktop = QApplication.desktop()
        screen_rect = desktop.screenGeometry()
        half_width = screen_rect.width() / 1.25
        half_height = screen_rect.height() / 1.25
        self.resize(int(half_width), int(half_height))

    def open_add_emails_window(self):
        self.add_emails_window = subscribeEmailPage(self.controller)
        self.add_emails_window.email_added.connect(self.add_emails_window.handle_new_email)
        self.add_emails_window.thread_finished_signal.connect(self.left_panel.update_tree)
        self.add_emails_button
        self.add_emails_window.show()