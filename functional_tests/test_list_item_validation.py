from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        # # James goes to the home page and accidentally tries to submit an empty list item
        ## - he hits ENTER on the empty input box
        self.browser.get(self.server_url)
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)

        ## The homepage refreshes and shows an error message saying list items can't be blank
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element(By.CSS_SELECTOR, '.has-error').text,
            "Empty list items aren't allowed"
        ))
        ## He tries again with some text, and it now works
        self.browser.find_element(By.ID, 'id_new_item').send_keys('Buy cheese')
        self.browser.find_element(By.ID, 'id_new_item').send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy cheese')

        ## Jokingly, he submits another blank list
        self.browser.find_element(By.ID, 'id_new_item').send_keys(Keys.ENTER)

        ## He receives a similar warning on the list page
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element(By.CSS_SELECTOR, '.has-error').text,
            "Empty list items aren't allowed"
        ))

        ## This can be corrected by filling in some text
        self.browser.find_element(By.ID, 'id_new_item').send_keys('Make lunch for tomorrow')
        self.browser.find_element(By.ID, 'id_new_item').send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy cheese')
        self.wait_for_row_in_list_table('2: Make lunch for tomorrow')
