import unittest
from website import db, create_app
from config import SQLALCHEMY_DATABASE_URI

class TestInventory(unittest.TestCase):
    def setUpClass(cls):
        cls.app = create_app()
        cls.app.config['TESTING'] = True
        cls.app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
        cls.client = cls.app.test_client()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_show_inventory(self):
        response = self.client.get('/show-inventory')
        self.assertEqual(response.status_code, 200)

    def test_submit_review(self):
        response = self.client.post('/submit-review',
                                    data={'rating': 5, 'bookTitle': 'The Great Gatsby', 'reviewText': 'Great book!', 'userID': 1})
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
