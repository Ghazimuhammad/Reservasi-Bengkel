from PyQt5.QtWidgets import (QWidget, QLabel, QMessageBox, 
                             QGridLayout, QScrollArea, QPushButton, 
                             QHBoxLayout, QVBoxLayout)
import requests
import os

API_KEY = str(os.getenv("FIREBASE_API"))
FIREBASE_URL = "https://projectbengkel-f2242-default-rtdb.asia-southeast1.firebasedatabase.app/"

# class untuk widget sparepart
class SparepartWidget(QWidget):
    def __init__(self, link):
        super().__init__()
        
        self.link = link
        self.data = self.get_database(link)
        self.data_buy = []
        self.set_scroll()

    # fungsi untuk mengambil database dari firebase dan error handling
    def button_clicked(self, index, increment, name):
        check = 0
        current_data = self.get_database(self.link) # ambil data sekarang
        self.counters[index] += increment
        label = self.findChild(QLabel, f'label_{index}')
        if self.counters[index] < 0: # pemesanan tidak bisa negatif
            self.alert("Quantity cannot be negatif!")
            return

        if current_data[name]['stock'] == 0: # check jika stock sparepart habis atau tidak
            self.alert("Out of stock!")
            return

        if label is not None:
            label.setText(" " * 5 + str(self.counters[index]))
        # update database sesuai dengan data yang dipilih
        for key, value in current_data.items():
            if key == name:
                hold = value['stock'] - increment
                data_hold = {name: {'price': value['price'], 'stock': hold}}
                self.update_database(self.link, data_hold)
        self.total_quantity_buy = sum(self.counters[1:]) # total kuantitas pembelian
        self.total_price_buy = sum(self.counters[i] * float(data.get(list(data.keys())[0], {}).get('price')) for i, data in enumerate(self.list_data, start=1)) # todal harga pembelian
        for data in self.data_buy:
            if name == data['name']:
                data['quantity'] = self.counters[index]
                data['total'] = data['quantity'] * data['price']
                check = 1
                break
        if check == 0: # menaruh data yang belum ada
            self.data_buy.append({'name': name, 'quantity': self.counters[index], 'price': self.data[name]['price'], 'total': self.counters[index] * self.data[name]['price']})
            check = 1

        self.total_quantity.setText(" " * 10 + f"<b>{str(self.total_quantity_buy)}<b>")
        self.total_price.setText(" " * 10 + f"<b>{str(self.total_price_buy)}<b>" + 'k')

    def alert(self, text):
        alert = QMessageBox(self)
        alert.setWindowTitle('Alert!')
        alert.setText(text)
        alert.setIcon(QMessageBox.Warning)
        alert.setStyleSheet("color: white;")
        button = alert.exec()
        if button == QMessageBox.Ok:
            pass
    
    # mengambil data hasil pembelian
    def get_data_buy(self):
        self.data_buy.append({'Total quantity': self.total_quantity_buy, 'Total price': self.total_price_buy})
        for i in range(len(self.data_buy) - 1):
            if self.data_buy[i]['quantity'] == 0:
                del self.data_buy[i]
        return self.data_buy

    # fungsi untuk menaruh scroll area secara dinamis
    def set_scroll(self):
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)

        content_widget = QWidget()
        scroll_area.setWidget(content_widget)
        scroll_area.verticalScrollBar().setStyleSheet(str(custom_vertikal_bar()))
        scroll_area.horizontalScrollBar().setStyleSheet(str(custom_horizontal_bar()))
        scroll_area.setStyleSheet("border: 5px;")

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
            # label.setStyleSheet("color: rgb(0, 0, 0); background-color: #aabade; /* Background color */font-size: 12px;padding: 4px;border-radius: 5px")
            label.setStyleSheet("color: white;")

            price = QLabel(str(data.get(list(data.keys())[0], {}).get('price')) + 'k')
            content_layout.addWidget(price, i, 2)
            price.setStyleSheet("color: white;")

            button_minus = QPushButton(f'-')
            button_minus.setStyleSheet("QPushButton{background-color: rgb(80, 80, 122);\
                                       color: white;\
                                       border: none;\
                                       border-radius: 7px;padding: 4px 10px;}\
                                       QPushButton:hover {background-color: rgb(245, 154, 182);}\
                                       QPushButton:pressed {background-color: rgb(109, 68, 81);}\
                                       color: rgb(255, 255, 255);")
            content_layout.addWidget(button_minus, i, 3)

            self.counters.append(0) 
            count = QLabel("     0")
            content_layout.addWidget(count, i, 4)
            count.setObjectName(f'label_{i}')
            count.setStyleSheet("color: white;")

            button_plus = QPushButton(f'+')
            button_plus.setStyleSheet("QPushButton{background-color: rgb(80, 80, 122);\
                                       color: white;\
                                       border: none;\
                                       border-radius: 7px;padding: 4px 10px;}\
                                       QPushButton:hover {background-color: rgb(245, 154, 182);}\
                                       QPushButton:pressed {background-color: rgb(109, 68, 81);}\
                                       color: rgb(255, 255, 255);")
            content_layout.addWidget(button_plus, i, 5)

            button_plus.clicked.connect(lambda checked, index=i, name=list(data.keys())[0]: self.button_clicked(index, 1, name))
            button_minus.clicked.connect(lambda checked, index=i, name=list(data.keys())[0]: self.button_clicked(index, -1, name))
            i += 1

        layout = QVBoxLayout(self)
        layout.addWidget(scroll_area, 9)
        Hbox = QWidget(self) 
        Hbox_layout = QHBoxLayout(Hbox)  
        self.quantity_label = QLabel("<b>Total quantity<b>")
        self.quantity_label.setStyleSheet("color: white;")
        Hbox_layout.addWidget(self.quantity_label)
        self.total_quantity = QLabel(" " * 20 + "<b>0<b>")
        self.total_quantity.setStyleSheet("color: white;")
        Hbox_layout.addWidget(self.total_quantity)
        self.price_label = QLabel("<b>Total price<b>")
        self.price_label.setStyleSheet("color: white;")
        Hbox_layout.addWidget(self.price_label)
        self.total_price = QLabel(" " * 20 + "<b>0<b>")
        self.total_price.setStyleSheet("color: white;")
        Hbox_layout.addWidget(self.total_price)

        layout.addWidget(scroll_area, 9)
        layout.addWidget(Hbox, 1) 
        self.setLayout(layout)

    def get_database(self, directory):
        response_get = requests.get(FIREBASE_URL + f'/{directory}.json?auth=' + API_KEY)
        database = response_get.json()
        return database
    
    def update_database(self, directory, data):
        requests.patch(FIREBASE_URL + f'/{directory}.json?auth=' + API_KEY, json = data)


