from pages.login_page import LoginPage
from pages.admin_page import AdminPage
from pages.pim_page import PimPage
from browsers.chrome_browser import ChromeBrowser
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
EMPLOYEES_CSV_FILE_PATH = 'data/employees.csv'

def main():
    browser = ChromeBrowser()
    browser.open_browser()

    login_page = LoginPage(browser.driver)
    login_page.login("Admin", "admin123")
    login_page.check_title()

    admin_page = AdminPage(browser.driver)
    admin_page.navigate_to_admin_tab()
    admin_page.count_and_save_users()

    pim_page = PimPage(browser.driver)
    pim_page.add_employee("Adam", "Kowalski", "akowal", "abcdefgh1")
    pim_page.get_all_employees()

    pim_page.add_employees_from_csv(EMPLOYEES_CSV_FILE_PATH)


if __name__ == "__main__":
    main()
