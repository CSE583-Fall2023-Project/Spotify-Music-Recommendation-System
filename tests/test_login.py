"""
Unit Testing for User Login Functionality in Spotify Music Exploration/Recommendation System.

This module provides unit tests for the user login functionality, ensuring that
users can log in with valid credentials and receive accurate responses for invalid
attempts. It also tests the user profile update feature post-login.
"""

import unittest
from dash import html
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from utils.pages.login.usermatch import check_user, handle_login, update_user_profile
from utils.database import Base, Users


class TestLogin(unittest.TestCase):
    """
    A TestCase class for testing user login functionalities.

    This class includes methods for setting up a test database environment,
    adding test users, and defining various test cases for user login and
    profile update functionalities.
    """
    @classmethod
    def setUpClass(cls):
        """
        Set up an in-memory SQLite database for testing.

        This method is called once before running the first test. It creates
        a new SQLite in-memory database and sets up the necessary table schemas.
        """
        cls.engine = create_engine('sqlite:///:memory:')  # Use in-memory database for testing
        Base.metadata.create_all(cls.engine)
        cls.Session = sessionmaker(bind=cls.engine)

    def setUp(self):
        """
        Prepare the database session and add test user data before each test.

        This method initializes a new database session and adds a test user
        to the Users table before each test case is run.
        """
        self.session = self.Session()
        self.add_test_data()

    def add_test_data(self):
        """
        Add test user data to the Users table.

        This method clears any existing records and inserts a predefined user
        record for testing the login functionality.
        """
        # Clear tables first to avoid integrity errors
        self.session.query(Users).delete()

        valid_user = Users(
            user_id="id1",
            first_name="Donald",
            last_name="Duck",
            sex="M",
            age=20,
            profile_pic="assets/profile_pics/id1.png"
        )
        self.session.add(valid_user)
        self.session.commit()

    def tearDown(self):
        """
        Rollback the database transaction after each test.

        This method ensures database isolation between tests by rolling back
        any changes made during the test execution.
        """
        self.session.rollback()  # Rollback the transaction
        self.session.close()

    def test_check_user_valid(self):
        """
        Test the functionality of checking for a valid user.

        This test verifies that the check_user function correctly identifies
        a valid user in the database and returns their data.
        """
        user_exists, user_data = check_user("Donald", "Duck", session=self.session)
        self.assertTrue(user_exists)
        self.assertIsNotNone(user_data)
        self.assertEqual(user_data['user_id'], "id1")

    def test_check_user_invalid(self):
        """
        Test the functionality of checking for an invalid user.

        This test ensures that the check_user function correctly returns
        False for a user not present in the database.
        """
        user_exists, user_data = check_user("Mickey", "Mouse", session=self.session)
        self.assertFalse(user_exists)
        self.assertIsNone(user_data)

    def test_handle_login_valid_user(self):
        """
        Test handling login for a valid user.

        This test checks if the handle_login function successfully logs in a
        user with valid credentials.
        """
        login_successful = handle_login(n_clicks=1, first_name="Donald", last_name="Duck", session=self.session)
        self.assertTrue(login_successful)

    def test_handle_login_invalid_user(self):
        """
        Test handling login for an invalid user.

        This test verifies that the handle_login function responds appropriately
        when invalid user credentials are provided, including returning an error
        message and a failed login indication.
        """
        login_response = handle_login(n_clicks=1, first_name="Mickey", last_name="Mouse", session=self.session)

        # Check if login_response is a list and contains expected elements for an invalid login
        self.assertIsInstance(login_response, list)
        self.assertTrue(any(isinstance(elem, html.Div) for elem in login_response))

        # Check for specific messages in the response
        error_message_found = any("User not found" in str(elem) for elem in login_response)
        self.assertTrue(error_message_found, "Expected error message not found in login response")

    def test_update_user_profile(self):
        """
        Test updating the user profile after login.

        This test checks if the update_user_profile function generates the correct
        HTML structure based on the user data provided.
        """
        user_data = {
            'user_id': 'id1',
            'first_name': 'Donald',
            'last_name': 'Duck',
            'age': 20,
            'sex': 'M',
            'profile_pic': 'path/to/profile_pic.png'
        }

        output = update_user_profile(user_data)

        # Check that the output is as expected
        self.assertIsInstance(output, html.Div)
        self.assertEqual(len(output.children), 2)  # Assuming 2 children: image and details
        self.assertIn('user-profile-image', output.children[0].children.className)
        self.assertIn(user_data['first_name'], output.children[1].children[0].children)
        self.assertIn(str(user_data['age']), output.children[1].children[1].children)


if __name__ == '__main__':
    unittest.main()