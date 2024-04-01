from PySide6.QtCore import QThread

class RefreshWorker(QThread):
    def __init__(self, emailManager, method=None, *args):
        super().__init__()
        self.emailManager = emailManager
        self.method = method
        self.args = args

    def run(self):
        if self.method:
            self.method(*self.args)