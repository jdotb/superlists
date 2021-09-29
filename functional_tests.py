from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import unittest


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    # helper function
    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element(By.ID, 'id_list_table')
        rows = table.find_elements(By.TAG_NAME, 'tr')
        self.assertIn(row_text, [row.text for row in rows])

    ## James has read about this new hip online to-do app.  He browses to check it out
    def test_can_start_a_list_and_retrieve_it_later(self):

        self.browser.get('http://localhost:8000')

        ## He notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, 'h1').text
        self.assertIn('To-Do', header_text)

        ## He is invited to enter a to-do item ##
        # [REMOVED] > self.browser.find_element(By.ID, 'id_new_item')
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        ## He types "Buy new drone" into the text box (James wants to pilot a drone)
        inputbox.send_keys('Buy new drone')

        ## When James presses Enter, the page updates to reflect the to-do item.
        ## It reads: '1: Buy new drone' as an item in the list
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        self.check_for_row_in_list_table('1: Buy new drone')

        table = self.browser.find_element(By.ID, 'id_list_table')
        rows = table.find_elements(By.TAG_NAME, 'tr')

        #### #### #### #### #### #### EDIT 1 #### #### #### #### #### #### #### #### ####
        # self.assertTrue(
        #     any(row.text == '1: Buy new done' for row in rows),
        #     f"\n\n>>>> FAILURE: New to-do item did not appear in table.\nContents:\t{table.text}")
        #
        # ^^^ REMOVED ^^^ - replaced with line below, because it's much simpler, and we get the same
        #   level of information 'for free'
        #
        #   New failure output:
        #       AssertionError: '1: Buy new drone' not found in ['Buy new drone']
        #
        #   Old failure output:
        #       >>>> FAILURE: New to - do item did not appear in table.
        #           Contents:       [Buy new drone]
        #
        #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### ####

        self.assertIn('1: Buy new drone', [row.text for row in rows])

        ## James notices a new text box awaits his input, so he enters "Find a cool place to fly new drone"
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Find a cool place to fly drone')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        ## The page refreshes and now he sees both of the items he's added to the list
        self.check_for_row_in_list_table('1: Buy new drone')
        self.check_for_row_in_list_table('2: Find a cool place to fly new drone')
        #>>> EDIT 2 #### #### #### #### EDIT 2 ####
        #
        # table = self.browser.find_element(By.ID, 'id_list_table')
        # rows = table.find_elements(By.TAG_NAME, 'tr')
        # self.assertIn('1: Buy new drone', [row.text for row in rows])
        # self.assertIn('2: Find a cool place to fly new drone', [row.text for row in rows])
        #
        #>>> END EDIT 2 #### #### #### #### EDIT 2 ####

        # James ponders whether or not the site will remember his list.  Then, to his surprise, he notices the site
        # has generated a unique URL...just for him
        self.fail('Finish the test!')
        # James notes down the unique url and visits the page - wow! His to-do list is still there!

        # Satisfied that his to-do list is safe, he goes about his day


if __name__ == '__main__':
    unittest.main(warnings='ignore')
