from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QPushButton
from PyQt5.QtGui import QPixmap, QColor, QIcon
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt, QSize

class UserMain(QMainWindow):
    def __init__(self):
        super(UserMain, self).__init__()

        self.main_page = uic.loadUi('file_ui/user_main_menu.ui', self)

        
        self.set_icon()

        self.create_account = self.findChild(QPushButton, 'push_sparepart')
        self.create_account.clicked.connect(self.to_sparepart)

        self.show()

    def to_sparepart(self):
        self.main_page.close()
        self.sparepart_page = Sparepart()
        self.sparepart_page.show()
    
    def set_icon(self):
        self.label = self.findChild(QLabel, 'logo')
        pixmap = QPixmap('Pictures/image 2.png')
        self.label.setPixmap(pixmap)
        self.label.setScaledContents(True)

        self.push_sparepart = self.findChild(QPushButton, 'push_sparepart')
        self.push_sparepart.setIcon(QIcon("Pictures/sparepart.png"))
        self.push_sparepart.setIconSize(QSize(65, 65))

        self.push_reservation = self.findChild(QPushButton, 'push_reservation')
        self.push_reservation.setIcon(QIcon("Pictures/reservation.png"))
        self.push_reservation.setIconSize(QSize(90, 95))

        self.push_service_list = self.findChild(QPushButton, 'push_service_list')
        self.push_service_list.setIcon(QIcon("Pictures/list.png"))
        self.push_service_list.setIconSize(QSize(65, 65))
    
class Sparepart(QMainWindow):
    def __init__(self):
        super(Sparepart, self).__init__()

        self.sparepart_page = uic.loadUi('file_ui/sparepart_menu.ui', self)

        self.label = self.findChild(QLabel, 'logo_sparepart')
        pixmap = QPixmap('Pictures/sparepart.png')
        self.label.setPixmap(pixmap)
        self.label.setScaledContents(True)

        self.push_back = self.findChild(QPushButton, 'push_back')
        self.push_back.clicked.connect(self.to_user_main)

        self.show()

    def to_user_main(self):
        self.sparepart_page.close()
        self.user_main = UserMain()
        self.user_main.show()