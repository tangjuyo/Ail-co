from PySide6.QtWidgets import QWidget, QVBoxLayout, QListView
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from vue.emailViewPage import emailViewPage
from vue.widget.customListModel import CustomListItemModel
from vue.widget.customListWidgetItem import CustomWidgetItem
from vue.widget.customEmailBandeau import CustomEmailBandeau
    
class rightMainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layoutRight = QVBoxLayout()
        
        #bandeau spécifique des mails
        bandeau_mail = CustomEmailBandeau()
        bandeau_mail.setFont(QFont('Arial', 8))
        self.layoutRight.addWidget(bandeau_mail)
        # Création de la vue de la liste des mails
        self.mail_view = QListView()
        self.mail_view.setUniformItemSizes(True)
        self.mail_view.clicked.connect(self.display_mail_content)
        self.layoutRight.addWidget(self.mail_view)

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

    """
    def showSelectedMails(self,emails):
        self.mail_list.clear()
        self.mail_list.setUniformItemSizes(True)
        self.emails = emails
        # Ajouter les e-mails triés à la liste
        for index, row in self.emails.iterrows():
            mail_item = CustomListWidgetItem()
            mail_item.setSender(row["sender"])
            mail_item.setSubject(row["subject"])
            try :
                mail_item.setIcon("vue/image/" + row["mail"].split("@")[1].split(".")[0] + ".png")
            except :
                mail_item.setIcon("vue/image/email.png")

            mail_item.setDate(row["date"])
            mail_item.setFont(QFont('Arial', 8))
            myQListWidgetItem = QListWidgetItem(self.mail_list)
            myQListWidgetItem.setSizeHint(mail_item.sizeHint())
            self.mail_list.addItem(myQListWidgetItem)
            self.mail_list.setItemWidget(myQListWidgetItem, mail_item)
            myQListWidgetItem.setData(Qt.UserRole, row["body"])
    """
    def display_mail_content(self, item):
        content = item.data(Qt.UserRole)
        self.central_widget = emailViewPage()
        self.central_widget.load_html(content)
        self.central_widget.show()