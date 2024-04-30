from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QCheckBox 
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout
from PySide6.QtCore import Qt 
import os
class CustomWidgetItem (QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.sender = ""
        self.subject = ""
        self.icon_path = ""
        self.date = ""
        self.data = ""
        # Création des labels
        self.label1 = QLabel(self.subject)
        self.label1.setFont(QFont("Arial", 10, QFont.Bold))
        
        self.label2 = QLabel(self.sender)
        self.label3 = QLabel(self.date)
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

    def setDate(self, text):
        self.date = text

    def setSender(self, text):
        self.sender = text

    def setSubject(self, text):
        self.subject = text

    def setIcon(self, image_path):
        if os.path.exists(image_path) :
            self.icon_path = image_path
        else :
            raise ("erreur de path")

    def setData(self, data):
        self.data = data

    def getData(self):
        return self.data