from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
import time
import os

MAX_WAIT = 10


class FunctionalTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server

    def tearDown(self):
        self.browser.quit()

    # helper function
    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element(By.ID, 'id_list_table')
                rows = table.find_elements(By.TAG_NAME, 'tr')
                self.assertIn(row_text, [row.text for row in rows])
                # Escape #1: If out assertions pass, return from function and exit loop
                return
            ###----
            # If we catch an exception, wait short time and loop around to retry
            # Catch two exceptions:
            # WebDriverException: page hasn't loaded and Selenium can't find table element
            # AssertionError:     when table is there, but doesn't have what we're looking for
            ###----
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    # Escape #2: If we get here, code kept raising exceptions until we exceeded our MAX_WAIT
                    raise e
                time.sleep(0.5)