# custom css buat vertikal dan horizontal bar
def custom_vertikal_bar():
    return ("/* VERTICAL SCROLLBAR */\n"
                                                        " QScrollBar:vertical {\n"
                                                        "    border: none;\n"
                                                        "    background: rgb(45, 45, 68);\n"
                                                        "    width: 14px;\n"
                                                        "    margin: 15px 0 15px 0;\n"
                                                        "    border-radius: 0px;\n"
                                                        " }\n"
                                                        "\n"
                                                        "/*  HANDLE BAR VERTICAL */\n"
                                                        "QScrollBar::handle:vertical {    \n"
                                                        "    background-color: rgb(80, 80, 122);\n"
                                                        "    min-height: 30px;\n"
                                                        "    border-radius: 7px;\n"
                                                        "}\n"
                                                        "QScrollBar::handle:vertical:hover{    \n"
                                                        "    background-color: rgb(255, 0, 127);\n"
                                                        "}\n"
                                                        "QScrollBar::handle:vertical:pressed {    \n"
                                                        "    background-color: rgb(185, 0, 92);\n"
                                                        "}\n"
                                                        "\n"
                                                        "/* BTN TOP - SCROLLBAR */\n"
                                                        "QScrollBar::sub-line:vertical {\n"
                                                        "    border: none;\n"
                                                        "    background-color: rgb(59, 59, 90);\n"
                                                        "    height: 15px;\n"
                                                        "    border-top-left-radius: 7px;\n"
                                                        "    border-top-right-radius: 7px;\n"
                                                        "    subcontrol-position: top;\n"
                                                        "    subcontrol-origin: margin;\n"
                                                        "}\n"
                                                        "QScrollBar::sub-line:vertical:hover {    \n"
                                                        "    background-color: rgb(255, 0, 127);\n"
                                                        "}\n"
                                                        "QScrollBar::sub-line:vertical:pressed {    \n"
                                                        "    background-color: rgb(185, 0, 92);\n"
                                                        "}\n"
                                                        "\n"
                                                        "/* BTN BOTTOM - SCROLLBAR */\n"
                                                        "QScrollBar::add-line:vertical {\n"
                                                        "    border: none;\n"
                                                        "    background-color: rgb(59, 59, 90);\n"
                                                        "    height: 15px;\n"
                                                        "    border-bottom-left-radius: 7px;\n"
                                                        "    border-bottom-right-radius: 7px;\n"
                                                        "    subcontrol-position: bottom;\n"
                                                        "    subcontrol-origin: margin;\n"
                                                        "}\n"
                                                        "QScrollBar::add-line:vertical:hover {    \n"
                                                        "    background-color: rgb(255, 0, 127);\n"
                                                        "}\n"
                                                        "QScrollBar::add-line:vertical:pressed {    \n"
                                                        "    background-color: rgb(185, 0, 92);\n"
                                                        "}\n"
                                                        "\n"
                                                        "/* RESET ARROW */\n"
                                                        "QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
                                                        "    background: none;\n"
                                                        "}\n"
                                                        "QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
                                                        "    background: none;\n"
                                                        "}\n"
                                                        "\n"
                                                        "\n"
                                                        "\n"
                                                        )

