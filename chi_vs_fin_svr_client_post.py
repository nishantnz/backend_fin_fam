import requests
BASE = "http://127.0.0.1:5000/predictChildren"

json_data = {"income":4000000, "debt":200000, "investment":150000}
resp = requests.post(url=BASE,json=json_data)
print(resp.status_code)
print(resp.text)