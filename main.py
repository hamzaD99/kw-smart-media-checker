from logger_setup import setup_logging
import logging
from datetime import datetime
import wpLogic

setup_logging()
logger = logging.getLogger(__name__)
logger.info(f"Run started @ {datetime.now().strftime('%y-%m-%d %H:%M')}")
print(wpLogic.add_post())
logger.info(f"Run done @ {datetime.now().strftime('%y-%m-%d %H:%M')}")