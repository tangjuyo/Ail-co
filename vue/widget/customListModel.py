from PySide6.QtCore import Qt, QModelIndex, QAbstractItemModel
from PySide6.QtGui import QIcon

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
                return item.sender
            elif index.column() == 1:
                return item.subject
            elif index.column() == 2:
                return item.date
            
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