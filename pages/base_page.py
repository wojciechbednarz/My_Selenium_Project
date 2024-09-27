import logging
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logger = logging.getLogger(__name__)


class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def wait_for_the_element_to_be_visible(self, locator, timeout):
        return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))

    def wait_for_the_element_to_be_clickable(self, locator, timeout):
        return WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator))

    def is_element_present(self, locator):
        try:
            self.driver.find_element(*locator)
        except NoSuchElementException:
            return False
        return True

    def find_element(self, locator):
        try:
            return self.driver.find_element(*locator)
        except TimeoutException:
            logger.error(f"Timeout while waiting for locator: {locator}")
        except Exception as e:
            logging.error(f"An error occurred while finding element: {locator}: {e}")

    def find_elements(self, locator):
        try:
            return self.driver.find_elements(*locator)
        except TimeoutException:
            logger.error(f"Timeout while waiting for locator: {locator}")
        except Exception as e:
            logging.error(f"An error occurred while finding element: {locator}: {e}")

    def click_element(self, locator):
        """Click an element identified by the given locator."""
        try:
            if self.wait_for_the_element_to_be_visible(locator, 10):
                self.driver.find_element(*locator).click()
            else:
                logging.error(f"Couldn't find the element with locator: {locator}")
        except TimeoutException:
            logger.error(f"Timeout while waiting for locator: {locator}")
        except Exception as e:
            logger.error(f"An error occurred while clicking on locator {locator}: {e}")

    def enter_text(self, locator, text):
        """Enter text into an element identified by the given locator."""
        try:
            if self.wait_for_the_element_to_be_visible(locator, 10):
                self.driver.find_element(*locator).send_keys(text)
            else:
                logger.error(f"Couldn't find provided locator: {locator}")
        except TimeoutException:
            logger.error("Timeout while waiting for locator: {locator}")
        except Exception as e:
            logger.error(f"An error occurred while entering text for locator {locator}: {e}")

    def get_page_title(self):
        return self.driver.title

    def open_browser(self, url):
        try:
            self.driver.get(url)
            self.driver.maximize_window()
        except WebDriverException as e:
            raise Exception("Failed to open the browser") from e

    def check_if_text_field_contains_any_text(self, locator):
        try:
            text = self.driver.find_element(*locator).get_attribute('value')
            if text:
                return True
            return False
        except NoSuchElementException as e:
            logger.error(f"Element not found: {e}")
        except TimeoutException as e:
            logger.error(f"Timeout: {e}")
