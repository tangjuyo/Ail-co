from PySide6.QtWidgets import QWidget, QVBoxLayout, QListView,QHBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from vue.emailViewPage import emailViewPage
from vue.widget.customListModel import CustomListItemModel
from vue.widget.customListWidgetItem import CustomWidgetItem
from vue.widget.customEmailBandeau import CustomEmailBandeau

class rightMainWidget(QWidget):
    def __init__(self,controller):
        super().__init__()
        self.controller = controller
        self.layoutRight = QVBoxLayout()
        
        #bandeau spécifique des mails
        bandeau_mail = CustomEmailBandeau(self.controller)
        bandeau_mail.setFont(QFont('Arial', 8))
        self.layoutRight.addWidget(bandeau_mail)

        showHtmlLayout = QHBoxLayout()
        # Création de la vue de la liste des mails
        self.mail_view = QListView()
        self.mail_view.setUniformItemSizes(True)
        self.mail_view.clicked.connect(self.display_mail_content)
        showHtmlLayout.addWidget(self.mail_view,1)

        self.htlm_widget = emailViewPage()
        showHtmlLayout.addWidget(self.htlm_widget,3)

        self.layoutRight.addLayout(showHtmlLayout)

    def getLayout(self):
        return self.layoutRight

    def showSelectedMails(self, emails):
        # Création du modèle de la vue
        model = CustomListItemModel()

        # Ajout des données dans le modèle
        for index, row in emails.iterrows():
            # Création de l'élément avec des données
            mail_item = CustomWidgetItem()
            mail_item.setSender(row["sender"])
            mail_item.setSubject(row["subject"])
            try:
                mail_item.setIcon("vue/image/" + row["mail"].split("@")[1].split(".")[0] + ".png")
            except:
                mail_item.setIcon("vue/image/email.png")

            mail_item.setDate(row["date"])
            mail_item.setData(row["body"])
            # Ajout de l'élément au modèle
            model.items.append(mail_item)
        
        # Définition du modèle pour la vue
        self.mail_view.setModel(model)

    def display_mail_content(self, item):
        content = item.data(Qt.UserRole)
        self.htlm_widget.load_html(content)
        self.htlm_widget.show()