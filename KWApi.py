import requests
from requests.auth import HTTPBasicAuth
import dotenv
import os
import logic
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
    houses = data["hits"]
    for house in houses[4:]:
        house_dict = {
            'id': house['_id'], #
            'address': house['_source']['list_address']['address'], #
            'city': house['_source']['list_address']['city'], #
            'loc': house['_source']['list_address']['coordinates_gp'], #
            'country': house['_source']['list_address']['country'], #
            'desc': house['_source']['list_desc'], #
            'price': house['_source']['current_list_price'], #
            'baths': house['_source']['total_bath'], #
            'beds': house['_source']['total_bed'], #
            'year': house['_source']['year_built'], #
            'area': house['_source']['living_area'], #
            'unit': house['_source']['living_area_units'],
            'parking': house['_source']['raw']['parking_total'], #
            'agent_name': house['_source']['list_agent_office']['list_agent_full_name'],
            'photos': house['_source']['photos'],
            'title': house['_source']['list_address']['full_street_address'], #
            'zip': house['_source']['list_address']['postal_code'] #
        }
        # print(house_dict)
        # wordpress_id = logic.create_post(property_id=house_dict['id'], data={'main': {'post_title': house_dict['title'], 'post_status' : 'publish', 'post_content': house_dict['desc']}, 'meta': {'property_price': house_dict['price'], 'property_address': house_dict['address'], 'property_country': 'Saudi Arabia', 'property_latitude': house_dict['loc']['lat'], 'property_longitude': house_dict['loc']['lon'], 'property-year': house_dict['year'], 'property_bedrooms': house_dict['beds'], 'property_bathrooms': house_dict['baths'], 'property_size': house_dict['area'], 'property-garage': house_dict['parking'], 'property_zip': house_dict['zip']}, 'terms': [{'name': house_dict['city'], 'taxonomy': 'property_city'}]})
        # print(wordpress_id)
        logic.add_images(wordpress_id=31037, photos=house_dict['photos'])
        break

else:
    print(f"Error: {response.status_code} - {response.text}")