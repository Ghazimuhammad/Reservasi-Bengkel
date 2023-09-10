from PyQt5 import uic
from PyQt5.QtWidgets import (
    QMainWindow, 
    QApplication, 
    QPushButton,
    QLineEdit,
    QMessageBox)
import sys
import firebase_admin
from firebase_admin import db
import re

cred_obj = firebase_admin.credentials.Certificate('ProjectBengkel.json')
default_app = firebase_admin.initialize_app(cred_obj, {'databaseURL': 'https://projectbengkel-f2242-default-rtdb.asia-southeast1.firebasedatabase.app/'})


class Login(QMainWindow):
    def __init__(self):
        super(Login, self).__init__()
        self.ref = db.reference('/Login')
        self.database_login = self.ref.get()
        self.login_page = uic.loadUi('file_ui/login.ui', self)

        self.username = self.findChild(QLineEdit, 'username_input')
        self.password = self.findChild(QLineEdit, 'password_input')

        self.create_account = self.findChild(QPushButton, 'push_create_account')
        self.create_account.clicked.connect(self.to_create_account)

        self.login_button = self.findChild(QPushButton, 'push_login')
        self.login_button.clicked.connect(self.verify_login)

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
        for key, value in self.database_login.items():
            if key == username.replace('.', ''):
                username_nonvalid = False
                if value == password:
                    password_nonvalid = False
                    self.to_main()
                    return
        
        if username_nonvalid:
            self.remove_label()
            self.alert('Username Invalid!')
        
        elif password_nonvalid:
            self.password.clear()
            self.alert('Your input password is wrong!')
        
        
    def to_main(self):
        self.login_page.close()
        self.main_page = Main()
        self.main_page.show()

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

        elif self.valid_login(username, password, conpassword):
            username = username.replace('.', '')
            data_hold = {username: password}
            if self.database_login is None:
                self.ref.set({'admin@gmailcom':'Haloadmin1234'})
                self.ref.update(data_hold)
            else:
                self.ref.update(data_hold)

            self.remove_label()
            self.success_create_account()
        
        elif password != conpassword:
            self.password_input.clear()
            self.conpassword_input.clear()
            self.alert("Password doesn't match confirmation password!")
            
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

    def valid_email_password(self, username, password):
        return not(self.invalid_password(password)) and not(self.invalid_username(username))
    
    def valid_login(self, username, password, conpassword):
        return password == conpassword and self.valid_email_password(username, password) and not(self.username_not_exist)
    
    def remove_label(self):
        self.username_input.clear()
        self.password_input.clear()
        self.conpassword_input.clear()


class Main(QMainWindow):
    def __init__(self):
        super(Main, self).__init__()

        self.main_page = uic.loadUi('file_ui/user_main_menu.ui', self)

        self.show()
