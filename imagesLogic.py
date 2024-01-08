import dotenv
import os
import requests
from requests.auth import HTTPBasicAuth
from logger_setup import setup_logging
import logging
setup_logging()
logger = logging.getLogger(__name__)
dotenv.load_dotenv()
wordpress_url = os.getenv("WORDPRESS_URL")
username = os.getenv("WORDPRESS_USERNAME")
password = os.getenv("WORDPRESS_PASSWORD")

def add_image(data, name):
    try:
        headers = {
            "Content-Type": "image/jpg",
            'Content-Disposition': f"attachment; filename={name}.jpg"
        }
        response = requests.post(f'{wordpress_url}/media', headers = headers, data = data, auth=HTTPBasicAuth(username, password))
        try:
            id = response.json()['id']
            logger.info(f"Image successfully uploaded {name}")
            return id
        except:
            raise ValueError
    except:
        logger.error(f"Something went wrong while uploading image {name}")
        return -1
def read_image(path):
    try:
        response = requests.get(path)
        name = path.split('/')[-1]
        return {'data': response.content, 'name': name}
    except:
        logger.error(f"Something went wrong while reading image {path}")
        return False