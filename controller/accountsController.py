from models.RefreshThreadEmail import RefreshWorker
from PySide6.QtWidgets import QWidget
from models.provider import Provider
from PySide6.QtCore import Signal

class accountsController(QWidget):
    add_email_thread_finished_signal = Signal()
    def __init__(self,accountManager):
        super().__init__()
        self.accountManager = accountManager