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
ref = db.reference('/Login')
if ref.get() is None:
    ref.set({'admin@gmailcom':'Haloadmin1234'})
database_login = ref.get()

class Login(QMainWindow):
    def __init__(self):
        super(Login, self).__init__()
        self.login_page = uic.loadUi('login.ui', self)

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
        for key, value in database_login.items():
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

        self.signup_page = uic.loadUi('signup.ui', self)

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
        username_not_exist = False
        for key in database_login.keys():
            if key == username.replace('.', ''):
                username_not_exist = True

        if self.invalid_username(username):
            self.remove_label()
            self.alert("Invalid Email format, please insert with this format __@___.")
        
        elif self.invalid_password(password):
            self.password_input.clear()
            self.conpassword_input.clear()
            self.alert("password must be 8 - 16 character and contains at least one uppercase character one lowercase character and one number")
        
        elif username_not_exist:
            self.remove_label()
            self.alert("This Email already exist.")

        elif password == conpassword and self.valid_email_password(username, password) and not(username_not_exist):
            username = username.replace('.', '')
            data_hold = {username: password}
            if ref.get() is None:
                ref.set({'admin@gmailcom':'Haloadmin1234'})
            else:
                ref.update(data_hold)

            self.remove_label()
            self.success_create_account()
        
        elif password != conpassword:
            self.password_input.clear()
            self.conpassword_input.clear()
            self.alert("Password doesn't match confirmation password!")
    
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
    
    def remove_label(self):
        self.username_input.clear()
        self.password_input.clear()
        self.conpassword_input.clear()


class Main(QMainWindow):
    def __init__(self):
        super(Main, self).__init__()

        self.signup_page = uic.loadUi('main.ui', self)

        self.show()
