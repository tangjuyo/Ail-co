import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel,QApplication
from PyQt5.QtCore import Qt,pyqtSignal
from PyQt5.QtGui import QMovie

class LoadingWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.resize_to_half_screen()

    def initUI(self):
        layout = QVBoxLayout()
        self.setWindowTitle("Chargement de vos mails...")


        # QLabel pour afficher le texte
        self.textLabel = QLabel("Chargement de vos mails...")
        self.textLabel.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.textLabel)

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
        desktop = QApplication.desktop()
        screen_rect = desktop.screenGeometry()
        half_width = screen_rect.width() / 5
        half_height = screen_rect.height() / 5
        self.resize(int(half_width), int(half_height))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = LoadingWidget()
    ex.show()
    sys.exit(app.exec_())