from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow

class AdminMain(QMainWindow):
    def __init__(self):
        super(AdminMain, self).__init__()

        self.main_page = uic.loadUi('file_ui/admin_main_menu.ui', self)

        self.show()