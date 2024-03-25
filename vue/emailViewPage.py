from PyQt5.QtWidgets import QVBoxLayout, QWidget, QApplication, QPushButton
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEnginePage
from PyQt5.QtCore import QUrl  

class emailViewPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.resize_to_half_screen()
        self.setWindowTitle("Lecteur de Mail")

    def load_html(self, html_content):
        self.web_view.setHtml(html_content)

    def init_ui(self):
        layout = QVBoxLayout()
        # Affichage du contenu HTML
        self.web_view = QWebEngineView()
        layout.addWidget(self.web_view)
        
        self.setLayout(layout)

    def resize_to_half_screen(self):
        desktop = QApplication.desktop()
        screen_rect = desktop.screenGeometry()
        half_width = screen_rect.width() / 1.5
        half_height = screen_rect.height() / 1.5
        self.resize(int(half_width), int(half_height))
