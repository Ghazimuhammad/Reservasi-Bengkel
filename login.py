import requests
import os

import re
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QMainWindow, QPushButton,
    QLineEdit, QMessageBox, QLabel, QCompleter
)
from user_main import UserMain
from admin_main import AdminMain


API_KEY = str(os.getenv("FIREBASE_API"))
FIREBASE_URL = "https://projectbengkel-f2242-default-rtdb.asia-southeast1.firebasedatabase.app/"

# class login
class Login(QMainWindow):
    def __init__(self):
        super(Login, self).__init__()

        self.get_database()
        self.login_page = uic.loadUi('file_ui/login.ui', self)

        self.setup_ui()

    # fungsi untuk melakukan setup ui
    def setup_ui(self):
        self.username = self.findChild(QLineEdit, 'username_input')
        self.username.setCompleter(QCompleter(['admin@gmail.com', 'user@gmail.com']))
        self.password = self.findChild(QLineEdit, 'password_input')

        self.create_account = self.findChild(QPushButton, 'push_create_account')
        self.create_account.clicked.connect(self.to_create_account)

        self.login_button = self.findChild(QPushButton, 'push_login')
        self.login_button.clicked.connect(self.verify_login)

        label = self.findChild(QLabel, 'label_2')
        pixmap = QPixmap('Pictures/image 2.png')
        label.setPixmap(pixmap)
        label.setScaledContents(True)

        if self.database_login is None:
            self.update_database()
        self.show()

    # menuju page signup
    def to_create_account(self):
        self.navigate_to(Signup())

    # menuju user main
    def to_user_main(self):
        self.navigate_to(UserMain(self.username.text().replace(".", "")))
        

    # menuju admin main
    def to_admin_main(self):
        self.navigate_to(AdminMain())

    # fungsi untuk navigasi ke page tertentu
    def navigate_to(self, window):
        if hasattr(self, 'login_page'):
            self.login_page.close()
        self.window = window
        self.window.show()

    # fungsi untuk meminta database dari firebase
    def get_database(self):
        self.response_get = requests.get(FIREBASE_URL + '/Account.json?auth=' + API_KEY)
        self.database_login = self.response_get.json()

    # fungsi untuk ngirim data ke database
    def update_database(self):
        requests.put(FIREBASE_URL + '/Account.json?auth=' + API_KEY, json = {'admin@gmailcom': 'Admin1234'})
    
    # fungsi untuk verifikasi login
    def verify_login(self):
        username = self.username.text()
        password = self.password.text()
        username_nonvalid = True
        password_nonvalid = True

        # menuju admin
        if username == 'admin@gmail.com' and password == 'Admin1234':
            self.to_admin_main()
            return

        # menuju user
        for key, value in self.database_login.items():
            if key == username.replace('.', ''):
                username_nonvalid = False
                if value == password:
                    password_nonvalid = False
                    self.to_user_main()
                    return

        if username_nonvalid:
            self.remove_label()
            self.alert('Username Invalid!')
        elif password_nonvalid:
            self.password.clear()
            self.alert('Your input password is wrong!')

    # notif
    def alert(self, text):
        alert = QMessageBox(self)
        alert.setWindowTitle('Alert!')
        alert.setText(text)
        alert.setIcon(QMessageBox.Warning)
        alert.setStyleSheet("color: white;")
        button = alert.exec()
        if button == QMessageBox.Ok:
            pass
    
    # remove label
    def remove_label(self):
        self.username.clear()
        self.password.clear()


# class signup
class Signup(QMainWindow):
    def __init__(self):
        super(Signup, self).__init__()

        self.get_database()

        self.signup_page = uic.loadUi('file_ui/signup.ui', self)

        self.setup_ui()

    # fungsi untuk setup ui
    def setup_ui(self):
        self.back_button = self.findChild(QPushButton, 'push_back')
        self.back_button.clicked.connect(self.to_login)

        self.username_input = self.findChild(QLineEdit, 'username_input')
        self.password_input = self.findChild(QLineEdit, 'password_input')
        self.conpassword_input = self.findChild(QLineEdit, 'conpassword_input')

        self.create_account_button = self.findChild(QPushButton, 'push_create_account')
        self.create_account_button.clicked.connect(self.create_account)

        self.show()

    # menuju login
    def to_login(self):
        if hasattr(self, 'signup_page'):
            self.signup_page.close()
        Login().show()

    # fungsi untuk validasi dan ngirim data signup
    def create_account(self):
        username = self.username_input.text()
        password = self.password_input.text()
        conpassword = self.conpassword_input.text()
        self.username_not_exist = False

        if self.database_login is not None:
            for key in self.database_login.keys():
                if key == username.replace('.', ''):
                    self.username_not_exist = True

        if self.invalid_username(username):
            self.remove_label()
            self.alert("Invalid Email format, please insert with this format __@___.")
        elif self.invalid_password(password):
            self.password_input.clear()
            self.conpassword_input.clear()
            self.alert("password must be 8 - 16 character and contains at least one uppercase character one lowercase character and one number")
        elif self.username_not_exist:
            self.remove_label()
            self.alert("This Email already exists.")
        elif password != conpassword:
            self.password_input.clear()
            self.conpassword_input.clear()
            self.alert("Password doesn't match confirmation password!")
        else:
            username = username.replace('.', '')
            data_hold = {username: password}

            self.update_database(data_hold)
            self.remove_label()
            self.success_create_account()
            self.to_login()

    def get_database(self):
        self.response_get = requests.get(FIREBASE_URL + '/Account.json?auth=' + API_KEY)
        self.database_login = self.response_get.json()

    def update_database(self, data):
        requests.patch(FIREBASE_URL + '/Account.json?auth=' + API_KEY, json = data)

    def alert(self, text):
        alert = QMessageBox(self)
        alert.setWindowTitle('Alert!')
        alert.setText(text)
        alert.setIcon(QMessageBox.Warning)
        alert.setStyleSheet("color: white;")
        button = alert.exec()
        if button == QMessageBox.Ok:
            pass

    def success_create_account(self):
        success = QMessageBox(self)
        success.setWindowTitle('Congratulations!')
        success.setText("Your account has been created!")
        success.setIcon(QMessageBox.Information)
        success.setStyleSheet("color: white;")
        button = success.exec()
        if button == QMessageBox.Ok:
            pass

    def invalid_password(self, password):
        return not (re.search("[a-z]", password) and re.search("[A-Z]", password) and re.search("[0-9]", password) and (8 <= len(password) <= 16))

    def invalid_username(self, username):
        regex_uname = r'[^@]+@[^@]+\.[^@]+'
        return not re.fullmatch(regex_uname, username)

    def remove_label(self):
        self.username_input.clear()
        self.password_input.clear()
        self.conpassword_input.clear()

