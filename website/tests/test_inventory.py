import unittest
from website.inventory import show_inventory, submit_review
from website.models import Inventory, Reviews
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
        # Add a book to the inventory
        book = Inventory(Title='Test Book', OwnerID=1)
        db.session.add(book)
        db.session.commit()

        # Submit a review for the book
        response = self.client.post('/submit-review', data={'rating': 5, 'bookTitle': 'Test Book', 'reviewText': 'Great book!'})
        self.assertEqual(response.status_code, 302)  # Expecting a redirect

        # Check that the review was added to the database
        review = Reviews.query.filter_by(BookID=book.BookID).first()
        self.assertIsNotNone(review)
        self.assertEqual(review.Rating, 5)
        self.assertEqual(review.ReviewText, 'Great book!')

if __name__ == '__main__':
    unittest.main()