import logging
import os
from datetime import datetime

class SQLAlchemyFilter(logging.Filter):
    def filter(self, record):
        return not record.name.startswith('sqlalchemy.engine.Engine')

def setup_logging(log_file=f'{datetime.now().strftime("%y%m%d-%H%M")}.log', log_level=logging.DEBUG):
    os.makedirs('Logs', exist_ok=True)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    # Configure SQLAlchemy engine logs
    sqlalchemy_handler = logging.FileHandler(os.path.join('Logs', f'sqlalchemy_{log_file}'))
    sqlalchemy_handler.setLevel(logging.DEBUG)
    sqlalchemy_handler.setFormatter(formatter)
    sqlalchemy_logger = logging.getLogger('sqlalchemy.engine.Engine')
    sqlalchemy_logger.addHandler(sqlalchemy_handler)
    sqlalchemy_logger.setLevel(logging.WARNING)

    # Configure main application logs
    full_log_file = os.path.join('Logs', log_file)
    
    # Remove the default file handler from the root logger
    root_logger = logging.getLogger('')
    for handler in root_logger.handlers:
        if isinstance(handler, logging.FileHandler):
            root_logger.removeHandler(handler)

    # Add the custom file handler for the main application logs
    file_handler = logging.FileHandler(full_log_file)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    file_handler.addFilter(SQLAlchemyFilter())
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    console_handler.addFilter(SQLAlchemyFilter())
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
    root_logger.setLevel(log_level)