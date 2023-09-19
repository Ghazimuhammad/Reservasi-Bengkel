import requests






apiKey = "AIzaSyCd9mCDnVPCDEzwPtYvmDZvWOAyQTpec1k"
firebase_url = "https://projectbengkel-f2242-default-rtdb.asia-southeast1.firebasedatabase.app/"

response = requests.get(firebase_url + '/Account.json?auth=' + apiKey)

print(response.json())
