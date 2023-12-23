import logic
from logger_setup import setup_logging
import logging
from datetime import datetime

setup_logging()
logger = logging.getLogger(__name__)
logger.info(f"Run started @ {datetime.now().strftime('%y%m%d-%H%M')}")

# wordpress_id = logic.create_post(property_id='34', data={'terms': ['Condos','Sales', 'Hi', 'Gym', ' New Jersey State'], 'main': {'post_title': 'YESSSSSS!', 'post_status' : 'publish'}, 'meta': {'property_price': '985214'}})
# print(wordpress_id)

logic.delete_post(wordpress_id=31001)
logger.info(f"Run done @ {datetime.now().strftime('%y%m%d-%H%M')}")