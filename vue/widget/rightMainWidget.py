from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget,QListWidgetItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from vue.emailViewPage import emailViewPage
from vue.widget.customListWidgetItem import CustomListWidgetItem 

class rightMainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layoutRight = QVBoxLayout() 
        # Liste des mails
        self.mail_list = QListWidget(self)
        self.mail_list.itemClicked.connect(self.display_mail_content)
        self.layoutRight.addWidget(self.mail_list)

    def getLayout(self):
        return self.layoutRight

    def showSelectedMails(self,emails):
        self.mail_list.clear()
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
            
    def display_mail_content(self, item):
        content = item.data(Qt.UserRole)
        self.central_widget = emailViewPage()
        self.central_widget.load_html(content)
        self.central_widget.show()