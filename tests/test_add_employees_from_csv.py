from tempfile import NamedTemporaryFile
import pytest
import csv
from pages.pim_page import PimPage
from browsers.chrome_browser import ChromeBrowser
from pages.login_page import LoginPage


@pytest.fixture()
def employees_csv():
    with NamedTemporaryFile(mode="w+", newline='', suffix='.csv', delete=False) as csv_file:
        field_names = ['FirstName', 'LastName', 'Username', 'Password']
        writer = csv.DictWriter(csv_file, fieldnames=field_names)

        writer.writeheader()
        writer.writerow({'FirstName': 'John', 'LastName': 'Doe', 'Username': 'jdoe', 'Password': 'password123'})
        writer.writerow({'FirstName': 'Jane', 'LastName': 'Smith', 'Username': 'jsmith', 'Password': 'password456'})

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


def test_add_employees_from_csv(open_browser_and_navigate_to_pim_page, employees_csv):
    pim_page = open_browser_and_navigate_to_pim_page
    employees_count = pim_page.get_length_of_employees()
    pim_page.add_employees_from_csv(employees_csv.name)
    employees = pim_page.get_all_employees()

    assert len(employees) == employees_count + 2
    assert employees[-2]['FirstName'] == 'John'
    assert employees[-2]['LastName'] == 'Doe'
    assert employees[-1]['FirstName'] == 'Jane'
    assert employees[-1]['LastName'] == 'Smith'


# def add_employees_from_csv(self, csv_file_path):
#     with open(csv_file_path, 'r') as file:
#         reader = csv.DictReader(file)
#         for row in reader:
#             self.add_employee(row["FirstName"], row["LastName"], row["Username"], row["Password"])
#
