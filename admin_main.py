import pandas as pd

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from cred import * 

class AdminMain(QMainWindow):
    def __init__(self):
        super(AdminMain, self).__init__()

        self.main_page = uic.loadUi('file_ui/admin_main_menu.ui', self)
        self.get_data_sales()
        self.show()

    def get_data_sales(self):
        ref = db.reference("/Sales")
        database = ref.get()
        df = pd.DataFrame([(date, product, info['quantity'], info['total']) 
                   for date, products in database.items() 
                   for product, info in products.items()],
                  columns=['Date', 'Product', 'Quantity', 'Total'])

        return df





