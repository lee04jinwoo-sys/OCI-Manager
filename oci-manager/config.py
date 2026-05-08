
import os
from dotenv import load_dotenv

load_dotenv()

# OCI Config
OCI_CONFIG_PATH = os.path.expanduser("~/.oci/config")
OCI_CONFIG_PROFILE = "DEFAULT"

# Local Data Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
STATE_FILE = os.path.join(DATA_DIR, "state.json")
KEYS_DIR = os.path.join(DATA_DIR, "keys")
LOGS_DIR = os.path.join(DATA_DIR, "logs")

# Ensure directories exist
for d in [DATA_DIR, KEYS_DIR, LOGS_DIR]:
    if not os.path.exists(d):
        os.makedirs(d)

# Telegram Config
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
