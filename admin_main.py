import pandas as pd
import seaborn as sns
import requests
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout, QLabel, QPushButton, QMessageBox
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QSize


API_KEY = "AIzaSyCd9mCDnVPCDEzwPtYvmDZvWOAyQTpec1k"
FIREBASE_URL = "https://projectbengkel-f2242-default-rtdb.asia-southeast1.firebasedatabase.app/"

class AdminMain(QMainWindow):
    def __init__(self):
        super(AdminMain, self).__init__()
        self.setup_ui()
        self.show()

    def setup_ui(self):
        self.main_page = uic.loadUi('file_ui/admin_main_menu.ui', self)
        self.main_page.Button_graphMotor.clicked.connect(self.graph_motor)
        self.main_page.Button_graphCar.clicked.connect(self.graph_car)
        self.main_page.Button_add_sparepart.clicked.connect(self.to_add_sparepart)
        self.main_page.Button_add_servicelist.clicked.connect(self.to_add_servicelist)

        label = self.findChild(QLabel, 'logo')
        pixmap = QPixmap('Pictures/image 2.png')
        label.setPixmap(pixmap)
        label.setScaledContents(True)

        path = ["Pictures/sparepart.png", "Pictures/service.png", "Pictures/grafic.png", "Pictures/grafic.png"]
        object_name = ['Button_add_sparepart', 'Button_add_servicelist', 'Button_graphMotor', 'Button_graphCar']
        size = [QSize(70, 75), QSize(110, 115), QSize(110, 115), QSize(110, 115)]

        for i in range(4):
            button = self.findChild(QPushButton, object_name[i])
            button.setIcon(QIcon(path[i]))
            button.setIconSize(size[i])


    def graph_motor(self):
        self.graph_motor = Graph(self.get_data_sales('Motorcycle'), 'Motor')
        self.graph_motor.show()

    def graph_car(self):
        self.graph_mobil = Graph(self.get_data_sales('Car'), 'Car')
        self.graph_mobil.show()

    def to_add_sparepart(self):
        self.navigate_to(AddSparepart())

    def to_add_servicelist(self):
        self.navigate_to(AddService())

    def navigate_to(self, window):
        if hasattr(self, 'main_page'):
            self.main_page.close()
        self.window = window
        self.window.show()

    def get_data_sales(self, type):
        database_sparepart = self.get_database(f'Sales/{type}/Sparepart')
        df_sparepart = pd.DataFrame([(date, product, info['quantity'], info['total']) 
                   for date, products in database_sparepart.items() 
                   for product, info in products.items()],
                  columns=['Date', 'Product', 'Quantity', 'Total'])
        
        database_service = self.get_database(f'Sales/{type}/Service')
        df_service = pd.DataFrame([(date, product, info) 
                            for date, products in database_service.items() 
                            for product, info in products.items()], 
                            columns=['Date', 'Service', 'Quantity'])
        

        return df_sparepart, df_service
    
    def get_database(self, directory):
        response_get = requests.get(FIREBASE_URL + f'/{directory}.json?auth=' + API_KEY)
        database = response_get.json()
        return database
    
    def update_database(self, directory, data):
        requests.patch(FIREBASE_URL + f'/{directory}.json?auth=' + API_KEY, json = data)


class Graph(QMainWindow):
    def __init__(self, dataframe, type):
        super().__init__()
        self.df_sparepart = dataframe[0]
        self.df_service = dataframe[1]
        self.type = type
        self.init_graph()

    def init_graph(self):
        central_widget = QWidget()
        layout = QGridLayout()
        sns.set_style("whitegrid")
        sns.set(font_scale = 0.6)
        sales_df_sparepart = self.df_sparepart.groupby('Date')['Total'].sum().reset_index()
        sales_df_service = self.df_service.groupby('Date')['Quantity'].sum().reset_index()

        fig1 = Figure(figsize=(8, 16), dpi=100)
        canvas1 = FigureCanvas(fig1)
        layout.addWidget(canvas1, 0, 0)
        ax1 = fig1.add_subplot(111)
        bar_sparepart = sns.barplot(x = self.df_sparepart['Product'], y = self.df_sparepart['Quantity'], ax = ax1)
        bar_sparepart.set_xticklabels(bar_sparepart.get_xticklabels(), rotation = 23, horizontalalignment='right', fontsize = 6)

        
        fig2 = Figure(figsize=(7, 10), dpi=100)
        canvas2 = FigureCanvas(fig2)
        layout.addWidget(canvas2, 0, 1)
        ax2 = fig2.add_subplot(111)
        line_sparepart = sns.lineplot(x = sales_df_sparepart['Date'], y = sales_df_sparepart['Total'], ax = ax2)

        fig3 = Figure(figsize=(8, 16), dpi=100)
        canvas3 = FigureCanvas(fig3)
        layout.addWidget(canvas3, 1, 0)
        ax3 = fig3.add_subplot(111)
        bar_service = sns.barplot(x = self.df_service['Service'], y = self.df_service['Quantity'], ax = ax3)
        bar_service.set_xticklabels(bar_service.get_xticklabels(), horizontalalignment='center', fontsize = 6)

        fig4 = Figure(figsize=(7, 10), dpi=100)
        canvas4 = FigureCanvas(fig4)
        layout.addWidget(canvas4, 1, 1)
        ax4 = fig4.add_subplot(111)
        line_service = sns.lineplot(x = sales_df_service['Date'], y = sales_df_service['Quantity'], ax = ax4)


        if self.type == 'Motor':
            self.setWindowTitle('Motor')
            bar_sparepart.set(title = 'Motorcycle Sparepart Sales Graph Count')
            line_sparepart.set(title = 'Motorcycle Sparepart Sales Graph')
            bar_service.set(title = 'Motorcycle Service Sales Graph Count')
            line_service.set(title = 'Motorcycle Service Sales Graph')
        else:
            self.setWindowTitle('Car')
            bar_sparepart.set(title = 'Car Sparepart Sales Graph Count')
            line_sparepart.set(title = 'Car Sparepart Sales Graph')
            bar_service.set(title = 'Car Service Sales Graph Count')
            line_service.set(title = 'Car Service Sales Graph')
            

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

