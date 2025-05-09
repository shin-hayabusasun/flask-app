import requests

url = 'http://localhost:5000/api/test'
payload = {'name': '太郎'}

response = requests.post(url, json=payload)

print(response.json())
