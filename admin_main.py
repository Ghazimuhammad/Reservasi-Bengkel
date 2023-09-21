import pandas as pd
import seaborn as sns
import requests
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from PyQt5 import QtCore, uic
from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout


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
        self.graph_motor = Graph(self.get_data_sales('MotorCycle'), 'Motor')
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
        database = self.get_database(f'Sales/{type}')
        df = pd.DataFrame([(date, product, info['quantity'], info['total']) 
                   for date, products in database.items() 
                   for product, info in products.items()],
                  columns=['Date', 'Product', 'Quantity', 'Total'])
        
        return df
    
    def get_database(self, directory):
        response_get = requests.get(FIREBASE_URL + f'/{directory}.json?auth=' + API_KEY)
        database = response_get.json()
        return database
    
    def update_database(self, directory, data):
        requests.patch(FIREBASE_URL + f'/{directory}.json?auth=' + API_KEY, json = data)


class Graph(QMainWindow):
    def __init__(self, dataframe, type):
        super().__init__()
        self.df = dataframe
        self.type = type
        self.init_graph()

    def init_graph(self):
        central_widget = QWidget()
        layout = QHBoxLayout()

        fig1 = Figure(figsize=(5, 4), dpi=100)
        canvas1 = FigureCanvas(fig1)
        layout.addWidget(canvas1)
        ax1 = fig1.add_subplot(111)
        bar = sns.barplot(x = self.df['Product'], y = self.df['Quantity'], ax = ax1)
        bar.set_xticklabels(bar.get_xticklabels(), rotation = 45, horizontalalignment='right')

        # Create the second bar graph
        # fig2 = Figure(figsize=(5, 4), dpi=100)
        # canvas2 = FigureCanvas(fig2)
        # layout.addWidget(canvas2)
        # ax2 = fig2.add_subplot(111)
        # ax2.bar(df['Category'], df['Values2'])


        fig3 = Figure(figsize=(5, 4), dpi=100)
        canvas3 = FigureCanvas(fig3)
        layout.addWidget(canvas3)
        ax3 = fig3.add_subplot(111)
        line = sns.lineplot(x = self.df['Date'], y = self.df['Total'], ax = ax3)

        if self.type == 'Motor':
            bar.set(title = 'MotorCycle Sparepart Sales Graph Count')
            line.set(title = 'MotorCycle Sparepart Sales Graph')
        else:
            bar.set(title = 'Car Sparepart Sales Graph Count')
            line.set(title = 'Car Sparepart Sales Graph')
            
            

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)










