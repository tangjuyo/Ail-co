from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QComboBox
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import Qt

class AddEmailsWidget(QWidget):
    # Signal personnalisé pour envoyer les informations de l'adresse mail, du mot de passe et du fournisseur
    email_added = pyqtSignal(str, str, str)

    def __init__(self,bdd):
        super().__init__()
        self.setWindowTitle('Ajouter des adresses mails')
        self.setWindowFlags(self.windowFlags() | Qt.WindowCloseButtonHint)
        self.resize_to_half_screen()
        self.layout = QVBoxLayout()
        self.bdd = bdd

        # Zone de texte pour saisir l'adresse e-mail
        self.email_edit = QLineEdit()
        self.email_edit.setPlaceholderText("Adresse e-mail")
        self.layout.addWidget(self.email_edit)

        # Zone de texte pour saisir le mot de passe
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.password_edit.setPlaceholderText("Mot de passe")
        self.layout.addWidget(self.password_edit)

        # Menu déroulant pour sélectionner le fournisseur
        self.provider_combo = QComboBox()
        self.provider_combo.addItems(['gmail', 'outlook', 'orange'])
        self.layout.addWidget(self.provider_combo)

        # Bouton pour ajouter l'adresse e-mail
        self.add_button = QPushButton('Ajouter')
        self.add_button.clicked.connect(self.add_email)
        self.layout.addWidget(self.add_button)

        self.setLayout(self.layout)

    def add_email(self):
        email = self.email_edit.text()
        password = self.password_edit.text()
        provider = self.provider_combo.currentText()
        self.bdd.add_email_password(email,password)
        # Émet le signal avec les informations de l'adresse mail, du mot de passe et du fournisseur
        self.email_added.emit(email, password, provider)

    def resize_to_half_screen(self):
        desktop = QApplication.desktop()
        screen_rect = desktop.screenGeometry()
        half_width = screen_rect.width() / 1.75
        half_height = screen_rect.height() / 1.75
        self.resize(int(half_width), int(half_height))
