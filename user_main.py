import json, requests
from datetime import datetime

from PyQt5 import uic
from PyQt5.QtWidgets import (QMainWindow, QPushButton, QScrollArea, 
                             QLabel, QLineEdit, QComboBox, 
                             QGridLayout, QSizePolicy, QVBoxLayout,
                             QHBoxLayout, QTableWidget, QTableWidgetItem,
                             QWidget, QMessageBox, QDateTimeEdit)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QSize, QDate, QDateTime, QTime
from user_widget import SparepartWidget, ConfirmationWidget

from firebase_admin import db
from cred import *



class UserMain(QMainWindow):
    def __init__(self, account):
        super(UserMain, self).__init__()
        self.account = account
        self.setup_ui()
        self.set_icon()
        self.show()

    def setup_ui(self):
        self.main_page = uic.loadUi('file_ui/user_main_menu.ui', self)
        self.create_account = self.findChild(QPushButton, 'push_sparepart')
        self.create_account.clicked.connect(self.to_sparepart)
        self.main_page.push_reservation.clicked.connect(self.to_reservation)
        self.main_page.push_service_list.clicked.connect(self.to_service_list)

    def to_sparepart(self):
        self.navigate_to(SparepartMenu(self.account))

    def to_reservation(self):
        self.navigate_to(ReservationMenu(self.account))

    def to_service_list(self):
        self.navigate_to(ServiceListMenu(self.account))
    
    def navigate_to(self, window):
        if hasattr(self, 'main_page'):
            self.main_page.close()
        self.window = window
        self.window.show()
    
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




class SparepartMenu(QMainWindow):
    def __init__(self, account):
        super(SparepartMenu, self).__init__()
        self.account = account
        self.setup_ui()
        self.show()
    
    def setup_ui(self):
        self.sparepart_menu = uic.loadUi('file_ui/sparepart_menu.ui', self)
        self.label = self.findChild(QLabel, 'logo_sparepart')
        pixmap = QPixmap('Pictures/sparepart.png')
        self.label.setPixmap(pixmap)
        self.label.setScaledContents(True)
        self.sparepart_menu.push_back.clicked.connect(self.to_user_main)
        self.sparepart_menu.Combobox.addItems(["Car", 'MotorCycle'])
        self.beginning = True
        if self.beginning:
            self.scrollable_layout = SparepartWidget('/Sparepart/Car')
            self.sparepart_menu.verticalLayout.addWidget(self.scrollable_layout)
            self.beginning = False
        self.sparepart_menu.Combobox.currentIndexChanged.connect(self.insert_sparepart_menu)

        self.sparepart_menu.push_next.clicked.connect(self.to_confirmation)

    def to_user_main(self):
        self.navigate_to(UserMain(self.account))

    def to_confirmation(self):
        self.navigate_to(ConfirmationPage(self.scrollable_layout.get_data_buy(), self.account))

    def navigate_to(self, window):
        if hasattr(self, 'sparepart_menu'):
            self.sparepart_menu.close()
        self.window = window
        self.window.show()

    def insert_sparepart_menu(self):
        selected_item = self.sparepart_menu.Combobox.currentText()
        self.link = f"/Sparepart/{selected_item}"
        for i in reversed(range(self.sparepart_menu.verticalLayout.count())):
            self.sparepart_menu.verticalLayout.itemAt(i).widget().setParent(None)
        self.scrollable_layout = SparepartWidget(self.link)
        self.sparepart_menu.verticalLayout.addWidget(self.scrollable_layout)
    




class ReservationMenu(QMainWindow):
    def __init__(self, account):
        super(ReservationMenu, self).__init__()
        self.account = account
        self.setup_ui()

        self.show()
    
    def setup_ui(self):
        self.reservation_page = uic.loadUi('file_ui/reservation.ui', self)
        self.ref = db.reference("/Login")

        self.name = self.findChild(QLineEdit, 'name_input')
        self.handphone = self.findChild(QLineEdit, 'phone_input')
        self.reservation_page.type_input.addItem("Car")
        self.reservation_page.type_input.addItem("Motorcycle")
        self.reservation_page.type_input.currentIndexChanged.connect(self.insert_type)
        self.reservation_page.push_back.clicked.connect(self.to_user_main)
        current_date = QDateTime.currentDateTime()
        max_time = QTime(19, 59, 59)
        self.reservation_page.date_input.setDateTime(current_date)
        self.reservation_page.date_input.setMinimumDateTime(current_date)
        self.reservation_page.date_input.setMaximumDateTime(QDateTime(current_date.date(), max_time))
        self.reservation_page.date_input.editingFinished.connect(self.get_date)
        self.reservation_page.push_booking.clicked.connect(self.booking)

    def to_user_main(self):
        if hasattr(self, 'reservation_page'):
            self.reservation_page.close()
        self.user_main = UserMain(self.account).show()

    def get_date(self):
        date_time = self.reservation_page.date_input.dateTime().date()
        date = date_time.toPyDate()
        self.dt = datetime(date.year, date.month, date.day, date.hour, date.minute, date.second)

    def insert_type(self):
        selected_type = self.reservation_page.type_input.currentText()
        link = f"/ServiceList/{selected_type}"
        services = db.reference(link).get()
        list_service = []
        for service in services.keys():
            list_service.append(service)
        for i in reversed(range(self.reservation_page.horizontalLayout.count())):
            self.reservation_page.horizontalLayout.itemAt(i).widget().setParent(None)
        self.combo = QComboBox(self)
        self.combo.addItems(list_service)
        self.reservation_page.horizontalLayout.addWidget(self.combo)

    def booking(self):
        ref = db.reference("/Booking")
        self.selected_service = self.combo.currentText()
        print(self.dt)
        data_booking = {self.account: 
                        {str(self.dt): {'service': self.selected_service
                        }}}
        ref.update(data_booking)





