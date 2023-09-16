from PyQt5.QtWidgets import (QWidget, QLabel, QMessageBox, 
                             QGridLayout, QScrollArea, QPushButton, 
                             QHBoxLayout, QVBoxLayout, QTableWidget, QTableWidgetItem)

from firebase_admin import db
from cred import *


class SparepartWidget(QWidget):
    def __init__(self, link):
        super().__init__()
        
        self.link = link
        self.data = db.reference(self.link).get()
        self.data_buy = []
        self.set_scroll()

    def button_clicked(self, index, increment, name):
        check = 0
        current_data = db.reference(self.link).get()
        self.counters[index] += increment
        label = self.findChild(QLabel, f'label_{index}')
        if self.counters[index] < 0:
            self.alert("Quantity cannot be negatif!")
            return

        if current_data[name]['stock'] == 0:
            self.alert("Out of stock!")
            return

        if label is not None:
            label.setText(" " * 5 + str(self.counters[index]))
        for key, value in current_data.items():
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

        self.total_quantity.setText(" " * 10 + str(self.total_quantity_buy))
        self.total_price.setText(" " * 10 + str(self.total_price_buy) + 'k')

    def alert(self, text):
        alert = QMessageBox(self)
        alert.setWindowTitle('Alert!')
        alert.setText(text)
        alert.setIcon(QMessageBox.Warning)
        button = alert.exec()
        if button == QMessageBox.Ok:
            pass
    
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
        table.verticalHeader().setVisible(False)  
        table.setEditTriggers(QTableWidget.NoEditTriggers)  

        layout = QVBoxLayout()

        layout.addWidget(table)
        self.setLayout(layout)