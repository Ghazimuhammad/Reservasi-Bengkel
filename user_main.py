import json, requests
from datetime import datetime
from random import randint

from PyQt5 import uic
from PyQt5.QtWidgets import (QMainWindow, QPushButton, QScrollArea, 
                             QLabel, QLineEdit, 
                             QGridLayout, QTableWidgetItem,
                             QWidget, QMessageBox)
from PyQt5.QtGui import QPixmap, QIcon, QBrush, QColor
from PyQt5.QtCore import QSize, QDate
from user_widget import SparepartWidget, custom_vertikal_bar, custom_horizontal_bar


API_KEY = "AIzaSyCd9mCDnVPCDEzwPtYvmDZvWOAyQTpec1k"
FIREBASE_URL = "https://projectbengkel-f2242-default-rtdb.asia-southeast1.firebasedatabase.app/"



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
        self.main_page.push_mybooking.clicked.connect(self.to_my_booking)

    def to_sparepart(self):
        self.navigate_to(SparepartMenu(self.account))

    def to_reservation(self):
        self.navigate_to(ReservationMenu(self.account))

    def to_service_list(self):
        self.navigate_to(ServiceListMenu(self.account))
    
    def to_my_booking(self):
        try:
            self.navigate_to(MyBookingPage(self.account))
        except:
            self.alert()

    
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
        self.push_sparepart.setIconSize(QSize(70, 75))

        self.push_reservation = self.findChild(QPushButton, 'push_reservation')
        self.push_reservation.setIcon(QIcon("Pictures/reservation.png"))
        self.push_reservation.setIconSize(QSize(90, 95))

        self.push_service_list = self.findChild(QPushButton, 'push_service_list')
        self.push_service_list.setIcon(QIcon("Pictures/service.png"))
        self.push_service_list.setIconSize(QSize(110, 115))
    
    def alert(self):
        alert = QMessageBox(self)
        alert.setWindowTitle('Alert!')
        alert.setText("You haven't made a reservation yet, please make a reservation first")
        alert.setIcon(QMessageBox.Warning)
        alert.setStyleSheet("color: white;")
        button = alert.exec()
        if button == QMessageBox.Ok:
            pass


class SparepartMenu(QMainWindow):
    def __init__(self, account):
        super(SparepartMenu, self).__init__()
        self.account = account
        self.setup_ui()
        self.show()
    
    def setup_ui(self):
        self.sparepart_menu = uic.loadUi('file_ui/sparepart_menu.ui', self)
        self.label = self.findChild(QLabel, 'logo')
        pixmap = QPixmap('Pictures/image 2.png')
        self.label.setPixmap(pixmap)
        self.label.setScaledContents(True)
        self.sparepart_menu.push_back.clicked.connect(self.to_user_main)
        self.sparepart_menu.Combobox.addItems(["Car", 'Motorcycle'])
        self.scrollable_layout = SparepartWidget("Sparepart/Car")
        self.sparepart_menu.verticalLayout.addWidget(self.scrollable_layout)
        self.sparepart_menu.Combobox.currentIndexChanged.connect(self.insert_sparepart_menu)
        self.sparepart_menu.push_next.clicked.connect(self.to_confirmation)

    def to_user_main(self):
        self.navigate_to(UserMain(self.account))

    def to_confirmation(self):
        self.navigate_to(ConfirmationPage(self.scrollable_layout.get_data_buy(), self.account, self.selected_item))

    def navigate_to(self, window):
        if hasattr(self, 'sparepart_menu'):
            self.sparepart_menu.close()
        self.window = window
        self.window.show()

    def insert_sparepart_menu(self):
        self.selected_item = self.sparepart_menu.Combobox.currentText()
        self.link = f"/Sparepart/{self.selected_item}"
        for i in reversed(range(self.sparepart_menu.verticalLayout.count())):
            self.sparepart_menu.verticalLayout.itemAt(i).widget().setParent(None)
        self.scrollable_layout = SparepartWidget(self.link)
        self.sparepart_menu.verticalLayout.addWidget(self.scrollable_layout)
    

