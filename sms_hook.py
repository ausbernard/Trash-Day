import requests

api_url = "http://localhost:5000/sms"

response = requests.get(api_url)
print(response.text)