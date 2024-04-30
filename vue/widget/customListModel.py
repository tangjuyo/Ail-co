from PySide6.QtCore import Qt, QModelIndex, QAbstractItemModel
from PySide6.QtGui import QIcon,QFont
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout

class CustomWidget(QWidget):
    def __init__(self,subjet,sender,date, parent=None):
        super().__init__(parent)

        # Création des labels
        self.label1 = QLabel(subjet)
        self.label1.setFont(QFont("Arial", 10, QFont.Bold))
        
        self.label2 = QLabel(sender)
        self.label3 = QLabel(date)
        self.label3.setAlignment(Qt.AlignRight)

        # Layouts
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label1)
        
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.label2)
        h_layout.addWidget(self.label3)
        
        self.layout.addLayout(h_layout)

        # Appliquer le layout au widget
        self.setLayout(self.layout)


class CustomListItemModel(QAbstractItemModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.items = []

    def rowCount(self, parent=QModelIndex()):
        return len(self.items)

    def columnCount(self, parent=QModelIndex()):
        # Nous avons une seule colonne, donc toujours retourner 1
        return 1
    
    def index(self, row, column, parent=QModelIndex()):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()
        return self.createIndex(row, column, self.items[row])

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < len(self.items)):
            return None
        
        item = self.items[index.row()]

        if role == Qt.DisplayRole:
            if index.column() == 0:
                widget = CustomWidget(item.subject,item.sender,item.date)
                #return widget.show()
                return str(item.subject) + "\n" + str(item.sender).split("<")[0] + "        " + str(item.date)
            
        if role == Qt.UserRole:
            return item.data
        
        # Pour afficher l'icône
        if role == Qt.DecorationRole:
            icon = QIcon(item.icon_path)
            return icon
        
        return None

    def parent(self, index):
        """
        Renvoie l'index du parent de l'élément spécifié par l'index donné.
        Pour un modèle plat comme le nôtre, nous retournons toujours un index invalide car nous n'avons pas de structure parent-enfant.
        """
        return QModelIndex()  # Retourne un QModelIndex invalide