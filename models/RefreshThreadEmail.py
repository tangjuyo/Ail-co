from PyQt5.QtCore import QThread

class RefreshWorker(QThread):
    def __init__(self, controller, method=None, *args):
        super().__init__()
        self.controller = controller
        self.method = method
        self.args = args

    def run(self):
        if self.method:
            self.method(*self.args)