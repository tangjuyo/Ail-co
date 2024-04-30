from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel,QApplication
from PySide6.QtCore import Qt
from PySide6.QtGui import QMovie
import sys
from models.jsonConfigs.readVariables import readVariables

class LoadingWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.resize_to_half_screen()

    def initUI(self):
        layout = QVBoxLayout()
        self.setWindowTitle(readVariables.lire_variable(self.__class__.__name__,"windowsTitle"))
        # QLabel pour afficher le texte
        self.loadingText = QLabel(readVariables.lire_variable(self.__class__.__name__,"loadingText"))
        self.loadingText.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.loadingText)

        # QLabel pour afficher le GIF de chargement
        self.loadingLabel = QLabel(self)
        self.loadingLabel.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.loadingLabel)
        self.setLayout(layout)
        
    def loadMovie(self):
        # Créer et configurer l'animation du GIF
        self.movie = QMovie("vue/image/loading.gif")
        self.loadingLabel.setMovie(self.movie)
        self.movie.start()

    def show_loading(self):
        self.show()

    def hide_loading(self):
        self.hide()

    def resize_to_half_screen(self):
        screen = QApplication.primaryScreen()
        screen_rect = screen.availableGeometry()
        half_width = screen_rect.width() / 5
        half_height = screen_rect.height() / 5
        self.resize(int(half_width), int(half_height))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = LoadingWidget()
    ex.show()
    sys.exit(app.exec_())