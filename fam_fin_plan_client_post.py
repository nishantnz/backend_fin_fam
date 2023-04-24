import requests
BASE = "http://127.0.0.1:5000/predictFamily"

json_data = {"income":5000000}
resp = requests.post(url=BASE,json=json_data)
print(resp.status_code)
print(resp.text)