class AddSparepart(QMainWindow):
    def __init__(self):
        super(AddSparepart, self).__init__()
        self.setup_ui()
        self.show()

    
    def setup_ui(self):
        self.sparepart_page = uic.loadUi('file_ui/add_sparepart.ui', self)
        self.sparepart_page.push_back.clicked.connect(self.to_admin_main)
        self.sparepart_page.push_update.clicked.connect(self.clicked_update)
        self.sparepart_page.name_input.setStyleSheet("color: white;")
        self.sparepart_page.price_input.setStyleSheet("color: white;")
        self.sparepart_page.stock_input.setStyleSheet("color: white;")
        self.sparepart_page.Combobox.addItems(['Car', 'Motorcycle'])
        label = self.findChild(QLabel, 'logo')
        pixmap = QPixmap('Pictures/image 2.png')
        label.setPixmap(pixmap)
        label.setScaledContents(True)

    def to_admin_main(self):
        if hasattr(self, 'sparepart_page'):
            self.sparepart_page.close()
        self.window = AdminMain()
        self.window.show()

    def clicked_update(self):
        self.name = self.sparepart_page.name_input.text()
        self.type = self.sparepart_page.Combobox.currentText()
        self.price = int(self.sparepart_page.price_input.text())
        self.stock = int(self.sparepart_page.stock_input.text())
        data = {'price': self.price, 'stock':self.stock}
        current_data = self.get_database(f"Sparepart/{self.type}")
        if self.name in current_data.keys():
            current_data[self.name]['stock'] += self.stock
            current_data[self.name]['price'] = self.price
            self.update_database(f"Sparepart/{self.type}", current_data)
        else:
            self.update_database(f"Sparepart/{self.type}/{self.name}", data)
        self.success_update(self.name)
        self.sparepart_page.name_input.clear()
        self.sparepart_page.price_input.clear()
        self.sparepart_page.stock_input.clear()

    def get_database(self, directory):
        response_get = requests.get(FIREBASE_URL + f'/{directory}.json?auth=' + API_KEY)
        database = response_get.json()
        return database
    
    def update_database(self, directory, data):
        requests.patch(FIREBASE_URL + f'/{directory}.json?auth=' + API_KEY, json = data)

    def success_update(self, text):
        success = QMessageBox(self)
        success.setWindowTitle('Success Update!')
        success.setText(f"{text} has been updated!")
        success.setIcon(QMessageBox.Information)
        success.setStyleSheet("color: white;")
        button = success.exec()
        if button == QMessageBox.Ok:
            pass

        
        

    

class AddService(QMainWindow):
    def __init__(self):
        super(AddService, self).__init__()
        self.setup_ui()
        self.show()

    
    def setup_ui(self):
        self.service_page = uic.loadUi('file_ui/add_service.ui', self)
        self.service_page.push_back.clicked.connect(self.to_admin_main)
        self.service_page.push_update.clicked.connect(self.clicked_update)
        self.service_page.name_input.setStyleSheet("color: white;")
        self.service_page.price_input.setStyleSheet("color: white;")
        self.service_page.desc_input.setStyleSheet("color: white;")
        self.service_page.Combobox.addItems(['Car', 'Motorcycle'])
        label = self.findChild(QLabel, 'logo')
        pixmap = QPixmap('Pictures/image 2.png')
        label.setPixmap(pixmap)
        label.setScaledContents(True)

    def to_admin_main(self):
        if hasattr(self, 'service_page'):
            self.service_page.close()
        self.window = AdminMain()
        self.window.show()

    def clicked_update(self):
        self.name = self.service_page.name_input.text()
        self.type = self.service_page.Combobox.currentText()
        self.price = int(self.service_page.price_input.text())
        self.desc = self.service_page.desc_input.text()
        data = {'price': self.price, 'description':self.desc}
        self.update_database(f"ServiceList/{self.type}/{self.name}", data)
        self.success_update(self.name)
        self.service_page.name_input.clear()
        self.service_page.price_input.clear()
        self.service_page.desc_input.clear()

    def get_database(self, directory):
        response_get = requests.get(FIREBASE_URL + f'/{directory}.json?auth=' + API_KEY)
        database = response_get.json()
        return database
    
    def update_database(self, directory, data):
        requests.patch(FIREBASE_URL + f'/{directory}.json?auth=' + API_KEY, json = data)

    def success_update(self, text):
        success = QMessageBox(self)
        success.setWindowTitle('Success Update!')
        success.setText(f"{text} has been updated!")
        success.setIcon(QMessageBox.Information)
        success.setStyleSheet("color: white;")
        button = success.exec()
        if button == QMessageBox.Ok:
            pass










