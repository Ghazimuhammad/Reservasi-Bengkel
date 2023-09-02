import login
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = login.Login()
    app.exec_()
