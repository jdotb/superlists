from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
import time
import unittest

MAX_WAIT = 10


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

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

    ## START USER STORY - JAMES
    ## James has read about this new hip online to-do app.  He browses to check it out
    def test_can_start_a_list_for_one_user(self):
        self.browser.get(self.live_server_url)

        ## He notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, 'h1').text
        self.assertIn('To-Do', header_text)

        ## He is invited to enter a to-do item ##
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')

        ## He types "Buy new drone" into the text box (James wants to pilot a drone)
        inputbox.send_keys('Buy new drone')

        ## When James presses Enter, the page updates to reflect the to-do item.
        ## It reads: '1: Buy new drone' as an item in the list
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy new drone')

        table = self.browser.find_element(By.ID, 'id_list_table')
        rows = table.find_elements(By.TAG_NAME, 'tr')

        self.assertIn('1: Buy new drone', [row.text for row in rows])

        ## James notices a new text box awaits his input, so he enters "Find a cool place to fly new drone"
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Find a cool place to fly new drone')
        inputbox.send_keys(Keys.ENTER)

        ## The page refreshes and now he sees both of the items he's added to the list
        self.wait_for_row_in_list_table('1: Buy new drone')
        self.wait_for_row_in_list_table('2: Find a cool place to fly new drone')

        # Satisfied that his to-do list is safe, he goes about his day

    def test_multiple_users_can_start_lists_at_different_urls(self):
        ## James starts a new to-do lists
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Buy new drone')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy new drone')

        ## He notices his list has a unique URL
        james_list_url = self.browser.current_url
        self.assertRegex(james_list_url, '/lists/.+')

        # Now a new user, Candice, comes to the site

        ## Use a new browser session to make sure that no info of James's is coming through from cookies etc
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Candice visits the home page. There is no sign of James's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy new drone', page_text)
        self.assertNotIn('fly new drone', page_text)

        # Candice starts a new list by entering a new item. She is less interesting than James...
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy cheese')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy cheese')

        # Candice gets her own unique URL
        candice_list_url = self.browser.current_url
        self.assertRegex(candice_list_url, '/lists/.+')
        self.assertNotEqual(candice_list_url, james_list_url)

        # Again, there is no trace of James's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy new drone', page_text)
        self.assertIn('Buy cheese', page_text)

        # Satisfied, they both go back to sleep
