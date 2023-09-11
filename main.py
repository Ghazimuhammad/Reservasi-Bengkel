from login import Login
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Login()
    app.exec_()
