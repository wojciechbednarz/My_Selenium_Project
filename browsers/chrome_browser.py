from browsers.base_browser import BaseBrowser
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.common.exceptions import WebDriverException


class ChromeBrowser(BaseBrowser):
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-search-engine-choice-screen')
        chrome_options.add_experimental_option("detach", True)
        # Option for failed to read descriptor from node connection issue.
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        super().__init__(driver_path='drivers/chromedriver.exe',
                         base_url="https://opensource-demo.orangehrmlive.com/web/index.php/auth/login",
                         service_class=ChromeService,
                         options=chrome_options)
        self.driver = webdriver.Chrome(service=self.service, options=self.options)

    def open_browser(self):
        try:
            self.driver.get(self.base_url)
            self.driver.maximize_window()
        except WebDriverException as e:
            raise Exception("Failed to open the browser") from e
