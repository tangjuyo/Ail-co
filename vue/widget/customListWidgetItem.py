from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QCheckBox 
from PySide6 import QtGui
from PySide6.QtCore import Qt 

class CustomWidgetItem:
    def __init__(self):
        self.sender = ""
        self.subject = ""
        self.icon_path = ""
        self.date = ""
        self.data = ""

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
        self.main_layout = QHBoxLayout()
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
    
    def setData(self, path):
        self.path = path
    
    def getData(self):
        return self.path
"""