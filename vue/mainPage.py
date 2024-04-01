from PySide6.QtWidgets import QApplication, QWidget,QHBoxLayout, QVBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QScreen
from vue.widget.leftMainWidget import leftMainWidget
from vue.widget.rightMainWidget import rightMainWidget
from vue.widget.bandeauWidget import bandeauWidget
from vue.widget.cTitleBar import CTitleBar

class MailListWidget(QWidget):
    
    def __init__(self,mailListController):
        super().__init__()
        self.resize_to_full_screen()  # Redimensionne la fenêtre à l'écran entier
        self.mailListController = mailListController
        self.emails = []
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        layout = QVBoxLayout(self)
        layout.addWidget(CTitleBar(self, title='AilEco',parent=True))
        #barre latérale de gauche
        self.left_panel = leftMainWidget(self.mailListController,self.emails,self.updateMailsView)
        self.mailListController.add_email_thread_finished_signal.connect(self.updateTreeView)
        # Partie droite
        self.right_panel = rightMainWidget()
        # Bandeau principal
        self.header_widget = bandeauWidget(self.mailListController)
        layout.addLayout(self.header_widget.bandeauLayout)
        
        
        mainLayout = QHBoxLayout()
        mainLayout.addLayout(self.left_panel.getCustomTree().layout)
        mainLayout.addLayout(self.right_panel.layoutRight)
        
        # Ajouter le layout du reste de la fenêtre au layout principal
        layout.addLayout(mainLayout)

        #définir la size du panel de gauche et de droite
        layout.setStretchFactor(self.left_panel,1)
        layout.setStretchFactor(self.right_panel,3)
        
        #set le layout principal
        self.setLayout(layout)
        
    def updateTreeView(self):
        self.left_panel.update_tree()
        
    def updateMailsView(self,emails):
        self.right_panel.showSelectedMails(emails)
    
    def resize_to_full_screen(self):
        screen = QApplication.primaryScreen()
        screen_rect = screen.availableGeometry()
        half_width = screen_rect.width()
        half_height = screen_rect.height()
        self.resize(int(half_width), int(half_height))
