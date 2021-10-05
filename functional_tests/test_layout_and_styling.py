from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from unittest import skip
from .base import FunctionalTest

#TODO: Remember this is skipped
@skip
class LayoutAndStylingTest(FunctionalTest):
    def test_layout_and_styling(self):
        # James browses to the home page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # He sees the input box is centered
        # inputbox = self.browser.find_element_by_id('id_new_item')
        # self.assertAlmostEqual(
        #     inputbox.location['x'] + inputbox.size['width'] / 2,
        #     512,
        #     delta=10
        # )

        # He begins a new list and sees the input is centered there as well
        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: testing')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )