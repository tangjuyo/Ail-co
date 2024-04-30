from PySide6.QtWidgets import QWidget, QTreeView, QHBoxLayout, QStackedWidget, QApplication, QTreeWidget,QTreeWidgetItem
from PySide6.QtGui import QFont,QIcon
import sys

class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.resize_to_half_screen()
        # Layout principal
        layout = QHBoxLayout(self)
        self.category_tree = QTreeWidget()

        # Affichage des paramètres à droite
        self.stacked_widget = QStackedWidget()

        # Ajouter les widgets au layout principal
        layout.addWidget(self.category_tree,1)
        layout.addWidget(self.stacked_widget,3)

        # Initialiser les catégories de paramètres
        self.init_settings()
        
    def init_settings(self):
    
        self.init_topLvl_settings("Général","vue/image/settings.png")


    def init_topLvl_settings(self,nameCategorie,categories):
        # Créer le nœud principal "Général"
        general_mail_tree_widget = QTreeWidgetItem()
        general_mail_tree_widget.setText(0, nameCategorie)
        font = QFont()
        font.setBold(True)
        general_mail_tree_widget.setFont(0, font)
        self.category_tree.addTopLevelItem(general_mail_tree_widget)

        for category_name in categories:
            category_item = QTreeWidgetItem()
            category_item.setText(0, category_name)
            general_mail_tree_widget.addChild(category_item)

    def resize_to_half_screen(self):
        screen = QApplication.primaryScreen()
        screen_rect = screen.availableGeometry()
        half_width = screen_rect.width() / 1.5
        half_height = screen_rect.height() / 1.5
        self.resize(int(half_width), int(half_height))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    settings_page = SettingsPage()
    settings_page.show()
    sys.exit(app.exec())
