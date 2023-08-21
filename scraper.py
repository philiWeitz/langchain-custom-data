import time

from chromedriver_py import binary_path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

options = webdriver.ChromeOptions()
options.add_argument("--ignore-certificate-errors")
options.add_argument("--incognito")
# options.add_argument("--headless")

# disable chrome logging
options.add_experimental_option("excludeSwitches", ["enable-logging"])

# don't load images
prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", prefs)


class Scraper:
    def __init__(self):
        self.driver = webdriver.Chrome(binary_path, chrome_options=options)

    def __del__(self):
        self.driver.quit()

    def scroll_to_bottom_of_page(self):
        page_height = self.driver.execute_script(
            "return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight );"
        )

        # Set the scroll step size and delay time
        scroll_step = 100  # Number of pixels to scroll at a time
        delay_time = 0.05  # Delay in seconds between each scroll step

        # Scroll slowly to the bottom of the page
        current_position = 0
        while current_position < page_height:
            self.driver.execute_script(
                f"window.scrollTo(0, {current_position});"
            )
            time.sleep(delay_time)
            current_position += scroll_step

    def get_html_content(self, url):
        self.driver.get(url)

        wait = WebDriverWait(self.driver, 5)

        try:
            # Wait for the page to be fully loaded
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "xxx")))
        except:
            pass

        self.scroll_to_bottom_of_page()
        return self.driver.page_source
