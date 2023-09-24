import requests, pandas
from datetime import datetime

API_KEY = "AIzaSyCd9mCDnVPCDEzwPtYvmDZvWOAyQTpec1k"
FIREBASE_URL = "https://projectbengkel-f2242-default-rtdb.asia-southeast1.firebasedatabase.app/"

def get_database(directory):
        response_get = requests.get(FIREBASE_URL + f'/{directory}.json?auth=' + API_KEY)
        database = response_get.json()
        return database
    
def update_database(directory, data):
        requests.patch(FIREBASE_URL + f'/{directory}.json?auth=' + API_KEY, json = data)


data = get_database('Sales/Motorcycle/Service')
df = pandas.DataFrame([
    (date, product, info) 
    for date, products in data.items() 
    for product, info in products.items()
], columns=['Date', 'Product', 'Quantity'])
print(df)

# data = {str(datetime.now().date()):{'Claim service': 1}}

# update_database('Sales/Motorcycle/Service', data)
