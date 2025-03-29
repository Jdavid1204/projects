from .base_test import BaseSeleniumTest
from api.tests.e2e_tests.test_utils import create_user

class TestLogin(BaseSeleniumTest):
    def setUp(self):
        self.user = create_user()
        super().setUp()


    def test_user_login(self):
        """
        Test the login form functionality:
        - Navigate to login page
        - Fill in the form
        - Submit the form
        - logout
        """

        self.login_user(email=self.user.email, password="User12345")
        self.assertEqual(f"{self.live_server_url}/", self.selenium.current_url, "Incorrect redirect.")

        self.logout_user()
        self.assertEqual(f"{self.live_server_url}/accounts/login/", self.selenium.current_url, "Incorrect redirect.")
        
        # Verify that the session cookie is deleted
        cookies = self.selenium.get_cookies()
        session_cookie = next((cookie for cookie in cookies if cookie['name'] == 'sessionid'), None)
        self.assertIsNone(session_cookie, "Session cookie was not deleted after logout.")
