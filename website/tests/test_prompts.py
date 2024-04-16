from website import create_app, db
import unittest
from website.models import Prompts, UploadedFiles, PromptMessages
from flask import Flask, session, url_for
from config import SQLALCHEMY_DATABASE_URI
from website.prompts import save_file_record, save_prompt_message, read_file, chat
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
import time


class FlaskTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up a test client for all class methods."""
        cls.app = create_app()  # Use your actual function to get the configured Flask app
        cls.app.config['TESTING'] = True  # Ensure TESTING mode is on to not catch exceptions by Flask
        cls.app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI  # Set to production database URI
        cls.client = cls.app.test_client()  # Set up a test client for use in all tests
        cls.app_context = cls.app.app_context()  # Create an app context
        cls.app_context.push()  # Push the app context

    def test_load_prompt(self):
        """Test the load_prompt route."""
        prompt_id = 1  # Example prompt ID
        with self.client as client:
            response = client.get(f'/prompt/load-prompt/{prompt_id}')
            self.assertEqual(response.status_code, 302)  # Check if redirection happens
            self.assertIn('/prompt/chat', response.headers['Location'])

    def test_new_prompt(self):
        """Test the new_prompt route."""
        with self.client as client:
            response = client.get('/prompt/start-new-prompt')
            self.assertEqual(response.status_code, 302)

    def test_new_prompt_creation(self):
        """Test creating a new prompt via POST request to the /chat endpoint."""
        initial_prompt_count = Prompts.query.count()
        response = self.client.post('/prompt/chat', data={'promptText': 'Test new prompt'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Prompts.query.count(), initial_prompt_count + 1)
        new_prompt = Prompts.query.order_by(Prompts.PromptID.desc()).first()
        self.assertIsNotNone(new_prompt)
        self.assertEqual(new_prompt.Name, 'Test new prompt')

    def test_delete_prompt(self):
        """Test deleting a prompt via POST request to the /delete-prompt endpoint."""
        # Create a new prompt to delete
        response = self.client.post('/prompt/chat', data={'promptText': 'Test prompt to delete'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Get the ID of the newly created prompt
        new_prompt = Prompts.query.filter_by(Name='Test prompt to delete').first()
        self.assertIsNotNone(new_prompt)
        prompt_id = new_prompt.PromptID

        # Send a POST request to delete the prompt
        response = self.client.post(f'/prompt/delete-prompt/{prompt_id}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Check if the prompt has been deleted
        deleted_prompt = Prompts.query.get(prompt_id)
        self.assertIsNone(deleted_prompt)

    def test_save_file_record(self):
        """Test saving a file record."""
        # Create a new file record
        filename = 'test_file.txt'
        path = 'test_file.txt'
        user_id = 1
        prompt_id = 1  # Example prompt ID

        # Get the initial count of file records
        initial_file_count = UploadedFiles.query.count()

        # Call the save_file_record method
        save_file_record(filename, path, user_id, prompt_id)

        # Check if the file record has been saved successfully
        new_file_count = UploadedFiles.query.count()
        self.assertEqual(new_file_count, initial_file_count + 1)

        # Retrieve the newly saved file record
        saved_file = UploadedFiles.query.filter_by(FileName=filename, FilePath=path, UserID=user_id,
                                                   PromptID=prompt_id).first()
        self.assertIsNotNone(saved_file)
        self.assertEqual(saved_file.FileName, filename)
        self.assertEqual(saved_file.FilePath, path)
        self.assertEqual(saved_file.UserID, user_id)
        self.assertEqual(saved_file.PromptID, prompt_id)

    def test_save_prompt_message(self):
        """Test saving a prompt message."""
        # Create test data
        text = "Test prompt message"
        response = "Test response"
        prompt_id = 1  # Example prompt ID

        # Get the initial count of prompt messages
        initial_message_count = PromptMessages.query.filter_by(PromptID=prompt_id).count()

        # Call the save_prompt_message method
        save_prompt_message(text, response, prompt_id)

        # Check if the prompt messages have been saved successfully
        new_message_count = PromptMessages.query.filter_by(PromptID=prompt_id).count()
        self.assertEqual(new_message_count, initial_message_count + 2)

        # Retrieve the newly saved prompt messages
        saved_messages = PromptMessages.query.filter_by(PromptID=prompt_id).order_by(
            PromptMessages.MessageID.desc()).limit(2).all()
        self.assertEqual(saved_messages[0].MessageText, response)
        self.assertTrue(saved_messages[0].IsResponse)
        self.assertEqual(saved_messages[1].MessageText, text)
        self.assertFalse(saved_messages[1].IsResponse)

    def test_read_text_file(self):
        """Test reading a text file."""
        content = "This is a test text file."
        with open("test.txt", "w") as file:
            file.write(content)
        self.assertEqual(read_file("test.txt"), content)

    def test_read_pdf_file(self):
        """Test reading a PDF file."""
        # Create a PDF file
        pdf_file_path = "test.pdf"
        create_pdf(pdf_file_path)

        # Test reading the PDF file
        self.assertEqual(read_file("test.pdf"), "Test PDF content\n")

    def test_excessively_long_input_rejected(self):
        """Test that input exceeding 200 characters is rejected."""
        long_input = 'a' * 201  # Generates a string with 201 characters
        response = self.client.post('/prompt/chat', data={'promptText': long_input}, follow_redirects=True)
        self.assertNotEqual(response.status_code, 302, "The input should not be processed.")
        self.assertIn('Input exceeds maximum length of 200 characters', response.data.decode(),
                      "Error message not found.")


def create_pdf(file_path):
    """Creates a PDF file with some text using ReportLab."""
    c = canvas.Canvas(file_path, pagesize=LETTER)
    width, height = LETTER  # Unpack width and height
    c.drawString(100, height - 100, "Test PDF content")  # Position text from the bottom-left corner
    c.showPage()
    c.save()


if __name__ == '__main__':
    unittest.main()
