import logging
import time
from typing import Dict, Optional, List, Tuple

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from webdriver_manager.chrome import ChromeDriverManager

import config

class FacebookBot:
    def __init__(self):
        # Setup logging
        logging.basicConfig(
            filename=config.LOG_FILE, 
            level=getattr(logging, config.LOG_LEVEL),
            format='%(asctime)s - %(levelname)s: %(message)s'
        )
        self.logger = logging.getLogger(__name__)

        # Setup Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument(f"user_data_dir={config.USER_DATA_DIR}")
        # Uncomment the line below for headless mode if needed
        # chrome_options.add_argument("--headless")

        # Setup WebDriver
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.implicitly_wait(config.IMPLICIT_WAIT_TIME)
        self.wait = WebDriverWait(self.driver, config.EXPLICIT_WAIT_TIME)
        self.actions = ActionChains(self.driver)

    def login(self, username: str, password: str):
        """Login to Facebook using ActionChains"""
        try:
            # Navigate to Facebook homepage to utilize persistent session
            self.driver.get("https://www.facebook.com")
            time.sleep(3)
            cookies = self.driver.get_cookies()
            if any(cookie.get("name") == "c_user" for cookie in cookies):
                self.logger.info("User is already logged in with persistent session.")
                return

            # Not logged in, proceed to login page
            self.driver.get("https://www.facebook.com/login")

            # Check if the email field is present and perform login if needed
            username_field = self.wait.until(
                EC.presence_of_element_located((By.ID, "email"))
            )
            password_field = self.wait.until(
                EC.presence_of_element_located((By.ID, "pass"))
            )

            # Use ActionChains for more robust input
            self.actions.move_to_element(username_field) \
                .click() \
                .pause(1) \
                .send_keys(username) \
                .pause(1) \
                .move_to_element(password_field) \
                .click() \
                .pause(1) \
                .send_keys(password) \
                .pause(1) \
                .send_keys(Keys.RETURN) \
                .perform()

            # Wait for login to complete
            self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//div[@role='main']"))
            )
            self.logger.info("Successfully logged in")

        except Exception as e:
            self.logger.error(f"Login failed: {e}")
            raise

    def navigate_to_post(self, post_url: str):
        """Navigate to a specific Facebook post using ActionChains"""
        try:
            # Construct the post URL from post_id (format: pageID_postID)
            # page_id, post_id_part = post_id.split('_')
            # post_url = f"https://www.facebook.com/{page_id}/posts/{post_id_part}"
            self.driver.execute_script(f"window.location.href = '{post_url}'")
            
            # Wait for 4 seconds instead of explicit wait
            time.sleep(4)
            
            self.logger.info(f"Navigated to post: {post_url}")
        except Exception as e:
            self.logger.error(f"Navigation failed: {e}")
            raise

    def comment_on_post(self, comment_text: str):
        """Comment on the current post using ActionChains"""
        try:
            # Find comment textarea
            comment_box = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='textbox'][aria-label='Write a comment…']"))
            )

            # Use ActionChains for commenting
            self.actions.move_to_element(comment_box) \
                .click() \
                .pause(1) \
                .send_keys(comment_text) \
                .pause(1) \
                .send_keys(Keys.RETURN) \
                .perform()
            
            # Wait for comment to be posted
            time.sleep(2)
            
            self.logger.info("Comment posted successfully")
        except Exception as e:
            self.logger.error(f"Commenting failed: {e}")
            raise


    def reply_to_comment(self, comment_text: str, parent_comment_id: str):
        """Reply to a specific comment using advanced ActionChains"""
        try:
            # Find parent comment by comment_id in href
            parent_comment = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, f"//a[contains(@href, 'comment_id={parent_comment_id}')]"))
            )

            # Scroll to parent comment
            self.driver.execute_script("arguments[0].scrollIntoView(true);", parent_comment)
            time.sleep(1)  # Small delay to ensure scrolling completes

            # Find the parent comment container
            # First, navigate up to find the comment container that contains both the comment and its reply button
            comment_container = parent_comment.find_element(By.XPATH, "./ancestor::div[contains(@class, 'comment') or @role='article'][1]")
            
            # Now find the reply button within this container
            reply_button = comment_container.find_element(By.XPATH, ".//div[contains(text(), 'Reply')]")
            
            self.actions.move_to_element(reply_button) \
                .pause(0.5) \
                .click() \
                .perform()
            
            # Wait for reply box to appear
            reply_box = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='textbox'][aria-label^='Reply to']"))
            )

            # Use ActionChains to type and submit reply
            self.actions.move_to_element(reply_box) \
                .click() \
                .send_keys(comment_text) \
                .send_keys(Keys.RETURN) \
                .perform()

            # Wait for reply to be posted
            time.sleep(2)
            self.wait.until(
                EC.presence_of_element_located((By.XPATH, f"//span[contains(text(), '{comment_text}')]"))
            )

            self.logger.info("Reply posted successfully")
        except Exception as e:
            self.logger.error(f"Replying failed: {e}")
            raise


    def close(self):
        """Close the browser"""
        self.driver.quit() 