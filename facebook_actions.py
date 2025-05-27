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
            self.driver.get("https://www.facebook.com/login")
            
            # Find username and password fields
            username_field = self.wait.until(
                EC.presence_of_element_located((By.ID, "email"))
            )
            password_field = self.wait.until(
                EC.presence_of_element_located((By.ID, "pass"))
            )

            # Use ActionChains for more robust input
            self.actions.move_to_element(username_field) \
                .click() \
                .send_keys(username) \
                .move_to_element(password_field) \
                .click() \
                .send_keys(password) \
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
            # Use JavaScript to navigate (more reliable for some URLs)
            self.driver.execute_script(f"window.location.href = '{post_url}'")
            
            # Wait for page to load
            self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'post')]"))
            )
            
            # Scroll to the post using ActionChains
            post_element = self.driver.find_element(By.XPATH, "//div[contains(@class, 'post')]")
            self.actions.move_to_element(post_element).perform()
            
            self.logger.info(f"Navigated to post: {post_url}")
        except Exception as e:
            self.logger.error(f"Navigation failed: {e}")
            raise

    def comment_on_post(self, comment_text: str):
        """Comment on the current post using ActionChains"""
        try:
            # Find comment textarea
            comment_box = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//div[@role='textbox']"))
            )

            # Use ActionChains for commenting
            self.actions.move_to_element(comment_box) \
                .click() \
                .send_keys(comment_text) \
                .send_keys(Keys.RETURN) \
                .perform()
            
            # Wait for comment to be posted
            self.wait.until(
                EC.presence_of_element_located((By.XPATH, f"//div[contains(text(), '{comment_text}')]"))
            )
            
            self.logger.info("Comment posted successfully")
        except Exception as e:
            self.logger.error(f"Commenting failed: {e}")
            raise

    def reply_to_comment(self, comment_text: str, parent_comment_xpath: str):
        """Reply to a specific comment using advanced ActionChains"""
        try:
            # Find parent comment
            parent_comment = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, parent_comment_xpath))
            )

            # Scroll to parent comment
            self.actions.move_to_element(parent_comment).perform()

            # Find and click reply button using complex ActionChains
            reply_button = parent_comment.find_element(
                By.XPATH, ".//div[contains(@aria-label, 'Reply') or contains(@data-testid, 'comment-reply')]"
            )
            
            # Perform click with ActionChains
            self.actions.move_to_element(reply_button) \
                .pause(0.5) \
                .click() \
                .perform()

            # Wait for reply box to appear
            reply_box = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//div[@role='textbox']"))
            )

            # Use ActionChains to type and submit reply
            self.actions.move_to_element(reply_box) \
                .click() \
                .send_keys(comment_text) \
                .send_keys(Keys.RETURN) \
                .perform()
            
            self.logger.info("Reply posted successfully")
        except Exception as e:
            self.logger.error(f"Replying failed: {e}")
            raise


    def scroll_and_find_element(self, locator: Tuple[By, str], max_scroll: int = 3) -> WebElement:
        """
        Scroll and find an element using ActionChains
        
        :param locator: Tuple of (By, locator_string)
        :param max_scroll: Maximum number of scroll attempts
        :return: Found WebElement
        """
        for _ in range(max_scroll):
            try:
                element = self.driver.find_element(*locator)
                self.actions.move_to_element(element).perform()
                return element
            except:
                # Scroll down
                self.actions.send_keys(Keys.PAGE_DOWN).perform()
        
        raise Exception(f"Element not found after {max_scroll} scroll attempts")

    def close(self):
        """Close the browser"""
        self.driver.quit() 