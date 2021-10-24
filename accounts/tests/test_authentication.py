from django.test import TestCase
from django.contrib.auth import get_user_model
from accounts.authentication import PasswordlessAuthenticationBackend
from accounts.models import Token

User = get_user_model()


class AuthenticateTest(TestCase):

    def test_creates_new_user_if_necessary_for_valid_assertion(self, mock_post):
        mock_post.return_value.json.return_value = {'status': 'okay', 'email': 'a@b.com'}
        found_user = self.backend.authenticate('an assertion')
        new_user = User.objects.get(email='a@b.com')
        self.assertEqual(found_user, new_user)

    def test_returns_None_if_no_such_token(self):
        result = PasswordlessAuthenticationBackend().authenticate(
            'no-such-token'
        )
        self.assertIsNone(result)

    def test_returns_new_user_with_correct_email_if_token_exists(self):
        email = 'gametime@example.com'
        token = Token.objects.create(email=email)
        user = PasswordlessAuthenticationBackend().authenticate(token.uid)
        new_user = User.objects.get(email=email)
        self.assertEqual(user, new_user)

    def test_returns_existing_user_with_correct_email_if_token_exists(self):
        email = 'gametime@example.com'
        existing_user = User.objects.create(email=email)
        token = Token.objects.create(email=email)
        user = PasswordlessAuthenticationBackend().authenticate(token.uid)
        self.assertEqual(user, existing_user)


class GetUserTest(TestCase):

    def test_gets_user_by_email(self):
        User.objects.create(email='diff_email@example.com')
        desired_user = User.objects.create(email='gametime@example.com')
        found_user = PasswordlessAuthenticationBackend().get_user(
            'gametime@example.com'
        )
        self.assertEqual(found_user, desired_user)

    def test_returns_None_if_no_user_with_that_email(self):
        self.assertIsNone(
            PasswordlessAuthenticationBackend().get_user('gametime@example.com')
        )
