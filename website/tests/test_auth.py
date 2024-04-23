from website import create_app, db
import unittest
from config import SQLALCHEMY_DATABASE_URI

class FlaskLoginTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.app.config['TESTING'] = True
        cls.app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
        cls.client = cls.app.test_client()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()

    def test_login_page_on_get(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('text/html' in response.content_type)

    def test_successful_login(self):
        response = self.client.post('/login', data={
            'email': 'adminadmin@gmail.com',
            'password': 'admin123'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Logged in successfully!', response.get_data(as_text=True))

    def test_failed_login_incorrect_password(self):
        response = self.client.post('/login', data={'email': 'alice@example.com',
            'password': 'w123456'}, follow_redirects=True)
        self.assertIn('Incorrect password, try again.', str(response.data))

    def test_failed_login_no_user(self):
        response = self.client.post('/login', data={'email': 'ww@gmail.com',
            'password': 'w12345'}, follow_redirects=True)
        self.assertIn('Email does not exist.', str(response.data))

    def test_signup_page_on_get(self):
        response = self.client.get('/sign-up')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('text/html' in response.content_type)

    def test_signup_email_already_exists(self):
        response = self.client.post('/sign-up', data={
            'email': 'alice@example.com',
            'username': 'TestUser2',
            'password1': 'password123',
            'password2': 'password123'
        }, follow_redirects=True)
        self.assertIn('Email already exists.', response.get_data(as_text=True))

    def test_signup_username_too_short(self):
        response = self.client.post('/sign-up', data={
            'email': 'uniqueuserr@example.com',
            'username': 'U',
            'password1': 'password123',
            'password2': 'password123'
        }, follow_redirects=True)
        self.assertIn("Username must be greater than 1 character.\n", response.get_data(as_text=True))

    def test_signup_password_too_short(self):
        response = self.client.post('/sign-up', data={
            'email': 'anotheruser@example.com',
            'username': 'AnotherUser',
            'password1': 'pw',
            'password2': 'pw'
        }, follow_redirects=True)
        self.assertIn('Password must be at least 8 characters.', response.get_data(as_text=True))

if __name__ == '__main__':
    unittest.main()


