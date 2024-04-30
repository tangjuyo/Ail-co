from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QCheckBox,QToolButton,QMenu,QLineEdit
from PySide6.QtGui import QIcon, QPixmap
from models.jsonConfigs.configVar import configVar
from PySide6.QtCore import Qt
from models.jsonConfigs.readVariables import readVariables

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
        self.button_trie.setIcon(QIcon(QPixmap("data/image/trie.png")))
        self.button_trie.clicked.connect(self.show_menu)

        # Add layouts to main layout
        self.main_layout.addWidget(self.button_trie,2)
        
        # Créer le menu déroulant du bouton de trie
        self.menu = QMenu(self)
        self.menu.addAction(readVariables.lire_variable(self.__class__.__name__,"sortDate"), self.sortByDate)
        self.menu.addAction(readVariables.lire_variable(self.__class__.__name__,"sortSender"), self.sortBySender)
        self.menu.addAction(readVariables.lire_variable(self.__class__.__name__,"sortSubject"), self.sortBySubject)
        self.menu.addSeparator()
        self.menu.addAction(readVariables.lire_variable(self.__class__.__name__,"ascendingOrder"), lambda: self.sortOrder(True))
        self.menu.addAction(readVariables.lire_variable(self.__class__.__name__,"descendingOrder"), lambda: self.sortOrder(False))

        
        
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
        self.searchTextbox = QLineEdit()
        self.searchTextbox.setPlaceholderText(readVariables.lire_variable(self.__class__.__name__,"searchTextbox"))
        self.searchTextbox.returnPressed.connect(self.handle_search)
        search_layout.addWidget(self.searchTextbox)
        self.main_layout.addLayout(search_layout,1)
    
    def handle_search(self):
        self.controller.searchItem(self.searchTextbox.text())
    
    
    def sortOrder(self,boolSort):
        configVar.update_variable("sortOrder",boolSort)
        
    def sortByDate(self):
        self.controller.sortByDate()
    def sortBySender(self):
        self.controller.sortBySender()
    def sortBySubject(self):
        self.controller.sortBySubject()