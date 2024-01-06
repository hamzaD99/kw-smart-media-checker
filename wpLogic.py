import dotenv
import os
import requests
from requests.auth import HTTPBasicAuth

dotenv.load_dotenv()
wordpress_url = os.getenv("WORDPRESS_URL")
username = os.getenv("WORDPRESS_USERNAME")
password = os.getenv("WORDPRESS_PASSWORD")
print(password)
headers = {
    'Content-Type': 'application/json',
}

def add_post():
    res = requests.post(f'{wordpress_url}/estate_property', headers=headers, auth=HTTPBasicAuth(username, password), json={
        'title': 'Test from python',
        'content': 'Hi',
        'status': 'publish',
        
    })
    return res.json()