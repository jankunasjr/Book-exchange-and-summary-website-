import unittest
from website import db, create_app

class TestInventory(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_show_inventory(self):
        response = self.client.get('/show-inventory')
        self.assertEqual(response.status_code, 200)

    def test_submit_review(self):
        response = self.client.post('/submit-review',
                                    data={'rating': 5, 'bookTitle': 'Test Book', 'reviewText': 'Great book!',
                                          'userID': 1})
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
