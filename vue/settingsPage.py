import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTabWidget, QGridLayout, QLabel, QLineEdit, QCheckBox, QComboBox,QPushButton
from PySide6.QtGui import QIntValidator, QDoubleValidator

class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Settings")
        self.setFixedSize(400, 600)

        layout = QVBoxLayout()

        tab_widget = QTabWidget()
        layout.addWidget(tab_widget)

        # Create tabs
        accounts_tab = QWidget()
        accounts_tab.setLayout(QGridLayout())
        tab_widget.addTab(accounts_tab, "Accounts")

        compose_tab = QWidget()
        compose_tab.setLayout(QGridLayout())
        tab_widget.addTab(compose_tab, "Compose")

        # Accounts tab
        accounts_tab_layout = accounts_tab.layout()

        # Add account pattern
        for i, account in enumerate(["Email 1", "Email 2", "Email 3"]):
            account_layout = QGridLayout()
            accounts_tab_layout.addLayout(account_layout, i, 0, 1, 2)

            account_label = QLabel("Account " + str(i + 1) + ":")
            account_layout.addWidget(account_label, 0, 0)

            email_edit = QLineEdit()
            email_edit.setText(account)
            email_edit.setStyleSheet("color:white;")
            #email_edit.setPlaceholderText("Email address")
            account_layout.addWidget(email_edit, 1, 0)

            password_edit = QLineEdit()
            password_edit.setEchoMode(QLineEdit.Password)
            account_layout.addWidget(password_edit, 2, 0)

            server_edit = QLineEdit()
            server_edit.setPlaceholderText("Server address")
            account_layout.addWidget(server_edit, 3, 0)

            port_edit = QLineEdit()
            port_edit.setPlaceholderText("Port number")
            port_edit.setValidator(QIntValidator())
            account_layout.addWidget(port_edit, 4, 0)

        # Compose tab
        compose_tab_layout = compose_tab.layout()

        # Add compose pattern
        for i, compose_setting in enumerate(["Font size", "Line spacing", "Theme"]):
            compose_layout = QGridLayout()
            compose_tab_layout.addLayout(compose_layout, i, 0, 1, 2)

            setting_label = QLabel(compose_setting + ":")
            compose_layout.addWidget(setting_label, 0, 0)

            edit = QLineEdit()
            edit.setPlaceholderText(compose_setting)
            compose_layout.addWidget(edit, 1, 0)

            self.add_button(compose_tab_layout, compose_layout, i)

        self.setLayout(layout)
    
    def add_button(self, parent_layout, child_layout, index):
        button = QPushButton("Add")
        child_layout.addWidget(button, index + 1, 1)
        button.clicked.connect(lambda: self.add_account(child_layout, index))

    def add_account(self, layout, index):
        account_layout = QGridLayout()
        layout.insertLayout(index, account_layout)

        account_label = QLabel("Account " + str(index + 1) + ":")
        account_layout.addWidget(account_label, 0, 0)

        email_edit = QLineEdit()
        email_edit.setPlaceholderText("Email address")
        account_layout.addWidget(email_edit, 1, 0)

        password_edit = QLineEdit()
        password_edit.setEchoMode(QLineEdit.Password)
        account_layout.addWidget(password_edit, 2, 0)

        server_edit = QLineEdit()
        server_edit.setPlaceholderText("Server address")
        account_layout.addWidget(server_edit, 3, 0)

        port_edit = QLineEdit()
        port_edit.setPlaceholderText("Port number")
        port_edit.setValidator(QIntValidator())
        account_layout.addWidget(port_edit, 4, 0)

        self.accounts.append({"email": email_edit.text(), "password": password_edit.text(), "server": server_edit.text(), "port": port_edit.text()})


if __name__ == "__main__":
    app = QApplication(sys.argv)
    settings_page = SettingsPage()
    settings_page.show()
    sys.exit(app.exec_())

