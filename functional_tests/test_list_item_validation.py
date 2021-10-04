from selenium.webdriver.common.keys import Keys
from unittest import skip
from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):

    @skip
    def test_cannot_add_empty_list_items(self):
        ## James goes to the home page and accidently tries to submit an empty list item - hits ENTER on the empty input

        ## The homepage refreshes and shows an error message saying list items can't be blank

        ## He tries again with some text, and it now works

        ## Jokingly, he submits another blank list

        ## He receives a similar warning on the list page

        ## This can be corrected by filling in some text
        self.fail("Finish this test!")