class ReservationMenu(QMainWindow):
    def __init__(self, account):
        super(ReservationMenu, self).__init__()
        self.account = account
        self.dt = None
        self.setup_ui()

        self.show()
    
    def setup_ui(self):
        self.reservation_page = uic.loadUi('file_ui/reservation.ui', self)
        label = self.findChild(QLabel, 'logo')
        pixmap = QPixmap('Pictures/image 2.png')
        label.setPixmap(pixmap)
        label.setScaledContents(True)
        self.name = self.findChild(QLineEdit, 'name_input')
        self.reservation_page.type_input.addItem("Car")
        self.reservation_page.type_input.addItem("Motorcycle")
        self.reservation_page.type_input.currentIndexChanged.connect(self.insert_type)
        self.reservation_page.push_back.clicked.connect(self.to_user_main)
        self.reservation_page.dateEdit.setMinimumDate(QDate.currentDate())
        self.reservation_page.push_booking.clicked.connect(self.booking_button)
        self.insert_type()


    def to_user_main(self):
        if hasattr(self, 'reservation_page'):
            self.reservation_page.close()
        self.user_main = UserMain(self.account).show()

    def get_date(self):
        date = self.reservation_page.dateEdit.date()
        time = self.reservation_page.timeEdit.time()
        self.dt = datetime(date.year(), date.month(), date.day(), time.hour(), time.minute(), 0)
        return self.dt

    def insert_type(self):
        self.selected_type = self.reservation_page.type_input.currentText()
        link = f"ServiceList/{self.selected_type}"
        services = self.get_database(link)
        list_service = []
        for service in services.keys():
            list_service.append(service)
        self.reservation_page.service_list.clear()
        self.reservation_page.service_list.addItems(list_service)

    def booking_button(self):
        self.selected_service = self.service_list.currentText()
        current_date = self.get_date()
        data_booking = {str(current_date): {'service': self.selected_service
                        }}
        self.update_database(f"Booking/{self.account}", data_booking)
        data_sales = {str(current_date.date()): {self.selected_service: 1}}
        try:
            current_data_service = self.get_database(f'Sales/{self.selected_type}/Service')
            if str(current_date.date()) in current_data_service.keys():
                if self.selected_service in current_data_service[str(current_date.date())].keys():
                    current_data_service[str(current_date.date())][self.selected_service] += 1
                    data_sales = current_data_service
                else:
                    current_data_service[str(current_date.date())][self.selected_service] = 1
                    data_sales = current_data_service
            self.update_database(f"Sales/{self.selected_type}/Service", data_sales)
        except:
            current_data_service = self.get_database('Sales/Car/Service')
            if str(current_date.date()) in current_data_service.keys():
                if self.selected_service in current_data_service[str(current_date.date())].keys():
                    current_data_service[str(current_date.date())][self.selected_service] += 1
                    data_sales = current_data_service
                else:
                    current_data_service[str(current_date.date())][self.selected_service] = 1
                    data_sales = current_data_service
            self.update_database("Sales/Car/Service", data_sales)
        self.success_book()
        self.to_user_main()

    def get_database(self, directory):
        response_get = requests.get(FIREBASE_URL + f'/{directory}.json?auth=' + API_KEY)
        database = response_get.json()
        return database
    
    def update_database(self, directory, data):
        requests.patch(FIREBASE_URL + f'/{directory}.json?auth=' + API_KEY, json = data)

    def success_book(self):
        success = QMessageBox(self)
        success.setWindowTitle('Thank You!')
        success.setText("Your reservation has been successfull!")
        success.setIcon(QMessageBox.Information)
        success.setStyleSheet("color: white;")
        button = success.exec()
        if button == QMessageBox.Ok:
            pass


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
        label = self.findChild(QLabel, 'logo_sparepart')
        pixmap = QPixmap('Pictures/image 2.png')
        label.setPixmap(pixmap)
        label.setScaledContents(True)

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
        scroll_area.verticalScrollBar().setStyleSheet(str(custom_vertikal_bar()))
        scroll_area.horizontalScrollBar().setStyleSheet(str(custom_horizontal_bar()))
        scroll_area.setStyleSheet("border: 5px;")

        content_layout = QGridLayout(content_widget)
        
        data = self.get_database(self.link)

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
    
    def get_database(self, directory):
        response_get = requests.get(FIREBASE_URL + f'/{directory}.json?auth=' + API_KEY)
        database = response_get.json()
        return database
    
    def update_database(self, directory, data):
        requests.patch(FIREBASE_URL + f'/{directory}.json?auth=' + API_KEY, json = data)


