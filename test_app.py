from run import app
from unittest import TestCase


class FlaskTestCase(TestCase):
    def setUp(self) -> None:
        self.tester = app.test_client(self)

    def tearDown(self) -> None:
        self.tester = None

    def test_index(self):
        response = self.tester.get('/', content_type='html/text')
        self.assertIn(b'Trial and Errror', response.data)

    def test_login(self):
        response = self.tester.get('/login', content_type='html/text')
        self.assertIn(b'Login Required', response.data)

        response = self.tester.post('/login')

