from browsers.base_browser import BaseBrowser
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import pytest

def test_field_access():
    browser = BaseBrowser(
        driver_path=r"C:\Users", base_url="https://www.google.com",
        service_class=Service, options=webdriver.ChromeOptions)
    assert browser.driver is None
    assert browser.driver_path == r"C:\Users"
    assert browser.base_url == "https://www.google.com"
    assert browser.options == webdriver.ChromeOptions


def test_equality():
    b1 = BaseBrowser(
        driver_path=r"C:\Users", base_url="https://www.google.com",
        service_class=Service, options=webdriver.ChromeOptions)
    b2 = BaseBrowser(
        driver_path=r"C:\Users", base_url="https://www.google.com",
        service_class=Service, options=webdriver.ChromeOptions)
    assert b1 == b2


def test_inequality():
    b1 = BaseBrowser(
        driver_path=r"D:\Users", base_url="https://www.google.com",
        service_class=Service, options=webdriver.ChromeOptions)
    b2 = BaseBrowser(
        driver_path=r"C:\Users", base_url="https://www.google.com",
        service_class=Service, options=webdriver.ChromeOptions)
    assert b1 != b2


def test_parameters():
    with pytest.raises(TypeError) as exc:
        BaseBrowser(base_url="https://www.google.com")
    expected = "missing 3 required positional arguments"
    assert expected in str(exc.value)


