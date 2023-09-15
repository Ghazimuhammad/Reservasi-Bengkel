import json, requests

from PyQt5 import uic
from PyQt5.QtWidgets import (QMainWindow, QPushButton, QScrollArea, 
                             QLabel, QLineEdit, QComboBox, 
                             QGridLayout, QSizePolicy, QVBoxLayout,
                             QHBoxLayout, QTableWidget, QTableWidgetItem,
                             QWidget)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QSize

from firebase_admin import db
from cred import cred_obj, default_app



class UserMain(QMainWindow):
    def __init__(self):
        super(UserMain, self).__init__()
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
        self.navigate_to(SparepartMenu())

    def to_reservation(self):
        self.navigate_to(ReservationMenu())

    def to_service_list(self):
        self.navigate_to(ServiceList())
    
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
    def __init__(self):
        super(SparepartMenu, self).__init__()

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
        self.navigate_to(UserMain())

    def to_confirmation(self):
        self.navigate_to(ConfirmationPage(self.scrollable_layout.get_data_buy()))

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
    def __init__(self):
        super(ReservationMenu, self).__init__()
        self.reservation_page = uic.loadUi('file_ui/reservation.ui', self)

        self.name = self.findChild(QLineEdit, 'name_input')
        self.handphone = self.findChild(QLineEdit, 'phone_input')
        # self.date = self.date_input.dateTime()
        self.reservation_page.type_input.addItem("Car")
        self.reservation_page.type_input.addItem("MotorCycle")
        self.reservation_page.type_input.currentIndexChanged.connect(self.insert_type)
        selected_type = self.reservation_page.type_input.currentText()
        self.insert_type(selected_type)

        self.show()

    def insert_type(self, text):
        combo = QComboBox(self)
        combo.addItem("Paket 1")
        combo.addItem("Paket 2")
        combo.addItem("Paket 3")

        self.reservation_page.horizontalLayout.addWidget(combo)



class ServiceList(QMainWindow):
    def __init__(self):
        super(ServiceList, self).__init__()
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
        self.user_main = UserMain()
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
    def __init__(self, data):
        super(ConfirmationPage, self).__init__()
        self.data = data
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
        self.sparepart_page = SparepartMenu()
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
        


class SparepartWidget(QWidget):
    def __init__(self, link):
        super().__init__()
        
        self.link = link
        self.data = db.reference(self.link).get()
        self.data_buy = []
        self.set_scroll()

    def button_clicked(self, index, increment, name):
        check = 0
        self.counters[index] += increment
        label = self.findChild(QLabel, f'label_{index}')
        if label is not None:
            label.setText(" " * 5 + str(self.counters[index]))
        for key, value in self.data.items():
            if key == name:
                hold = value['stock'] - increment
                db.reference(self.link).child(key).update({'stock':hold})
        self.total_quantity_buy = sum(self.counters[1:])
        self.total_price_buy = sum(self.counters[i] * float(data.get(list(data.keys())[0], {}).get('price')) for i, data in enumerate(self.list_data, start=1))
        for data in self.data_buy:
            if name == data['name']:
                data['quantity'] = self.counters[index]
                check = 1
                break
        if check == 0:
            self.data_buy.append({'name': name, 'quantity': self.counters[index], 'price': self.data[name]['price'], 'total': self.counters[index] * self.data[name]['price']})
            check = 1

        print(self.data_buy)
        self.total_quantity.setText(" " * 10 + str(self.total_quantity_buy))
        self.total_price.setText(" " * 10 + str(self.total_price_buy) + 'k')
    
    def get_data_buy(self):
        self.data_buy.append({'Total quantity': self.total_quantity_buy, 'Total price': self.total_price_buy})
        for i in range(len(self.data_buy) - 1):
            if self.data_buy[i]['quantity'] == 0:
                del self.data_buy[i]
        return self.data_buy

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

        self.list_data = [{key:value} for key, value in self.data.items()]

        labels = ['No.', 'Name', 'Price', 'Count']
        for i, label in enumerate(labels):
            if i == 3:
                i+= 1
            header = QLabel(label)
            header.setStyleSheet("color: white;")
            content_layout.addWidget(header, 0, i)

        i = 1

        for data in self.list_data:
            number = QLabel(str(i))
            number.setStyleSheet("color: white;")
            content_layout.addWidget(number, i, 0)
            
            label = QLabel(list(data.keys())[0])
            content_layout.addWidget(label, i, 1)
            label.setStyleSheet("color: white;")

            price = QLabel(str(data.get(list(data.keys())[0], {}).get('price')) + 'k')
            content_layout.addWidget(price, i, 2)
            price.setStyleSheet("color: white;")

            button_minus = QPushButton(f'-')
            content_layout.addWidget(button_minus, i, 3)

            self.counters.append(0) 
            count = QLabel("     0")
            content_layout.addWidget(count, i, 4)
            count.setObjectName(f'label_{i}')
            count.setStyleSheet("color: white;")

            button_plus = QPushButton(f'+')
            content_layout.addWidget(button_plus, i, 5)

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
        self.total_quantity = QLabel(" " * 10 + "0")
        self.total_quantity.setStyleSheet("color: white;")
        Hbox_layout.addWidget(self.total_quantity)
        self.price_label = QLabel("Total price")
        self.price_label.setStyleSheet("color: white;")
        Hbox_layout.addWidget(self.price_label)
        self.total_price = QLabel(" " * 10 + "0")
        self.total_price.setStyleSheet("color: white;")
        Hbox_layout.addWidget(self.total_price)

        layout.addWidget(scroll_area, 9)
        layout.addWidget(Hbox, 1) 
        self.setLayout(layout)





class ConfirmationWidget(QWidget):
    def __init__(self, data):
        super().__init__()
        self.total_quantity = data[-1]['Total quantity']
        self.total_price = data[-1]['Total price']
        del data[-1]
        self.data = data

        self.resume()

    def resume(self):
        content_layout = QGridLayout()
        table = QTableWidget(len(self.data), 3)
        table.setHorizontalHeaderLabels(['Name', 'Quantity', 'Price'])
        i = 0

        for data in self.data:

            item1 = QTableWidgetItem(f"{data['name']}")
            table.setItem(i, 0, item1)

            item2 = QTableWidgetItem(" " * 12 + f"{data['quantity']}")
            table.setItem(i, 1, item2)

            item3 = QTableWidgetItem(" " * 12 + str(data['price']) + 'k')
            table.setItem(i, 2, item3)


            i += 1
        
        total = QTableWidgetItem('Total')
        table.setItem(i, 0, total)

        total1 = QTableWidgetItem(" " * 12 + str(self.total_quantity))
        table.setItem(i, 1, total1)

        total2 = QTableWidgetItem(" " * 12 + str(self.total_price))
        table.setItem(i, 2, total2)
        
        table.setShowGrid(True)
        table.verticalHeader().setVisible(False)  # Hide vertical header
        table.setEditTriggers(QTableWidget.NoEditTriggers)  # Disable cell editing

        layout = QVBoxLayout()

        # Add the QScrollArea to the layout
        layout.addWidget(table)
        self.setLayout(layout)