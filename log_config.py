import os
import sys
from datetime import datetime
from loguru import logger
from dotenv import load_dotenv

load_dotenv()

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_DIR = "logs"
LOG_PATH = os.path.join(LOG_DIR, f"api_{datetime.utcnow():%Y-%m-%d}.log")

os.makedirs(LOG_DIR, exist_ok=True)

logger.remove()

logger.add(sys.stderr,
           level=LOG_LEVEL,
           colorize=True,
           format="<level>{time:HH:mm:ss} {level: <8} {message}</level>")

logger.add(LOG_PATH,
           rotation="00:00",
           retention="7 days",
           compression="zip",
           level=LOG_LEVEL,
           serialize=False,
           format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}")
