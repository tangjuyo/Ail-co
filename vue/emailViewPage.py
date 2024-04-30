from PySide6.QtWidgets import QVBoxLayout, QWidget, QApplication
from PySide6.QtWebEngineWidgets import QWebEngineView

class emailViewPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.resize_to_half_screen()

    def load_html(self, html_content):
        self.web_view.setHtml(html_content)

    def init_ui(self):
        layout = QVBoxLayout()
        # Affichage du contenu HTML
        self.web_view = QWebEngineView()
        layout.addWidget(self.web_view)
        self.setLayout(layout)

    def resize_to_half_screen(self):
        screen = QApplication.primaryScreen()
        screen_rect = screen.availableGeometry()
        half_width = screen_rect.width() / 1.5
        half_height = screen_rect.height() / 1.5
        self.resize(int(half_width), int(half_height))
        
