import requests
from requests.auth import HTTPBasicAuth
import dotenv
import os

dotenv.load_dotenv()

url = os.getenv("API_URL")
username = os.getenv("API_USERNAME")
password = os.getenv("API_PASSWORD")
page = 1
limit = 30
total_pages = -1

response = requests.get(f'{url}/50394?page[offset]={page}&page[limit]={limit}', auth=HTTPBasicAuth(username, password))
if response.status_code == 200:
    data = response.json()
    data = data["hits"]
    total = data["total"]["value"]
    if page == 1:
        total_pages = total // limit
        print(total_pages)
    houses = data["hits"]
    print(houses[0])

else:
    print(f"Error: {response.status_code} - {response.text}")

    # ae2ab7e1ae9e37c5f7a7b93f