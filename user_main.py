from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QPushButton
from PyQt5.QtGui import QPixmap, QColor, QIcon
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt, QSize

class UserMain(QMainWindow):
    def __init__(self):
        super(UserMain, self).__init__()

        self.main_page = uic.loadUi('file_ui/user_main_menu.ui', self)

        self.label = self.findChild(QLabel, 'logo')
        pixmap = QPixmap('Pictures/image 2.png')
        self.label.setPixmap(pixmap)
        self.label.setScaledContents(True)

        self.button_menu1 = self.findChild(QPushButton, 'push_sparepart')
        self.button_menu1.setIcon(QIcon("Pictures/sparepart.png"))
        self.button_menu1.setIconSize(QSize(65, 65))

        self.button_menu2 = self.findChild(QPushButton, 'push_reservation')
        self.button_menu2.setIcon(QIcon("Pictures/reservation.png"))
        self.button_menu2.setIconSize(QSize(90, 95))

        self.button_menu3 = self.findChild(QPushButton, 'push_service_list')
        self.button_menu3.setIcon(QIcon("Pictures/list.png"))
        self.button_menu3.setIconSize(QSize(65, 65))
        

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

        self.sparepart_page = uic.loadUi('file_ui/sparepart_menu.ui', self)

        self.label = self.findChild(QLabel, 'logo_sparepart')
        pixmap = QPixmap('Pictures/sparepart.png')
        self.label.setPixmap(pixmap)
        # self.label.setStyleSheet("background-color: #2D2E43")
        # self.setStyleSheet("background-color: #2D2E43") 
        self.label.setScaledContents(True)

        self.push_back = self.findChild(QPushButton, 'push_back')
        self.push_back.clicked.connect(self.to_user_main)

        self.show()

    def to_user_main(self):
        self.sparepart_page.close()
        self.user_main = UserMain()
        self.user_main.show()