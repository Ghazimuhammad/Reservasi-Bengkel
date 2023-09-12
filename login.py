from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QMainWindow, QPushButton,
    QLineEdit,QMessageBox,
    QLabel, QCompleter)
import sys
import re
from user_main import UserMain
from admin_main import AdminMain
from cred import *


class Login(QMainWindow):
    def __init__(self):
        super(Login, self).__init__()

        self.ref = db.reference('/Login')
        self.database_login = self.ref.get()
        self.login_page = uic.loadUi('file_ui/login.ui', self)

        self.username = self.findChild(QLineEdit, 'username_input')
        self.username.setCompleter(QCompleter(['admin@gmail.com', 'halouser@gmail.com']))
        self.password = self.findChild(QLineEdit, 'password_input')

        self.create_account = self.findChild(QPushButton, 'push_create_account')
        self.create_account.clicked.connect(self.to_create_account)

        self.login_button = self.findChild(QPushButton, 'push_login')
        self.login_button.clicked.connect(self.verify_login)

        label = self.findChild(QLabel, 'label_2')
        pixmap = QPixmap('Pictures/image 2.png')
        label.setPixmap(pixmap)
        label.setScaledContents(True)

        self.show()
    
    def to_create_account(self):
        self.login_page.close()
        self.signup_page = Signup()
        self.signup_page.show()

    def verify_login(self):
        username = self.username.text()
        password = self.password.text()
        username_nonvalid = True
        password_nonvalid = True
        if username == 'admin@gmail.com' and password == 'Haloadmin1234':
            self.to_admin_main()
            return
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
        
        
    def to_user_main(self):
        self.login_page.close()
        self.user_main_page = UserMain()
        self.user_main_page.show()
    
    def to_admin_main(self):
        self.login_page.close()
        self.to_admin_main_page = AdminMain()
        self.to_admin_main_page.show()

    def alert(self, text):
        alert = QMessageBox(self)
        alert.setWindowTitle('Alert!')
        alert.setText(text)
        alert.setIcon(QMessageBox.Warning)
        button = alert.exec()
        if button == QMessageBox.Ok:
            pass

    def remove_label(self):
        self.username_input.clear()
        self.password_input.clear()


class Signup(QMainWindow):
    def __init__(self):
        super(Signup, self).__init__()

        self.ref = db.reference('/Login')
        self.database_login = self.ref.get()

        self.signup_page = uic.loadUi('file_ui/signup.ui', self)

        self.back_button = self.findChild(QPushButton, 'push_back')
        self.back_button.clicked.connect(self.to_login)

        self.username_input = self.findChild(QLineEdit, 'username_input')
        self.password_input = self.findChild(QLineEdit, 'password_input')
        self.conpassword_input = self.findChild(QLineEdit, 'conpassword_input')

        self.create_account_button = self.findChild(QPushButton, 'push_create_account')
        self.create_account_button.clicked.connect(self.create_account)


        self.show()
    
    def to_login(self):
        self.signup_page.close()
        self.login_page = Login()
        self.login_page.show()

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
            self.alert("This Email already exist.")

        elif password != conpassword:
            self.password_input.clear()
            self.conpassword_input.clear()
            self.alert("Password doesn't match confirmation password!")

        else:
            username = username.replace('.', '')
            data_hold = {username: password}
            if self.database_login is None:
                self.ref.set({'admin@gmailcom':'Haloadmin1234'})
                self.ref.update(data_hold)
            else:
                self.ref.update(data_hold)

            self.remove_label()
            self.success_create_account()
            self.to_login()
    
    
    def alert(self, text):
        alert = QMessageBox(self)
        alert.setWindowTitle('Alert!')
        alert.setText(text)
        alert.setIcon(QMessageBox.Warning)
        button = alert.exec()
        if button == QMessageBox.Ok:
            pass

    def success_create_account(self):
        success = QMessageBox(self)
        success.setWindowTitle('Congratulations!')
        success.setText("Your account has been created!")
        success.setIcon(QMessageBox.Information)
        button = success.exec()
        if button == QMessageBox.Ok:
            pass
    
    def invalid_password(self, password):
        return not(re.search("[a-z]", password) and re.search("[A-Z]", password) and re.search("[0-9]", password) and (len(password) >= 8 and len(password) <= 16))

    def invalid_username(self, username):
        regex_uname = r'[^@]+@[^@]+\.[^@]+'
        return not (re.fullmatch(regex_uname, username))
    
    def remove_label(self):
        self.username_input.clear()
        self.password_input.clear()
        self.conpassword_input.clear()