from app import create_app
from flask_testing import TestCase
import unittest


app = create_app('app.config.TestConfig')

class BaseTestCase(TestCase):
    """A base test case."""

    def create_app(self):
        app.config.from_object("app.config.TestConfig")
        return app

    def setUp(self):
        app.config['SECRET_KEY'] = "you-will-never-guess"

    def tearDown(self):
        pass

class FlaskTestCase(BaseTestCase):

    def test_index(self):
        response = self.client.get('/', content_type='html/text', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'organisations' in response.data)

    def test_closest_organisations(self):
        response = self.client.get('/closestorganisations', content_type='html/text', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Find Closest Organisations' in response.data)

if __name__ == '__main__':
    unittest.main()