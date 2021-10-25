from django.conf import settings
from .base import FunctionalTest
from .server_tools import create_session_on_server
from .management.commands.create_session import create_pre_authenticated_session
from selenium.webdriver.common.by import By


class MyListsTest(FunctionalTest):

    def create_pre_authenticated_session(self, email):
        if self.against_staging:
            session_key = create_session_on_server(self.server_host, email)
        else:
            session_key = create_pre_authenticated_session(email)

        ## to set a cookie we need to first visit the domain.
        ## 404 pages load the quickest!
        self.browser.get(self.server_url + "/404_no_such_url/")
        self.browser.add_cookie(dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session_key,
            path='/',
        ))

    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        # James is a logged-in user
        self.create_pre_authenticated_session('gametime@example.com')

        # She goes to the home page and starts a list
        self.browser.get(self.server_url)
        self.add_list_item('Fresh list item')
        self.add_list_item('Learn ansible')
        first_list_url = self.browser.current_url

        # He notices a "My lists" link, he's never seen this before..
        self.browser.find_element(By.LINK_TEXT('My Lists')).click()

        # He notices his list, which is named his first list item
        self.wait_for(
            lambda: self.browser.find_element(By.LINK_TEXT, 'Fresh list item')
        )
        self.browser.find_element(By.LINK_TEXT, 'Fresh list item').click()
        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, first_list_url)
        )

        # Just to see what happens, James starts a new list
        self.browser.get(self.server_url)
        self.add_list_item('Get a job')
        second_list_url = self.browser.current_url

        # Now, under 'my lists' he sees his new list
        self.browser.find_element(By.LINK_TEXT, 'My lists').click()
        self.wait_for(
            lambda: self.browser.find_element(By.LINK_TEXT,'Get a job!')
        )
        self.browser.find_element(By.LINK_TEXT, 'Get a job!').click()
        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, second_list_url)
        )

        # He logs out and the 'my lists' option goes away
        self.browser.find_element(By.LINK_TEXT, 'Log out)').click()
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_elements(By.LINK_TEXT, 'My lists'),
            []
        ))