def custom_horizontal_bar():
    return ("/* HORIZONTAL SCROLLBAR */\n"
                                                        "QScrollBar:horizontal {\n"
                                                        "    border: none;\n"
                                                        "    background: rgb(45, 45, 68);\n"
                                                        "    height: 14px;\n"
                                                        "    margin: 0 15px 0 15px;\n"
                                                        "    border-radius: 0px;\n"
                                                        "}\n"
                                                        "\n"
                                                        "/* HANDLE BAR HORIZONTAL */\n"
                                                        "QScrollBar::handle:horizontal {\n"
                                                        "    background-color: rgb(80, 80, 122);\n"
                                                        "    min-width: 30px;\n"
                                                        "    border-radius: 7px;\n"
                                                        "}\n"
                                                        "QScrollBar::handle:horizontal:hover {\n"
                                                        "    background-color: rgb(255, 0, 127);\n"
                                                        "}\n"
                                                        "QScrollBar::handle:horizontal:pressed {\n"
                                                        "    background-color: rgb(185, 0, 92);\n"
                                                        "}\n"
                                                        "\n"
                                                        "/* BTN LEFT - SCROLLBAR */\n"
                                                        "QScrollBar::sub-line:horizontal {\n"
                                                        "    border: none;\n"
                                                        "    background-color: rgb(59, 59, 90);\n"
                                                        "    width: 15px;\n"
                                                        "    border-top-left-radius: 7px;\n"
                                                        "    border-bottom-left-radius: 7px;\n"
                                                        "    subcontrol-position: left;\n"
                                                        "    subcontrol-origin: margin;\n"
                                                        "}\n"
                                                        "QScrollBar::sub-line:horizontal:hover {\n"
                                                        "    background-color: rgb(255, 0, 127);\n"
                                                        "}\n"
                                                        "QScrollBar::sub-line:horizontal:pressed {\n"
                                                        "    background-color: rgb(185, 0, 92);\n"
                                                        "}\n"
                                                        "\n"
                                                        "/* BTN RIGHT - SCROLLBAR */\n"
                                                        "QScrollBar::add-line:horizontal {\n"
                                                        "    border: none;\n"
                                                        "    background-color: rgb(59, 59, 90);\n"
                                                        "    width: 15px;\n"
                                                        "    border-top-right-radius: 7px;\n"
                                                        "    border-bottom-right-radius: 7px;\n"
                                                        "    subcontrol-position: right;\n"
                                                        "    subcontrol-origin: margin;\n"
                                                        "}\n"
                                                        "QScrollBar::add-line:horizontal:hover {\n"
                                                        "    background-color: rgb(255, 0, 127);\n"
                                                        "}\n"
                                                        "QScrollBar::add-line:horizontal:pressed {\n"
                                                        "    background-color: rgb(185, 0, 92);\n"
                                                        "}\n"
                                                        "\n"
                                                        "/* RESET ARROW */\n"
                                                        "QScrollBar::left-arrow:horizontal, QScrollBar::right-arrow:horizontal {\n"
                                                        "    background: none;\n"
                                                        "}\n"
                                                        "QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {\n"
                                                        "    background: none;\n"
                                                        "}\n"
                                                        "\n"
                                                        "\n"
                                                        "\n"
                                                        "\n"
                                                        "\n"
                                                        "\n"
                                                        "\n"
                                                        "\n"
                                                        "\n"
                                                        "\n"
                                                        "\n"
                                                        "\n"
                                                        "\n"
                                                        "\n"
"")