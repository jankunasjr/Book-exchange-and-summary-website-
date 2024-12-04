import unittest
from website import create_app


class TestSubmitReview(unittest.TestCase):
    def setUp(self):
        app = create_app()
        self.app = app.test_client()
        self.app.testing = True

    def test_submit_review(self):
        with self.app as c:
            response = c.post('/submit-review',
                              data={'rating': 6, 'bookTitle': 'Test Book', 'reviewText': 'Test Review', 'userID': 1})
            self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()
