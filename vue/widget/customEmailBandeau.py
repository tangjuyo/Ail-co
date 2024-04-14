from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QCheckBox,QToolButton,QMenu,QLineEdit
from PySide6.QtGui import QIcon, QPixmap
from models.configVar import configVar
from PySide6.QtCore import Qt

class CustomEmailBandeau(QWidget):
    def __init__(self, controller, parent=None):
        super(CustomEmailBandeau, self).__init__(parent)
        self.controller = controller
        # Layouts
        self.main_layout = QHBoxLayout()
        self.text_layout = QVBoxLayout()
        self.date_layout = QVBoxLayout()
        self.order = 0
        # Labels
        self.date_label = QLabel()

        # Add delete checkbox
        self.delete_checkbox = QCheckBox()
        self.main_layout.addWidget(self.delete_checkbox,0)    
        
        # Set up la recherche
        self.search_bar()
        
        # Bouton pour afficher options de trie
        self.button_trie = QToolButton(self)
        self.button_trie.setIcon(QIcon(QPixmap("vue/image/trie.png")))
        self.button_trie.clicked.connect(self.show_menu)

        # Add layouts to main layout
        self.main_layout.addWidget(self.button_trie,2)
        
        # Créer le menu déroulant du bouton de trie
        self.menu = QMenu(self)
        self.menu.addAction("Trier par date", self.sortByDate)
        self.menu.addAction("Trier par expéditeur", self.sortBySender)
        self.menu.addAction("Trier par sujet", self.sortBySubject)
        self.menu.addSeparator()
        self.menu.addAction("Ordre croissant", lambda: self.sortOrder(True))
        self.menu.addAction("Ordre décroissant", lambda: self.sortOrder(False))

        
        
        # Set up date layout
        self.date_layout.addWidget(self.button_trie, alignment=Qt.AlignRight)
        
        # Set main layout
        self.setLayout(self.main_layout)
        
        self.delete_checkbox.setStyleSheet('''
            padding: 10px;
        '''
        )
        self.date_label.setStyleSheet('''
            color: rgb(0, 0, 0);
            text-align: right;
        ''')
        
        # Path variable
        self.path = ""
    
    def show_menu(self):
        # Afficher le menu déroulant au-dessus du bouton
        self.menu.popup(self.button_trie.mapToGlobal(self.button_trie.rect().bottomLeft()))
    
    def search_bar(self):
        search_layout = QHBoxLayout()
        self.search_textbox = QLineEdit()
        self.search_textbox.setPlaceholderText("Rechercher")
        self.search_textbox.returnPressed.connect(self.handle_search)
        search_layout.addWidget(self.search_textbox)
        self.main_layout.addLayout(search_layout,1)
    
    def handle_search(self):
        self.controller.searchItem(self.search_textbox.text())
    
    
    def sortOrder(self,boolSort):
        configVar.update_variable("sortOrder",boolSort)
        
    def sortByDate(self):
        self.controller.sortByDate()
    def sortBySender(self):
        self.controller.sortBySender()
    def sortBySubject(self):
        self.controller.sortBySubject()