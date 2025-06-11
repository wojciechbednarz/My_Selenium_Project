from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from browsers.base_browser import BaseBrowser
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.common.exceptions import WebDriverException, TimeoutException


class ChromeBrowser(BaseBrowser):
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-search-engine-choice-screen')
        chrome_options.add_experimental_option("detach", True)
        # Option for failed to read descriptor from node connection issue.
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        service = ChromeService(ChromeDriverManager().install())
        super().__init__(driver_path=None,
                         base_url="https://opensource-demo.orangehrmlive.com",
                         service_class=ChromeService,
                         options=chrome_options)
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

    def open_browser(self, timeout=10):
        try:
            self.driver.get(self.base_url)
            self.driver.maximize_window()

            # Wait until the page is fully loaded
            WebDriverWait(self.driver, timeout).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
        except (WebDriverException, TimeoutException) as e:
            raise Exception("Failed to open or fully load the browser") from e
