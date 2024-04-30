from PySide6.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout
from models.jsonConfigs.readVariables import readVariables

class PasswordInputDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(readVariables.lire_variable(self.__class__.__name__,"windowsTitle"))

        self.passwordLabel = QLabel(readVariables.lire_variable(self.__class__.__name__,"passwordLabel"))
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.ok_button = QPushButton("OK")

        layout = QVBoxLayout()
        layout.addWidget(self.passwordLabel)
        layout.addWidget(self.password_edit)
        layout.addWidget(self.ok_button)

        self.ok_button.clicked.connect(self.accept)

        self.setLayout(layout)


    def setpassword(self,mdp):
        self.password_edit.setText(mdp)

    @property
    def password(self):
        return self.password_edit.text()
