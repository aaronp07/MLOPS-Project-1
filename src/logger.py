import os
import logging
from datetime import datetime

# Create logs directory
LOGS_DIR = 'logs'
os.makedirs(LOGS_DIR, exist_ok=True)

# Daily log file
today = datetime.now().strftime('%Y-%m-%d')
LOG_FILE = os.path.join(LOGS_DIR, f'log_{today}.log')

# Basic configuration - only needs to be done once
logging.basicConfig(
    filename=LOG_FILE,
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def get_logger(name: str) -> logging.Logger:
    """
    Get a named logger with INFO level.
    Already configured by basicConfig().
    """
    logger = logging.getLogger(name)
    return logger