import unittest
from website.auth import custom_generate_password_hash
from werkzeug.security import generate_password_hash
def test_password_hash_correctness():
    password = "test123"
    hashed_password = custom_generate_password_hash(password, method='pbkdf2:sha256')
    assert hashed_password != password
    assert hashed_password == generate_password_hash(password, method='pbkdf2:sha256')

if __name__ == '__main__':
    unittest.main()
