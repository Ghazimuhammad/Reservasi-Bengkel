from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QPushButton
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt

class UserMain(QMainWindow):
    def __init__(self):
        super(UserMain, self).__init__()

        self.main_page = uic.loadUi('file_ui/user_main_menu.ui', self)

        label = self.findChild(QLabel, 'label_5')
        pixmap = QPixmap('Pictures/image 2.png')
        label.setPixmap(pixmap)
        label.setScaledContents(True)

        self.create_account = self.findChild(QPushButton, 'push_sparepart')
        self.create_account.clicked.connect(self.to_sparepart)

        self.show()
    
    def to_sparepart(self):
        self.main_page.close()
        self.sparepart_page = Sparepart()
        self.sparepart_page.show()

class Sparepart(QMainWindow):
    def __init__(self):
        super(Sparepart, self).__init__()

        self.main_page = uic.loadUi('file_ui/sparepart_menu.ui', self)

        self.label = self.findChild(QLabel, 'logo')
        pixmap = QPixmap('Pictures/sparepart.jpeg')
        self.label.setPixmap(pixmap)
        # self.label.setStyleSheet("background-color: #2D2E43")
        # self.setStyleSheet("background-color: #2D2E43") 
        self.label.setScaledContents(True)
        self.show()
