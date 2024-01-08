from logger_setup import setup_logging
import logging
from datetime import datetime
import logic

setup_logging()
logger = logging.getLogger(__name__)
logger.info(f"Run started @ {datetime.now().strftime('%y-%m-%d %H:%M')}")
wordpress_id = logic.create_post(property_id='34', data={'terms': [{'name': ' New Jersey State'}, {'name': 'Hi', 'taxonomy': 'property_features'}, {'name': 'Hi2', 'taxonomy': 'property_city', 'parent': 'New York'}], 'main': {'post_title': 'Hello hi I\'m jdj', 'post_status' : 'publish'}, 'meta': {'property_price': '985214'}})
print(wordpress_id)
print(wordpress_id)
logger.info(f"Run done @ {datetime.now().strftime('%y-%m-%d %H:%M')}")