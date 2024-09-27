import pytest
from unittest.mock import MagicMock, patch
from browsers.chrome_browser import ChromeBrowser
from pages.login_page import LoginPage
from selenium.webdriver.common.by import By


LOGIN_PAGE = "//h6[normalize-space()='Dashboard']"

LOGIN_CREDENTIALS = [
    ("Admin", "admin123", True),   # Valid credentials
    ("InvalidUser", "wrongpass", False),  # Invalid credentials
]


def test_open_browser_and_login_success():
    browser = ChromeBrowser()
    browser.open_browser()
    obj = LoginPage(browser.driver)
    assert "OrangeHRM" in obj.get_page_title()

    obj.login("Admin", "admin123")
    obj.is_element_present((By.XPATH, LOGIN_PAGE)), "Login was not successful"


@pytest.mark.parametrize("username, password, expected", LOGIN_CREDENTIALS)
def test_mock_open_browser_and_login_success(username, password, expected):
    with patch('browsers.chrome_browser.ChromeBrowser') as MockBrowser:
        mock_browser = MockBrowser.return_value
        mock_browser.driver = MagicMock()
        with patch('pages.login_page.LoginPage') as MockLoginPage:
            mock_login_page = MockLoginPage.return_value
            mock_login_page.get_page_title.return_value = "OrangeHRM"
            mock_login_page.is_element_preset.return_value = expected

            mock_browser.open_browser()
            assert "OrangeHRM" in mock_login_page.get_page_title()

            mock_login_page.login(username, password)
            assert mock_login_page.is_element_preset((By.XPATH, LOGIN_PAGE)) == expected, "Login was not successful"
