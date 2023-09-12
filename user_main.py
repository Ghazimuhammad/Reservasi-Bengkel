from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QPushButton, QScrollArea, QWidget, QFrame, QGridLayout, QVBoxLayout, QHBoxLayout, QComboBox
from PyQt5.QtGui import QPixmap, QColor, QIcon
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt, QSize, QRect
import firebase_admin
from firebase_admin import db
from cred import *

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
        self.insert_sparepart_menu()

        self.sparepart_page.Combobox.addItem("Car")
        self.sparepart_page.Combobox.addItem("MotorCycle")
        self.sparepart_page.Combobox.currentIndexChanged.connect(self.insert_sparepart_menu)

        self.show()

    def to_user_main(self):
        self.sparepart_page.close()
        self.user_main = UserMain()
        self.user_main.show()
    
    def insert_sparepart_menu(self):
        selected_item = self.sparepart_page.Combobox.currentText()
    
        if not selected_item:
            for i in reversed(range(self.sparepart_page.verticalLayout.count())):
                self.sparepart_page.verticalLayout.itemAt(i).widget().setParent(None)
        else:
            link = f"/Sparepart/{selected_item}"
            scrollable_layout = SparepartMenu(link)

            for i in reversed(range(self.sparepart_page.verticalLayout.count())):
                self.sparepart_page.verticalLayout.itemAt(i).widget().setParent(None)
            self.sparepart_page.verticalLayout.addWidget(scrollable_layout)


class SparepartMenu(QWidget):
    def __init__(self, link):
        super().__init__()
        
        self.link = link
        self.ref = db.reference(self.link)
        self.set_scroll()

    def button_clicked(self, index, increment, name):
        self.counters[index] += increment
        label = self.findChild(QLabel, f'label_{index}')
        if label is not None:
            label.setText("     " + str(self.counters[index]))
        for key, value in self.ref.get().items():
            if key == name:
                hold = value['stock'] - increment
                self.ref.child(key).update({'stock':hold})
        total_quantity = sum(self.counters[1:])
        total_price = sum(self.counters[i] * float(data.get(list(data.keys())[0], {}).get('price')) for i, data in enumerate(self.list_data, start=1))

        self.total_quantity.setText("          " + str(total_quantity))
        self.total_price.setText("          " + str(total_price) + 'k')

    def set_scroll(self):
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)

        content_widget = QWidget()
        scroll_area.setWidget(content_widget)
        scroll_area.verticalScrollBar().setStyleSheet("""
            QScrollBar:vertical {
                border: 2px solid #555555;
                background: #999999;
                width: 10px;
                background-color: rgb(80, 80, 122);
            }
            QScrollBar::handle:vertical {
                background: #555555;
                min-height: 20px;
                background-color: rgb(245, 154, 182);
            }
        """)

        content_layout = QGridLayout(content_widget)

        self.counters = []
        self.counters.append(0) 

        self.list_data = [{key:value} for key, value in self.ref.get().items()]

        label_name = QLabel('Name')
        content_layout.addWidget(label_name, 0, 0)
        label_name.setStyleSheet("color: white;")

        label_price = QLabel('Price')
        content_layout.addWidget(label_price, 0, 1)
        label_price.setStyleSheet("color: white;")

        label_count = QLabel("Count")
        content_layout.addWidget(label_count, 0, 3)
        label_count.setStyleSheet("color: white;")

        i = 1

        for data in self.list_data:
            label = QLabel(list(data.keys())[0])
            content_layout.addWidget(label, i, 0)
            label.setStyleSheet("color: white;")

            price = QLabel(str(data.get(list(data.keys())[0], {}).get('price')) + 'k')
            content_layout.addWidget(price, i, 1)
            price.setStyleSheet("color: white;")

            button_minus = QPushButton(f'-')
            content_layout.addWidget(button_minus, i, 2)

            self.counters.append(0) 
            count = QLabel("     0")
            content_layout.addWidget(count, i, 3)
            count.setObjectName(f'label_{i}')
            count.setStyleSheet("color: white;")

            button_plus = QPushButton(f'+')
            content_layout.addWidget(button_plus, i, 4)

            button_plus.clicked.connect(lambda checked, index=i, name=list(data.keys())[0]: self.button_clicked(index, 1, name))
            button_minus.clicked.connect(lambda checked, index=i, name=list(data.keys())[0]: self.button_clicked(index, -1, name))
            i += 1

        layout = QVBoxLayout(self)
        layout.addWidget(scroll_area, 9)
        Hbox = QWidget(self) 
        Hbox_layout = QHBoxLayout(Hbox)  
        self.quantity_label = QLabel("Total quantity")
        self.quantity_label.setStyleSheet("color: white;")
        Hbox_layout.addWidget(self.quantity_label)
        self.total_quantity = QLabel("          0")
        self.total_quantity.setStyleSheet("color: white;")
        Hbox_layout.addWidget(self.total_quantity)
        self.price_label = QLabel("Total price")
        self.price_label.setStyleSheet("color: white;")
        Hbox_layout.addWidget(self.price_label)
        self.total_price = QLabel("          0")
        self.total_price.setStyleSheet("color: white;")
        Hbox_layout.addWidget(self.total_price)

        layout.addWidget(scroll_area, 9)
        layout.addWidget(Hbox, 1) 
        self.setLayout(layout)