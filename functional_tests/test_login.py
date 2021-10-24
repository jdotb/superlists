import os
import poplib
import re
import time
from selenium.webdriver.support.ui import WebDriverWait
from django.core import mail
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from .base import FunctionalTest

TEST_EMAIL = 'gametime@example.com'
SUBJECT = 'Your login link for Superlists'


class LoginTest(FunctionalTest):

    def test_login_with_persona(self):
        ## James goes to his superlists sites and can sign in
        self.browser.get(self.server_url)
        self.browser.find_element_by_id('login').click()

        ## A persona login box appears
        self.switch_to_new_window('Mozilla Persona')

        ## James logs in with his email using 'mockmid.com'
        self.browser.find_element_by_id(
            'authentication_email'
        ).send_keys('james@mockmyid.com')
        self.browser.find_element_by_tag_name('button').click()

        ## The persona window closes
        self.switch_to_new_window('To-Do')

        ## He can see that he is logged in
        self.wait_for_element_with_id('logout')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn('james@mockmyid.com', navbar.text)

    def switch_to_new_window(self, text_in_title):
        retries = 60
        while retries > 0:
            for handle in self.browser.window_handles:
                self.browser.switch_to_window(handle)
                if text_in_title in self.browser.title:
                    return
            retries -= 1
            time.sleep(0.5)
        self.fail('could not find window')

    def wait_for_element_with_id(self, element_id):
        WebDriverWait(self.browser, timeout=30).until(
            lambda b: b.find_element_by_id(element_id)
        )

    # def wait_for_email(self, test_email, subject):
    #     if not self.against_staging:
    #         email = mail.outbox[0]
    #         self.assertIn(test_email, email.to)
    #         self.assertEqual(email.subject, subject)
    #         return email.body
    #
    #     subject_line = 'Subject: {}'.format(subject)
    #     email_id = None
    #     start = time.time()
    #     inbox = poplib.POP3_SSL('pop.mail.google.com')
    #     try:
    #         inbox.user(test_email)
    #         inbox.pass_(os.environ['#F55QL*SDNG.u:W+$;g4AsM5|q'])
    #         while time.time() - start < 60:
    #             count, _ = inbox.stat()
    #             for i in reversed(range(max(1, count - 10), count + 1)):
    #                 print('getting msg', i)
    #                 _, lines, __ = inbox.retr(i)
    #                 lines = [l.decode('utf8') for l in lines]
    #                 if subject_line in lines:
    #                     email_id = i
    #                     body = '\n'.join(lines)
    #                     return body
    #             time.sleep(5)
    #     finally:
    #         if email_id:
    #             inbox.dele(email_id)
    #         inbox.quit()
    #
    # def test_can_get_email_link_to_log_in(self):
    #     ## James navigates to his superlists site and notices a "Log in" section in the navbar for the first time
    #     ## It's telling her to enter her email address, so she does
    #     # test_email = 'jdotb@jdotbdotb.com'
    #     if self.against_staging:
    #         TEST_EMAIL = 'bboldspam@gmail.com'
    #     else:
    #         TEST_EMAIL = 'gametime@example.com'
    #
    #     self.browser.get(self.server_url)
    #     self.browser.find_element(By.NAME, 'email').send_keys(TEST_EMAIL)
    #     self.browser.find_element(By.NAME, 'email').send_keys(Keys.ENTER)
    #
    #     ## A message appears telling him an email has been sent
    #     self.wait_for(lambda: self.assertIn(
    #         'Check your email',
    #         self.browser.find_element(By.TAG_NAME, 'body').text
    #     ))
    #
    #     ## He checks his email, and sees he has a message
    #     email = mail.outbox[0]
    #     self.assertIn(TEST_EMAIL, email.to)
    #     self.assertEqual(email.subject, SUBJECT)
    #
    #     ## The message has a URL link
    #     body_search = re.search(r'Use this link to login.+$', email.body)
    #     self.assertTrue('Use this link to login', body_search)
    #     url_search = re.search(r'http://.+/.+$', email.body)
    #     if not url_search:
    #         self.fail(f'Could not find url in email body:\n{email.body}')
    #     url = url_search.group(0)
    #     self.assertIn(self.live_server_url, url)
    #
    #     ## He clicks the link
    #     self.browser.get(url)
    #
    #     ## He is logged in! Hurrah!
    #     self.wait_for(
    #         lambda: self.browser.find_element(By.LINK_TEXT, 'Log out')
    #     )
    #     navbar = self.browser.find_element(By.CSS_SELECTOR, '.navbar')
    #     self.assertIn(TEST_EMAIL, navbar.text)
    #     # He checks his email and finds a message
    #     body = self.wait_for_email(TEST_EMAIL, SUBJECT)
    #
    #     # It has a url link in it
    #     self.assertIn('Use this link to log in', body)
    #     url_search = re.search(r'http://.+/.+$', body)
    #     if not url_search:
    #         self.fail(
    #             'Could not find url in email body:\n{}'.format(body)
    #         )
    #     url = url_search.group(0)
    #     self.assertIn(self.server_url, url)
    #
    #     # he clicks it
    #     self.browser.get(url)
    #
    #     # and he is logged in!!!
    #     self.wait_to_be_logged_in(email=TEST_EMAIL)
    #
    #     # Now he logs out
    #     self.browser.find_element(By.LINK_TEXT, 'Log out').click()
    #
    #     # He is logged out
    #     self.wait_to_be_logged_out(email=TEST_EMAIL)
