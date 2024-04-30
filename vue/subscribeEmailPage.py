from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QComboBox, QFrame, QDialog, QDialogButtonBox
from PySide6.QtCore import Signal, Qt
from vue.widget.loadingWidget import LoadingWidget
from vue.widget.cTitleBar import CTitleBar
from models.jsonConfigs.readVariables import readVariables

class subscribeEmailPage(QDialog):
    # Signal personnalisé pour envoyer les informations de l'adresse mail, du mot de passe et du fournisseur
    email_added = Signal(str, str, str)
    thread_finished_signal = Signal()
    
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.Dialog)
        self.controller = controller
        
        layout = QVBoxLayout(self)
        layout.addWidget(CTitleBar(self, title=readVariables.lire_variable(self.__class__.__name__,"windowsTitle")))
        
        # Zone de texte pour saisir l'adresse e-mail
        self.email_edit = QLineEdit()
        self.email_edit.setPlaceholderText(readVariables.lire_variable(self.__class__.__name__,"hintAdressMail"))
        layout.addWidget(self.email_edit)

        # Zone de texte pour saisir le mot de passe
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.password_edit.setPlaceholderText(readVariables.lire_variable(self.__class__.__name__,"hintPassword"))
        layout.addWidget(self.password_edit)

        # Menu déroulant pour sélectionner le fournisseur
        self.provider_combo = QComboBox()
        self.provider_combo.addItems(['gmail', 'outlook', 'orange'])
        layout.addWidget(self.provider_combo)

        # Boutons OK et Annuler
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def accept(self):
        email = self.email_edit.text()
        password = self.password_edit.text()
        provider = self.provider_combo.currentText()
        self.controller.add_email_password(email, password)
        # Émet le signal avec les informations de l'adresse mail, du mot de passe et du fournisseur
        self.email_added.emit(email, password, provider)
        super().accept()

    def handle_new_email(self, email, password, provider):
        self.close()
        #création du widget de loading
        self.loadingWidget = LoadingWidget()
        self.loadingWidget.loadMovie()
        self.controller.addEmailsThread(self.loadingWidget,email,password,provider)
        # Affichez le widget de chargement
        self.loadingWidget.show()
