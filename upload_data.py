import firebase_admin
from firebase_admin import db

cred_obj = firebase_admin.credentials.Certificate('ProjectBengkel.json')
default_app = firebase_admin.initialize_app(cred_obj, {'databaseURL': 'https://projectbengkel-f2242-default-rtdb.asia-southeast1.firebasedatabase.app/'})

ref_mobil = db.reference('/ServiceList/Motorcycle')
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

data_mobil = {
    'Pit Express': {'description': 'Instant service that only carries out work without having to wait.', 
                        'price': 50},
    'Reguler maintenance': {'description': 'When oil and filter need replacement', 'price': 100},
    'Light service': {'description': 'minor services such as injection services, replacing shock absorbers, or motorbike spare parts', 
                     'price': 200},
    'Heavy repair': {'description': 'major services that take a long time, such as overhaul or pressing the frame.', 
                            'price': 500},
    'Claim service': {'description': 'special service for consumers who want to claim their motorcycle warranty if they experience problems due to manufacturer error.',
                      'price': 0}
}

# ref_motor.set(data_motor)
# ref_mobil.set(data_mobil)

data = ref_mobil.get()
lis = [{key:value} for key, value in data_mobil.items()]
for key, value in data.items():
    print(key)
    print(value)
    print()