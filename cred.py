import firebase_admin
from firebase_admin import db

cred_obj = firebase_admin.credentials.Certificate('ProjectBengkel.json')
default_app = firebase_admin.initialize_app(cred_obj, {'databaseURL': 'https://projectbengkel-f2242-default-rtdb.asia-southeast1.firebasedatabase.app/'})