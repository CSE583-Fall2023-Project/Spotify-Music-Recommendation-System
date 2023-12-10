"""Test the log-in system"""
import unittest
from dash import html
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from utils.pages.login.usermatch import check_user, handle_login, update_user_profile
from utils.database import Base, Users


class TestLogin(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine('sqlite:///:memory:')  # Use in-memory database for testing
        Base.metadata.create_all(cls.engine)
        cls.Session = sessionmaker(bind=cls.engine)

    def setUp(self):
        self.session = self.Session()
        self.add_test_data()

    def add_test_data(self):
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
        self.session.rollback()  # Rollback the transaction
        self.session.close()

    def test_check_user_valid(self):
        user_exists, user_data = check_user("Donald", "Duck", session=self.session)
        self.assertTrue(user_exists)
        self.assertIsNotNone(user_data)
        self.assertEqual(user_data['user_id'], "id1")

    def test_check_user_invalid(self):
        user_exists, user_data = check_user("Mickey", "Mouse", session=self.session)
        self.assertFalse(user_exists)
        self.assertIsNone(user_data)

    def test_handle_login_valid_user(self):
        login_successful = handle_login(n_clicks=1, first_name="Donald", last_name="Duck", session=self.session)
        self.assertTrue(login_successful)

    def test_handle_login_invalid_user(self):
        login_response = handle_login(n_clicks=1, first_name="Mickey", last_name="Mouse", session=self.session)

        # Check if login_response is a list and contains expected elements for an invalid login
        self.assertIsInstance(login_response, list)
        self.assertTrue(any(isinstance(elem, html.Div) for elem in login_response))

        # Check for specific messages in the response
        error_message_found = any("User not found" in str(elem) for elem in login_response)
        self.assertTrue(error_message_found, "Expected error message not found in login response")

    def test_update_user_profile(self):
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