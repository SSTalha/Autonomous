import os
from dotenv import load_dotenv
# Load environment variables
load_dotenv()

# Facebook Credentials
FB_USERNAME = os.getenv('FB_USERNAME')
FB_PASSWORD = os.getenv('FB_PASSWORD')

# Selenium WebDriver Configuration
CHROME_DRIVER_PATH = None  # Will use WebDriver Manager to handle this

# Timeout and Wait Configurations
IMPLICIT_WAIT_TIME = 10
EXPLICIT_WAIT_TIME = 15

# Logging Configuration
LOG_FILE = 'facebook_bot.log'
LOG_LEVEL = 'INFO'
USER_DATA_DIR = 'your_chrome_path'
#Enter your chrome profile path above. You can find it by opening chrome and typing chrome://version in the URL bar and copying the full path of 'Profile Path'.
