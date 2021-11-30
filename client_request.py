import requests
import pprint

HOME_URL = "http://localhost:5000"
GET_ALL_CURRENCIES = "/api/all"
API_CONVERT = "/api/convert"

payload = {'base_currency': 'USD', 'to_currency': 'BGN', 'amount': 100}
response = requests.get(f"{HOME_URL}{API_CONVERT}", params=payload)

try:
    response.raise_for_status()
except Exception as error:
    print(error)

pprint.pprint(response.json())
