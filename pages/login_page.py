from pages.base_page import BasePage
from selenium.webdriver.common.by import By
import logging

logger = logging.getLogger(__name__)


USERNAME_LOCATOR = "//input[@placeholder='Username']"
PASSWORD_LOCATOR = "//input[@placeholder='Password']"
LOGIN_LOCATOR = "//button[normalize-space()='Login']"


class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    def click_login(self, locator):
        self.click_element(locator)

    def enter_username(self, locator, username):
        self.enter_text(locator, username)

    def enter_password(self, locator, password):
        self.enter_text(locator, password)

    def login(self, username, password):
        """Perform login using the provided username and password."""
        self.enter_username((By.XPATH, USERNAME_LOCATOR), username)
        self.enter_password((By.XPATH, PASSWORD_LOCATOR), password)
        self.click_login((By.XPATH, LOGIN_LOCATOR))

    def check_title(self):
        title = self.get_page_title()
        if title == "OrangeHRM":
            logger.info("Page title is correct.")
        else:
            logger.error("Page title is wrong.")