class ServiceListMenu(QMainWindow):
    def __init__(self, account):
        super(ServiceListMenu, self).__init__()
        self.account = account
        self.setup_ui()

        self.show()

    def setup_ui(self):
        self.servicelist_menu = uic.loadUi('file_ui/service_list.ui', self)
        self.servicelist_menu.push_back.clicked.connect(self.to_user_main)
        self.servicelist_menu.Combobox.addItems(["Car", 'Motorcycle'])
        beginning = True
        if beginning:
            self.link = '/ServiceList/Car'
            self.scrollable_layout = self.list_service()
            self.servicelist_menu.verticalLayout.addWidget(self.scrollable_layout)
            beginning = False
        self.servicelist_menu.Combobox.currentIndexChanged.connect(self.get_activated)

    def to_user_main(self):
        if hasattr(self, 'servicelist_menu'):
            self.servicelist_menu.close()
        self.user_main = UserMain(self.account)
        self.user_main.show()

    def get_activated(self):
        selected_item = self.servicelist_menu.Combobox.currentText()
        self.link = f"/ServiceList/{selected_item}"
        for i in reversed(range(self.servicelist_menu.verticalLayout.count())):
            self.servicelist_menu.verticalLayout.itemAt(i).widget().setParent(None)
        self.servicelist_menu.verticalLayout.addWidget(self.list_service())


    def list_service(self):
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
        
        self.ref = db.reference(self.link)
        data = self.ref.get()

        labels = ['No.', 'Name', 'Description', 'Price']

        for i, label in enumerate(labels):
            label = QLabel(label)
            label.setStyleSheet("color: white;")
            content_layout.addWidget(label, 0, i)

        for i, (key, value) in enumerate(data.items(), start = 1):
            row_data = [i, key, value['description'], f"{value['price']}k"]
            for j, item in enumerate(row_data):
                label = QLabel(str(item))
                label.setStyleSheet("color: white;")
                if item == value['description']:
                    label.setWordWrap(True)
                    label.setFixedHeight(100)
                else:
                    label.setFixedHeight(50)
                content_layout.addWidget(label, i, j)
            content_layout.setRowMinimumHeight(i, 120)

        return scroll_area




class ConfirmationPage(QMainWindow):
    def __init__(self, data, account):
        super(ConfirmationPage, self).__init__()
        self.data = data
        self.account = account
        self.init_ui()

        self.show()

    def init_ui(self):
        self.confirmation_page = uic.loadUi('file_ui/shopping_cart.ui', self)
        self.confirmation_widget = ConfirmationWidget(self.data)

        self.confirmation_page.verticalLayout.addWidget(self.confirmation_widget) 

        self.confirmation_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.confirmation_page.push_back.clicked.connect(self.to_sparepart)

        self.confirmation_page.push_buy.clicked.connect(self.get_pdf)


    def to_sparepart(self):
        if hasattr(self, 'confirmation_page'):
            self.confirmation_page.close()
        self.sparepart_page = SparepartMenu(self.account)
        self.sparepart_page.show()

    def save_pdf(self, content, filename):
        with open(filename, 'wb') as f:
            f.write(content)


    def get_pdf(self):
        data_buy = self.data
        

        api_key = "a4b8MTQ4NzU6MTE5NTM6VHREamhxTExBSW5tQ3VPbA="
        template_id = "efc77b23aef49cee"

        data = {
                "brand_name": "CMech Service",
                "invoice_no": "123 456789",
                "invoice_date": "01 / 10 /2022  ",
                "account_name": "Lorem Ipsum",
                "bank_det": "Bank Masyarakat Sejahtera",
                "company_name": "CMech Service",
                "street_address": "24 Los Angeles, India",
                "items":None,
                "terms" : "Lorem ipsum dolor sit, amet consectetur",
                "conditions" : "ipsum dolor sit, amet consectetur",
                "tel1": "+123 456 7890",
                "tell2": "+777 500 5485",
                "mail1": "sales@yourwebsite.com",
                "mail2": "support@yourwebsite.com",
                "address": "Lorem ipsum-40"
                }
        data['items'] = data_buy
        print(data)

        response = requests.post(
            F"https://rest.apitemplate.io/v2/create-pdf?template_id={template_id}",
            headers = {"X-API-KEY": F"{api_key}"},
            json = data
        )

        if response.status_code == 200:
            pdf_content = json.loads(response.content)['download_url']
            response_content = requests.get(pdf_content)
            with open('invoice.pdf', 'wb') as file:
                file.write(response_content.content)
            return pdf_content
        else:
            print(f"Error: {response.status_code}")
            return None
        