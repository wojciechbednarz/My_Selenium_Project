from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import logging
import csv

logger = logging.getLogger(__name__)


class UsernameTooShortException(Exception):
    """Exception raised when username is too short"""
    logger.error("Please provide username at least 5 character long!")


class PasswordTooShortException(Exception):
    """Exception raised when password is too short."""
    logger.error("Please provide password at least 7 character long!")


class PasswordMustHaveNumberException(Exception):
    """Exception raised when password does not contain a number."""
    logger.error("Please provide password with at least 1 number!")


PIM_TAB_LOCATOR = "//span[@class='oxd-text oxd-text--span oxd-main-menu-item--name'][normalize-space()='PIM']"
ADD_EMPLOYEE_LOCATOR = "//a[normalize-space()='Add Employee']"
LOGIN_DETAILS_LOCAOTR = ".oxd-switch-input.oxd-switch-input--active.--label-right"
FIRST_NAME_LOCATOR = "//input[@placeholder='First Name']"
LAST_NAME_LOCATOR = "//input[@placeholder='Last Name']"
USERNAME_LOCATOR = "(//input[@autocomplete='off'])[1]"
PASSWORD_LOCATOR = "(//input[@type='password'])[1]"
CONFIRM_PASSWORD_LOCATOR = "(//input[@type='password'])[2]"
SAVE_LOCATOR = "//button[normalize-space()='Save']"
TOO_SHORT_USERNAME_LOCATOR = "//span[normalize-space()='Should be at least 5 characters']"
TOO_SHORT_PASSWORD_LOCATOR = "//span[normalize-space()='Should have at least 7 characters']"
MUST_HAVE_NUMBER_PASSWORD_LOCATOR = "//span[normalize-space()='Your password must contain minimum 1 number']"


class PimPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    def _open_add_employee_form(self):
        """Opens the 'Add Employee' form."""
        self.click_element((By.XPATH, PIM_TAB_LOCATOR))
        self.click_element((By.XPATH, ADD_EMPLOYEE_LOCATOR))
        self.click_element((By.CSS_SELECTOR, LOGIN_DETAILS_LOCAOTR))

    def _fill_basic_details(self, first_name, last_name):
        """Fills in the basic details like first and last name."""
        self.find_element((By.XPATH, FIRST_NAME_LOCATOR)).send_keys(first_name)
        self.find_element((By.XPATH, LAST_NAME_LOCATOR)).send_keys(last_name)

    def _validate_username(self, username):
        """Validates the username and logs error if too short."""
        self.find_element((By.XPATH, USERNAME_LOCATOR)).send_keys(username)
        try:
            self.wait_for_the_element_to_be_visible((By.XPATH, TOO_SHORT_USERNAME_LOCATOR), 3)
            raise UsernameTooShortException()
        except TimeoutException:
            logger.info("Username seems valid, proceeding.")

    def _element_visible(self, locator, timeout):
        """Helper function to check if element is visible within a timeout."""
        try:
            self.wait_for_the_element_to_be_visible(locator, timeout)
            return True
        except TimeoutException:
            return False

    def _validate_password(self, password):
        """Validates the password length and number presence."""
        self.enter_text((By.XPATH, PASSWORD_LOCATOR), password)
        if self._element_visible((By.XPATH, TOO_SHORT_PASSWORD_LOCATOR), 3):
            logger.error("Password must be at least 7 characters long.")
        elif self._element_visible((By.XPATH, MUST_HAVE_NUMBER_PASSWORD_LOCATOR), 3):
            logger.error("Password must contain at least 1 number.")
        else:
            logger.info("Password format seems valid, proceeding.")
        self.enter_text((By.XPATH, CONFIRM_PASSWORD_LOCATOR), password)

    def _submit_form(self):
        """Submits the form after validating the password."""
        self.click_element((By.XPATH, SAVE_LOCATOR))

    def add_employee(self, first_name, last_name, username, password):
        self._open_add_employee_form()
        self._fill_basic_details(first_name, last_name)
        self._validate_username(username)
        self.enter_text((By.XPATH, PASSWORD_LOCATOR), password)
        self._validate_password(password)
        self._submit_form()

    def employee_exists(self, param, param1):
        pass

    def add_employees_from_csv(self, csv_file_path):
        with open(csv_file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.add_employee(row["FirstName"], row["LastName"], row["Username"], row["Password"])
                assert self.employee_exists(row["FirstName"], row["LastName"])


