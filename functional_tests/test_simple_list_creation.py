from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


class NewVisitorTest(FunctionalTest):

    def test_can_start_a_list_for_one_user(self):
        self.browser.get(self.server_url)

        ## He notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, 'h1').text
        self.assertIn('To-Do', header_text)

        ## He is invited to enter a to-do item ##
        inputbox = self.get_item_input_box()
        self.assertEqual(inputbox.get_attribute('placeholder'),
                         'Enter a to-do item')

        ## He types "Buy new drone" into the text box (James wants to pilot a drone)
        inputbox.send_keys('Buy new drone')

        ## When James presses Enter, the page updates to reflect the to-do item.
        ## It reads: '1: Buy new drone' as an item in the list
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy new drone')

        # table = self.browser.find_element(By.ID, 'id_list_table')
        # rows = table.find_elements(By.TAG_NAME, 'tr')
        #
        # self.assertIn('1: Buy new drone', [row.text for row in rows])

        ## James notices a new text box awaits his input, so he enters "Find a cool place to fly new drone"
        inputbox = self.get_item_input_box()
        self.add_list_item('Find a cool place to fly new drone')
        inputbox.send_keys(Keys.ENTER)

        ## The page refreshes and now he sees both of the items he's added to the list
        self.wait_for_row_in_list_table('2: Find a cool place to fly new drone')
        self.wait_for_row_in_list_table('1: Buy new drone')

        # Satisfied that his to-do list is safe, he goes about his day

    def test_multiple_users_can_start_lists_at_different_urls(self):
        ## James starts a new to-do lists
        self.browser.get(self.live_server_url)
        self.add_list_item('Buy new drone')

        ## He notices his list has a unique URL
        james_list_url = self.browser.current_url
        self.assertRegex(james_list_url, '/lists/.+')

        # Now a new user, Candice, comes to the site

        ## Use a new browser session to make sure that no info of James' is coming through from cookies etc
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Candice visits the home page and doesn't see any trace of James' list
        self.browser.get(self.server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy new drone', page_text)
        self.assertNotIn('fly new drone', page_text)

        # Candice starts a new list by entering a new item. She is less interesting than James...
        self.add_list_item('Buy cheese')

        # Candice gets her own unique URL
        candice_list_url = self.browser.current_url
        self.assertRegex(candice_list_url, '/lists/.+')
        self.assertNotEqual(candice_list_url, james_list_url)

        # Checking again, there is no trace of James's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy new drone', page_text)
        self.assertIn('Buy cheese', page_text)

        # Satisfied, they both go back to sleep
