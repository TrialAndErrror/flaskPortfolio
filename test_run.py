from flask_login import current_user

from run import app
from unittest import TestCase
import os


class FlaskTestCase(TestCase):
    def setUp(self) -> None:
        self.tester = app.test_client(self)

    def tearDown(self) -> None:
        self.tester = None

    def check_get(self, route, check_text):
        response = self.tester.get(route, content_type='html/text', follow_redirects=True)
        self.assertTrue(response.status == '200 OK')
        self.assertIn(check_text, response.data)

    def check_post(self, route, data, check_text):
        response = self.tester.post('/login',
                                    data={'username': 'unknown_user', 'password': 'not_a_password'},
                                    follow_redirects=True)
        self.assertIn(b'Username or password was incorrect.', response.data)

    def test_main(self):
        main_urls = [
            ('/', b'Trial and Errror'),
            ('/about', b'Wade\'s areas of expertise include:'),
            ('/wade', b'Technology Educator'),
            ('/wade', b'Employment History'),
            ('/wade', b'Education'),
        ]
        for url, test_text in main_urls:
            self.check_get(url, test_text)

    def test_proj(self):
        proj_urls = [
            ('/projects', b'Current Projects'),
            ('/projects', b'Past Projects')
        ]
        for url, test_text in proj_urls:
            self.check_get(url, test_text)

    def test_auth(self):
        """
        Test the Login Page.

        :return: None
        """

        """
        Load Login Page
        """
        self.check_get('/login', b'Login Required')

        """
        Test for incorrect username/password.
        """
        wrong_creds = {'username': 'unknown_user', 'password': 'not_a_password'}
        self.check_post('/login', wrong_creds, b'Username or password was incorrect.')

        """
        Test for correct username/password.
        """
        right_creds = {'username': os.environ.get('USER'), 'password': os.environ.get('PASS')}
        self.check_post('/login', right_creds, b'Manage Resume')

        """
        Test Logout
        """
        self.check_get('/logout', b'Trial and Errror')


