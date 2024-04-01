from PySide6.QtWidgets import QVBoxLayout,QTreeWidget,QTreeWidgetItem,QWidget,QSizePolicy
from PySide6.QtGui import QFont,QIcon
from PySide6.QtCore import Qt

class CustomTreeWidget(QWidget):
    def __init__ (self,controller, parent = None):
        super(CustomTreeWidget, self).__init__(parent)
        self.setStyleSheet("background-color: #333333; color: white;")
        self.controller = controller
        #barre du haut
        self.layout = QVBoxLayout()
        # Arbre des catégories d'e-mails
        self.category_tree = QTreeWidget()
        self.category_tree.setStyleSheet("QTreeWidget::item { padding: 3px;  font-size: 50pt;}")
        self.category_tree.setHeaderHidden(True)
        self.category_tree.setColumnCount(2)
        self.category_tree.setColumnWidth(0,int(self.frameSize().width()/2.77))
        #set de la taille au minimum possible pour ne pas prendre de la size inutile
        self.category_tree.setColumnWidth(1,1)
        self.createAllTree()

    def createAllTree(self):
        # Définir le padding avec une feuille de style CSS
        
        self.layout.addWidget(self.category_tree)

        #création branche générale
        self.general_Tree()
        #création de l'arbre de chaque adresse
        for mail in self.controller.get_all_email_addresses():
            self.email_branch_tree(mail)

        self.category_tree.setExpandsOnDoubleClick(False)
        self.category_tree.expandAll()
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.category_tree.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def general_Tree(self):
        # Créer le nœud principal "Général"
        general_mail_tree_widget = QTreeWidgetItem()
        general_mail_tree_widget.setIcon(0, QIcon("vue/image/favorite.png"))
        general_mail_tree_widget.setText(0, "Général")
        font = QFont()
        font.setBold(True)
        general_mail_tree_widget.setFont(0, font)
        self.category_tree.addTopLevelItem(general_mail_tree_widget)

        # Définir les catégories avec leurs icônes et comptages
        categories = [
            ("Boîte de réception", "vue/image/inbox.png"),
            ("Éléments envoyés", "vue/image/send.png"),
            ("Éléments supprimés", "vue/image/delete.png")
        ]

        for category_name, icon_path in categories:
            category_item = QTreeWidgetItem()
            category_item.setIcon(0, QIcon(icon_path))
            category_item.setText(0, category_name)
            count = self.controller.count_all_emails(category_name)
            category_item.setText(1, str(count))
            general_mail_tree_widget.addChild(category_item)

    def email_branch_tree(self, mail):
        # Créer le nœud principal
        mail_tree_widget = QTreeWidgetItem()
        mail_tree_widget.setIcon(0, QIcon("vue/image/favorite.png"))
        mail_tree_widget.setText(0, mail)
        font = QFont()
        font.setBold(True)
        mail_tree_widget.setFont(0, font)

        # Définir les catégories avec leurs icônes et comptages
        categories = [
            ("Boîte de réception", "vue/image/inbox.png"),
            ("Éléments envoyés", "vue/image/send.png"),
            ("Éléments supprimés", "vue/image/delete.png"),
            ("Spam", "vue/image/spam.png")
        ]

        for category_name, icon_path in categories:
            category_item = QTreeWidgetItem()
            category_item.setIcon(0, QIcon(icon_path))
            category_item.setText(0, category_name)
            count = self.controller.count_emails_in_mailbox_folder(mail, category_name)
            category_item.setText(1, str(count))
            mail_tree_widget.addChild(category_item)

        # Ajouter le nœud principal à l'arbre
        self.category_tree.addTopLevelItem(mail_tree_widget)
        
    def getCategory_tree(self):
        return self.category_tree
    
    def update(self):
        print(len(self.controller.getLoadedMails()))
        self.category_tree.clear()
        self.createAllTree()