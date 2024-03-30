from PyQt5.QtWidgets import QWidget,QPushButton,QHBoxLayout,QToolButton,QMenu,QLineEdit
from PyQt5.QtGui import QIcon, QPixmap
from vue.widget.loadingWidget import LoadingWidget
from vue.subscribeEmailPage import subscribeEmailPage

class bandeauWidget(QWidget):
    def __init__(self,controller):
        super().__init__()
        self.controller = controller
        self.bandeauLayout = QHBoxLayout()
        self.search_bar()
        # Bouton pour refresh les mails
        self.button_refresh = QToolButton(self)
        self.button_refresh.setIcon(QIcon(QPixmap("vue/image/refresh.png")))
        self.button_refresh.clicked.connect(self.refresh_mails)
        self.bandeauLayout.addWidget(self.button_refresh)

        # Bouton pour ouvrir l'interface AddEmailsWidget
        self.add_emails_button = QPushButton('Ajouter des adresses mails')
        self.add_emails_button.clicked.connect(self.open_add_emails_window)
        self.bandeauLayout.addWidget(self.add_emails_button)

        # Bouton pour afficher options de trie
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
    
    def search_bar(self):
        search_layout = QHBoxLayout()
        self.search_textbox = QLineEdit()
        self.search_textbox.setPlaceholderText("Rechercher")
        self.search_textbox.returnPressed.connect(self.handle_search)
        search_layout.addWidget(self.search_textbox)
        self.bandeauLayout.addLayout(search_layout)
    
    def handle_search(self):
        self.controller.searchItem(self.search_textbox.text())
        
    def refresh_mails(self):
        #création du widget de loading
        self.loadingWidget = LoadingWidget()
        self.loadingWidget.loadMovie()
        self.controller.refreshEmailsThread(self.loadingWidget)
        # Affichez le widget de chargement
        self.loadingWidget.show()
    
    def open_add_emails_window(self):
        self.add_emails_window = subscribeEmailPage(self.controller)
        self.add_emails_window.email_added.connect(self.add_emails_window.handle_new_email)
        self.add_emails_window.show()
        
    def sortByRecentDate(self):
        pass

    def sortByOldDate(self):
        pass
        
    def show_menu(self):
        # Afficher le menu déroulant au-dessus du bouton
        self.menu.popup(self.button_trie.mapToGlobal(self.button_trie.rect().bottomLeft()))