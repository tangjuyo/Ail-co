from PySide6.QtWidgets import QWidget,QPushButton,QHBoxLayout,QToolButton
from PySide6.QtGui import QIcon, QPixmap
from vue.widget.loadingWidget import LoadingWidget
from vue.subscribeEmailPage import subscribeEmailPage
from models.jsonConfigs.readVariables import readVariables
class bandeauWidget(QWidget):
    def __init__(self,controller):
        super().__init__()
        self.controller = controller
        self.bandeauLayout = QHBoxLayout()
        # Bouton pour refresh les mails
        self.button_refresh = QToolButton(self)
        self.button_refresh.setIcon(QIcon(QPixmap("vue/image/refresh.png")))
        self.button_refresh.clicked.connect(self.refresh_mails)
        self.bandeauLayout.addWidget(self.button_refresh)

        # Bouton pour ouvrir l'interface AddEmailsWidget
        self.add_emails_button = QPushButton(readVariables.lire_variable(self.__class__.__name__,"addEmailsText"))
        self.add_emails_button.clicked.connect(self.open_add_emails_window)
        self.bandeauLayout.addWidget(self.add_emails_button)
        
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
        

    