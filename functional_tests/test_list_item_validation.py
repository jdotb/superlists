from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        # # James goes to the home page and accidentally tries to submit an empty list item
        ## - he hits ENTER on the empty input box
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)

        ## The browser intercepts the request, and does not load the list page
        ## Instead of checking for our custom error message, we check the CSS pseudoselector :invalid
        ## which the browser applies to any HTML5 input that has invalid input
        self.wait_for(lambda: self.browser.find_element(By.CSS_SELECTOR,
                                                        '#id_text:invalid'))
        ## He tries again with some text, and it now works
        self.get_item_input_box().send_keys('Buy cheese')
        self.wait_for(lambda: self.browser.find_element(By.CSS_SELECTOR,
                                                        '#id_text:valid'))

        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy cheese')

        ## Jokingly, he submits another blank list
        self.get_item_input_box().send_keys(Keys.ENTER)

        ## He receives a similar warning on the list page
        self.wait_for_row_in_list_table('1: Buy cheese')
        self.wait_for(lambda: self.browser.find_element(By.CSS_SELECTOR,
                                                        '#id_text:invalid'))

        ## This can be corrected by filling in some text
        self.get_item_input_box().send_keys('Make lunch for tomorrow')
        self.wait_for(lambda: self.browser.find_element(By.CSS_SELECTOR,
                                                        '#id_text:valid'))
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy cheese')
        self.wait_for_row_in_list_table('2: Make lunch for tomorrow')

    def test_cannot_add_duplicate_items(self):
        ## James goes to the home page and starts a new list
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys('Buy chocolate')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy chocolate')

        ## He accidentally enters 'Buy chocolate' again
        self.get_item_input_box().send_keys('Buy chocolate')
        self.get_item_input_box().send_keys(Keys.ENTER)

        ## He sees an error message
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element(By.CSS_SELECTOR, '.has-error').text,
            "You've already added this to your list!"
        ))
