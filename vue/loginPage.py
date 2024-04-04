from PySide6.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout

class PasswordInputDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Enter Password")

        self.label = QLabel("Enter password:")
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.ok_button = QPushButton("OK")

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.password_edit)
        layout.addWidget(self.ok_button)

        self.ok_button.clicked.connect(self.accept)

        self.setLayout(layout)


    def setpassword(self,mdp):
        self.password_edit.setText(mdp)
    @property
    def password(self):
        return self.password_edit.text()
