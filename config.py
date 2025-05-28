import os
from dotenv import load_dotenv
# Load environment variables
load_dotenv()

# Facebook Credentials
FB_USERNAME = 'alicheema.omni@gmail.com'
FB_PASSWORD = 'ali.omni@cheema'

# Selenium WebDriver Configuration
CHROME_DRIVER_PATH = None  # Will use WebDriver Manager to handle this

# Timeout and Wait Configurations
IMPLICIT_WAIT_TIME = 10
EXPLICIT_WAIT_TIME = 15

# Logging Configuration
LOG_FILE = 'facebook_bot.log'
LOG_LEVEL = 'INFO'
USER_DATA_DIR = 'C:/Users/Talha/AppData/Local/Google/Chrome/User Data/Profile 17'
