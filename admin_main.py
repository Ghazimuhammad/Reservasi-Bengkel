import pandas as pd
import seaborn as sns
import requests
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from PyQt5 import QtCore, uic
from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout


API_KEY = "AIzaSyCd9mCDnVPCDEzwPtYvmDZvWOAyQTpec1k"
FIREBASE_URL = "https://projectbengkel-f2242-default-rtdb.asia-southeast1.firebasedatabase.app/"

class AdminMain(QMainWindow):
    def __init__(self):
        super(AdminMain, self).__init__()
        self.setup_ui()
        self.show()

    def setup_ui(self):
        self.main_page = uic.loadUi('file_ui/admin_main_menu.ui', self)
        self.main_page.Button_graphMotor.clicked.connect(self.add_motor)
        self.main_page.Button_graphCar.clicked.connect(self.add_car)


    def add_motor(self):
        self.graph_motor = Graph(self.get_data_sales('Motorcycle'), 'Motor')
        self.graph_motor.show()

    def add_car(self):
        self.graph_mobil = Graph(self.get_data_sales('Car'), 'Car')
        self.graph_mobil.show()

    def to_add_sparepart(self):
        pass

    def to_add_servicelist(self):
        pass

    def navigate_to(self, window):
        if hasattr(self, 'login_page'):
            self.login_page.close()
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

        fig1 = Figure(figsize=(8, 16), dpi=100)
        canvas1 = FigureCanvas(fig1)
        layout.addWidget(canvas1, 0, 0)
        ax1 = fig1.add_subplot(111)
        bar_sparepart = sns.barplot(x = self.df_sparepart['Product'], y = self.df_sparepart['Quantity'], ax = ax1)
        bar_sparepart.set_xticklabels(bar_sparepart.get_xticklabels(), rotation = 23, horizontalalignment='right', fontsize = 6)

        
        fig2 = Figure(figsize=(7, 5), dpi=100)
        canvas2 = FigureCanvas(fig2)
        layout.addWidget(canvas2, 0, 1)
        ax2 = fig2.add_subplot(111)
        line_sparepart = sns.lineplot(x = self.df_sparepart['Date'], y = self.df_sparepart['Total'], ax = ax2)

        fig3 = Figure(figsize=(8, 16), dpi=100)
        canvas3 = FigureCanvas(fig3)
        layout.addWidget(canvas3, 1, 0)
        ax3 = fig3.add_subplot(111)
        bar_service = sns.barplot(x = self.df_service['Service'], y = self.df_service['Quantity'], ax = ax3)
        bar_service.set_xticklabels(bar_service.get_xticklabels(), horizontalalignment='center', fontsize = 6)

        fig4 = Figure(figsize=(7, 5), dpi=100)
        canvas4 = FigureCanvas(fig4)
        layout.addWidget(canvas4, 1, 1)
        ax4 = fig4.add_subplot(111)
        line_service = sns.lineplot(x = self.df_service['Date'], y = self.df_service['Quantity'], ax = ax4)


        if self.type == 'Motor':
            bar_sparepart.set(title = 'Motorcycle Sparepart Sales Graph Count')
            line_sparepart.set(title = 'Motorcycle Sparepart Sales Graph')
            bar_service.set(title = 'Motorcycle Service Sales Graph Count')
            line_service.set(title = 'Motorcycle Service Sales Graph')
        else:
            bar_sparepart.set(title = 'Car Sparepart Sales Graph Count')
            line_sparepart.set(title = 'Car Sparepart Sales Graph')
            bar_sparepart.set(title = 'Car Service Sales Graph Count')
            line_sparepart.set(title = 'Car Service Sales Graph')
            
        
        # plt.subplots_adjust(wspace = 0.4)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)










