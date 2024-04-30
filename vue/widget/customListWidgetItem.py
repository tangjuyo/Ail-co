from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QCheckBox 
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout
from PySide6.QtCore import Qt 

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
        self.icon_path = image_path

    def setData(self, data):
        self.data = data

    def getData(self):
        return self.data
"""
class CustomWidgetItem(QWidget):
    def __init__(self, parent=None):
        super(CustomWidgetItem, self).__init__(parent)
        
        # Layouts
        self.main_layout = QHBoxLayout(self)
        self.text_layout = QVBoxLayout()
        self.date_layout = QVBoxLayout()
        
        # Labels
        self.icon_label = QLabel()
        self.sender_label = QLabel()
        self.subject_label = QLabel()
        self.date_label = QLabel()

        # Add delete checkbox
        self.delete_checkbox = QCheckBox()
        self.main_layout.addWidget(self.delete_checkbox,0)    
        
        # Set up text layout
        self.text_layout.addWidget(self.sender_label)
        self.text_layout.addWidget(self.subject_label)
        
        # Set up date layout
        self.date_layout.addWidget(self.date_label, alignment=Qt.AlignRight)
        
        # Add layouts to main layout
        self.main_layout.addWidget(self.icon_label,0)
        self.main_layout.addLayout(self.text_layout,1)
        self.main_layout.addLayout(self.date_layout,2)
        
        # Set main layout
        self.setLayout(self.main_layout)
        
        self.delete_checkbox.setStyleSheet('''
            padding: 10px;
        '''
        )
        # Set style sheet
        self.sender_label.setStyleSheet('''
            color: rgb(0, 0, 255);
        ''')
        self.subject_label.setStyleSheet('''
            color: rgb(255, 0, 0);
        ''')
        self.date_label.setStyleSheet('''
            color: rgb(0, 0, 0);
            text-align: right;
        ''')
        
        # Path variable
        self.path = ""
            
    def setDate(self, text):
        self.date_label.setText(text)
    
    def setSender(self, text):
        self.sender_label.setText(text)
    
    def setSubject(self, text):
        self.subject_label.setText(text)
    
    def setIcon(self, image_path):
        self.icon_label.setPixmap(QtGui.QPixmap(image_path))
        self.icon_label.setScaledContents(True)
    
    def setData(self, path):
        self.path = path
        
    def getDate(self):
        return self.date_label.text
    
    def getSender(self):
        return self.sender_label.text
    
    def getSubject(self):
        return self.subject_label.text
    
    def getIcon(self):
        return self.icon_label
    
    def getData(self):
        return self.path
"""