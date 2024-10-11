import pytest
from tempfile import NamedTemporaryFile
import csv
import tempfile
from pages.pim_page import PimPage
from browsers.chrome_browser import ChromeBrowser
from pages.login_page import LoginPage


@pytest.fixture()
def employees_csv():
    with NamedTemporaryFile(mode="w+", newline='', suffix='.csv', delete=False) as csv_file:
        field_names = ['FirstName', 'LastName', 'Username', 'Password']
        writer = csv.DictWriter(csv_file, fieldnames=field_names)

        writer.writeheader()
        writer.writerow({'FirstName': 'John', 'LastName': 'Doe', 'Username': 'jdoe123', 'Password': 'password123'})
        writer.writerow({'FirstName': 'Jane', 'LastName': 'Smith', 'Username': 'jsmith123', 'Password': 'password456'})

        csv_file.seek(0)
        yield csv_file


@pytest.fixture()
def open_browser_and_navigate_to_pim_page():
    browser = ChromeBrowser()
    browser.open_browser()
    login_page = LoginPage(browser.driver)
    login_page.login("Admin", "admin123")
    login_page.check_title()
    pim_page = PimPage(browser.driver)
    yield pim_page


@pytest.fixture()
def temp_file():
    with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as temp_file:
        temp_file_name = temp_file.name
        yield temp_file_name
