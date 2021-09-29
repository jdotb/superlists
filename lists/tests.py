from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
import django.core.urlresolvers

from lists.views import home_page


class HomePageTest(TestCase):

    # First added test
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    # Second added test
    def test_home_page_returns_correct_html(self):
        request = HttpRequest()  # HttpRequest object creation
        response = home_page(request)  # request passed to home_page view
        html = response.content.decode('utf8')  # extract content of response and decode and convert to HTML
        self.assertTrue(html.startswith('<html>'), html)  # check page starts with html tag
        self.assertIn('<title>To-Do lists</title>', html)  # check title is 'To-Do list'
        self.assertTrue(html.endswith('</html>'))  # check page ends with closing html tag
