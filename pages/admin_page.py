from pages.base_page import BasePage
from selenium.webdriver.common.by import By
import logging

logger = logging.getLogger(__name__)

ADMIN_TAB_LOCATOR = "//a[@class='oxd-main-menu-item' and .//span[text()='Admin']]"
USERS_TABLE_CONTAINER = "//div[@class='orangehrm-container']"
TABLE_ROWS = "//div[@class='oxd-table-card']/descendant::div[@class='oxd-table-cell oxd-padding-cell'][2]"
USERS = {}


class AdminPage(BasePage):
    def __init__(self, driver):
        self.driver = driver
        super().__init__(driver)

    def navigate_to_admin_tab(self):
        self.click_element((By.XPATH, ADMIN_TAB_LOCATOR))

    def count_and_save_users(self):
        table = self.wait_for_the_element_to_be_visible((By.XPATH, USERS_TABLE_CONTAINER), 10)
        if table:
            self.wait_for_the_element_to_be_visible((By.XPATH, TABLE_ROWS), 10)
            elements = self.find_elements((By.XPATH, TABLE_ROWS))
            for idx, elem in enumerate(elements):
                USERS[idx + 1] = elem.text
            logger.info(f"Total number of users: {len(USERS)}, usernames: {', '.join(USERS.values())}")
