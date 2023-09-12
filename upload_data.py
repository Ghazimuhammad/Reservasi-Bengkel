import firebase_admin
from firebase_admin import db

cred_obj = firebase_admin.credentials.Certificate('ProjectBengkel.json')
default_app = firebase_admin.initialize_app(cred_obj, {'databaseURL': 'https://projectbengkel-f2242-default-rtdb.asia-southeast1.firebasedatabase.app/'})

ref_motor = db.reference('/Sparepart/MotorCycle')
# data_motor = {
#     'Tire': {'price': 150, 'stock': 100},
#     'V Belt': {'price': 120, 'stock': 100},
#     'Spark Plug': {'price': 70, 'stock': 100},
#     'Filter': {'price': 50, 'stock': 100},
#     'Battery': {'price': 80, 'stock': 100},
#     'Clutch Plate': {'price': 100, 'stock': 100},
#     'Machine Oil': {'price': 55, 'stock': 100},
#     'Rearview Mirror': {'price': 125, 'stock': 100}
# }

# ref_mobil = db.reference('/Sparepart/Car')

# data_mobil = {
#     'Tire': {'price': 150, 'stock': 100},
#     'V Belt': {'price': 120, 'stock': 100},
#     'Spark Plug': {'price': 70, 'stock': 100},
#     'Filter': {'price': 50, 'stock': 100},
#     'Battery': {'price': 80, 'stock': 100},
#     'Clutch Plate': {'price': 100, 'stock': 100},
#     'Machine Oil': {'price': 55, 'stock': 100},
#     'Brake Canvas': {'price': 100, 'stock': 100},
#     'Car Bumper': {'price': 170, 'stock': 100},
#     'Wiper': {'price': 100, 'stock': 100},
#     'Rearview Mirror': {'price': 225, 'stock': 100},
#     'Filter Dryer': {'price': 125, 'stock': 100}
# }

# ref_motor.set(data_motor)
# ref_mobil.set(data_mobil)

data = ref_motor.get()
list_data = [{key:value} for key, value in data.items()]
print(list_data[0])