import requests
import pprint

# Base url "Home"
HOME_URL = "http://localhost:5000"
# All the currency rates
API_CONVERT = "/api/calculate"
GET_CURRENCY = "/api/"

# r = requests.get(f"{HOME_URL}{API_CONVERT}/usd")
payload = {'currency_one': 'USD', 'currency_two': 'BGN', 'amount': 100}
# req = requests.get(f"{HOME_URL}{API_CONVERT}", params=payload)
req = requests.get(f"{HOME_URL}{GET_CURRENCY}", params=payload)

try:
    # r.raise_for_status()
    req.raise_for_status()
except Exception as error:
    print(error)



pprint.pprint(req)

