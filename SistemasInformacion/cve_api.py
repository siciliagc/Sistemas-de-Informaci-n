import requests

url = "https://cve.circl.lu/api/last"

response = requests.get(url)
data = response.json()[:10]

for vulnerability in data:
    print(f"Vulnerabilidad: {vulnerability['id']}")
    print(f"CAPEC: {vulnerability['capec']['name']}")
    print(f"URL: {vulnerability['references']} \n")