class ConfirmationPage(QMainWindow):
    def __init__(self, data, account, type):
        super(ConfirmationPage, self).__init__()
        self.data = data
        self.account = account
        self.type = type
        self.setup_ui()
        self.insert_table()

        self.show()

    def setup_ui(self):
        self.confirmation_page = uic.loadUi('file_ui/shopping_cart.ui', self)
        label = self.findChild(QLabel, 'logo_sparepart')
        pixmap = QPixmap('Pictures/image 2.png')
        label.setPixmap(pixmap)
        label.setScaledContents(True)
        self.confirmation_page.push_back.clicked.connect(self.to_sparepart)

        self.confirmation_page.push_buy.clicked.connect(self.clicked_buy)

    def insert_table(self):
        self.total_quantity = self.data[-1]['Total quantity']
        self.total_price = self.data[-1]['Total price']
        data_buy = self.data[:-1]
        # self.confirmation_page.tableWidget.setStyleSheet("border: 5px;")
        self.confirmation_page.tableWidget.setStyleSheet("QTableWidget {background-color: #2D2E43; border: 2px #d0d2f9;border-radius: 10px;gridline-color: #ccc;}\
                                                        QHeaderView::section {background-color: #aabade;color: #14212b;padding: 5px;border: 1px solid #ccc;font-size: 14px;}\
                                                        QTableWidgetItem {border: 1px solid #ccc;padding: 5px;font-size: 12px;color: #ffffff;  /* Text color */}")
        self.confirmation_page.tableWidget.setColumnCount(3)
        self.confirmation_page.tableWidget.setRowCount(len(data_buy) + 1)
        self.confirmation_page.tableWidget.setColumnWidth(0, 175)
        self.confirmation_page.tableWidget.setColumnWidth(1, 100)
        self.confirmation_page.tableWidget.setColumnWidth(2, 136)
        self.confirmation_page.tableWidget.setHorizontalHeaderLabels(['Name', 'Quantity', 'Price'])
        i = 0

        for data in data_buy:

            item1 = QTableWidgetItem(f"{data['name']}")
            item1.setForeground(QBrush(QColor(255, 255, 255)))
            self.confirmation_page.tableWidget.setItem(i, 0, item1)

            item2 = QTableWidgetItem(" " * 12 + f"{data['quantity']}")
            item2.setForeground(QBrush(QColor(255, 255, 255)))
            self.confirmation_page.tableWidget.setItem(i, 1, item2)

            item3 = QTableWidgetItem(" " * 12 + str(data['price']) + 'k')
            item3.setForeground(QBrush(QColor(255, 255, 255)))
            self.confirmation_page.tableWidget.setItem(i, 2, item3)


            i += 1
        
        total = QTableWidgetItem('Total')
        total.setForeground(QBrush(QColor(255, 255, 255)))
        self.confirmation_page.tableWidget.setItem(i, 0, total)

        total1 = QTableWidgetItem(" " * 12 + str(self.total_quantity))
        total1.setForeground(QBrush(QColor(255, 255, 255)))
        self.confirmation_page.tableWidget.setItem(i, 1, total1)

        total2 = QTableWidgetItem(" " * 12 + str(self.total_price) + 'k')
        total2.setForeground(QBrush(QColor(255, 255, 255)))
        self.confirmation_page.tableWidget.setItem(i, 2, total2)



    def to_sparepart(self):
        if hasattr(self, 'confirmation_page'):
            self.confirmation_page.close()
        self.sparepart_page = SparepartMenu(self.account)
        self.sparepart_page.show()

    def save_pdf(self, content, filename):
        with open(filename, 'wb') as f:
            f.write(content)



    def update_sales(self):
        current_date = str(datetime.now().date())
        data_sales = self.get_database(f'Sales/{self.type}/Sparepart')
        data_temp = {}
        for data in self.data[:-1]:
            data_temp.update({data['name']: {'quantity': data['quantity'], 'total': data['total']}})

        if current_date in data_sales.keys():
            for name, temp_data in data_temp.items():
                if name in data_sales[current_date]:
                    data_sales[current_date][name]['quantity'] += temp_data['quantity']
                else:
                    data_sales[current_date][name] = temp_data
        else:
            data_sales = {current_date:data_temp}

        try:
            self.update_database(f"Sales/{self.type}/Sparepart", data_sales)
        except KeyError as e:
            print(e)

    def get_database(self, directory):
        response_get = requests.get(FIREBASE_URL + f'/{directory}.json?auth=' + API_KEY)
        database = response_get.json()
        return database
    
    def update_database(self, directory, data):
        requests.patch(FIREBASE_URL + f'/{directory}.json?auth=' + API_KEY, json = data)
        

    def get_pdf(self):
        data_buy = self.data[:-1]
        account = self.account
        

        api_key = "fe70MTUwOTM6MTIxNzI6ZUExbHZGTUk3czR4YnIydQ="
        template_id = "d0877b23a514faf6"


        data = {
                "brand_name": "CMech Service",
                "invoice_no": f"{str(self.random_with_N_digits(3))} {str(self.random_with_N_digits(6))}",
                "invoice_date": f"{str(datetime.now().date())}",
                "account_name": f"{account.split('@', 1)[0]}",
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
        response = requests.post(
            f"https://rest.apitemplate.io/v2/create-pdf?template_id={template_id}",
            headers = {"X-API-KEY": f"{api_key}"},
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
    
    def clicked_buy(self):
        # self.get_pdf()
        self.success_buy()
        self.update_sales()
        if hasattr(self, 'confirmation_page'):
            self.confirmation_page.close()
        UserMain(self.account).show()

    def success_buy(self):
        success = QMessageBox(self)
        success.setWindowTitle('Thank You!')
        success.setText("Your transaction has been successfull!")
        success.setIcon(QMessageBox.Information)
        success.setStyleSheet("color: white;")
        button = success.exec()
        if button == QMessageBox.Ok:
            pass
    
    def random_with_N_digits(self, n):
        range_start = 10**(n-1)
        range_end = (10**n)-1
        return randint(range_start, range_end)


class MyBookingPage(QMainWindow):
    def __init__(self, account):
        super(MyBookingPage, self).__init__()
        self.account = account
        self.setup_ui()
        self.show()

    def setup_ui(self):
        self.my_booking_page = uic.loadUi('file_ui/my_booking.ui', self)
        self.my_booking_page.push_back.clicked.connect(self.to_user_main)
        self.my_booking_page.verticalLayout.addWidget(self.list_booking())
        label = self.findChild(QLabel, 'logo_sparepart')
        pixmap = QPixmap('Pictures/image 2.png')
        label.setPixmap(pixmap)
        label.setScaledContents(True)
    
    def to_user_main(self):
        if hasattr(self, 'my_booking_page'):
            self.my_booking_page.close()
        UserMain(self.account).show()

    def list_booking(self):
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)

        content_widget = QWidget()
        scroll_area.setWidget(content_widget)
        scroll_area.verticalScrollBar().setStyleSheet(str(custom_vertikal_bar()))
        scroll_area.horizontalScrollBar().setStyleSheet(str(custom_horizontal_bar()))
        scroll_area.setStyleSheet("border: 5px;")

        content_layout = QGridLayout(content_widget)

        link = f"Booking/{self.account}"
        
        data = self.get_database(link)

        labels = ['No.', ' ' * 15 + 'Date', ' ' * 15 + 'Service', 'Status']

        for i, label in enumerate(labels):
            label = QLabel(label)
            label.setStyleSheet("color: white;")
            label.setFixedHeight(12)
            if label == 'No.':
                content_layout.setColumnMinimumWidth(0, 3)
            content_layout.addWidget(label, 0, i)

        format_time = "%Y-%m-%d %H:%M:%S"

        for i, (key, value) in enumerate(data.items(), start = 1):
            status = 'Waiting'
            if datetime.strptime(key, format_time) < datetime.now():
                status = 'Finished'
            row_data = [i, key, value['service'], status]
            for j, item in enumerate(row_data):
                label = QLabel(str(item))
                if item == value['service']:
                    label.setWordWrap(True)
                label.setStyleSheet("color: white;")
                label.setFixedHeight(20)
                content_layout.addWidget(label, i, j)
        return scroll_area
    
    def get_database(self, directory):
        response_get = requests.get(FIREBASE_URL + f'/{directory}.json?auth=' + API_KEY)
        database = response_get.json()
        return database
