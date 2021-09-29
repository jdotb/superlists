from django.test import TestCase
# from django.http import HttpRequest
# ^ REMOVED since using self.client.get()

"""
class HomePageTest(TestCase):

    # First added test
    # def test_root_url_resolves_to_home_page_view(self):
    #     found = resolve('/')
    #     self.assertEqual(found.func, home_page)
    # ^ REMOVED - this is tested implicitly via Django Test Client

    # Second added test
    def test_home_page_returns_correct_html(self):
        # request = HttpRequest()  # HttpRequest object creation
        # response = home_page(request)  # request passed to home_page view
        # ^ REMOVED (replaced with Django Test Client tool self.client.get('/')

        response = self.client.get('/')

        html = response.content.decode('utf8')  # extract content of response and decode and convert to HTML

        # self.assertTrue(html.startswith('<!DOCTYPE html>'), html)  # check page starts with html tag
        # self.assertIn('<title>To-Do lists</title>', html)  # check title is 'To-Do list'
        # self.assertTrue(html.strip().endswith('</html>'))  # check page ends with closing html tag

        # expected_html = render_to_string('home.html')
        # self.assertEqual(html, expected_html)
        # ^ REMOVED, replaced with assertTemplatedUsed method
        self.assertTemplateUsed(response, 'home.html')
"""


class HomePageTest(TestCase):
    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')
