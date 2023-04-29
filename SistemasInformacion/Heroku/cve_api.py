import requests

url = "https://cve.circl.lu/api/last"

response = requests.get(url)
data = response.json()[:10]

for vulnerability in data:
    print(f"Vulnerabilidad: {vulnerability['id']}")
    print(f"Descripción: {vulnerability['summary']}")




