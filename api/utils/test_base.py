import unittest
import tempfile
import os
from main import create_app
from api.utils.database import db
from api.config.config import TestingConfig

class BaseTestCase(unittest.TestCase):
    """ Base test case for all tests """

    def setUp(self):
        # Create temp file for test database
        self.db_fd, self.test_db_file = tempfile.mkstemp()
        
        # Create test app
        self.app = create_app(TestingConfig)
        
        # Configure test database
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + self.test_db_file
        self.app.config['TESTING'] = True
        
        # Create test client
        self.client = self.app.test_client()
        
        # Create app context and tables
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        # Clean up
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        
        # Remove test database
        os.close(self.db_fd)
        os.unlink(self.test_db_file)

if __name__ == '__main__':
    unittest.main()