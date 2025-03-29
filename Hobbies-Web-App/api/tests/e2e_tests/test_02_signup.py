from .base_test import BaseSeleniumTest
from selenium.webdriver.common.by import By
from django.contrib.auth import get_user_model


class TestSignup(BaseSeleniumTest):
    def test_user_signup(self):
        """
        Test the signup form functionality:
        - Navigate to signup page
        - Fill in the form
        - Submit the form
        """
        self.selenium.get(f"{self.live_server_url}/accounts/signup/")

        user = {
            "id_username": "testuser",
            "id_first_name": "Test",
            "id_last_name": "User",
            "id_email": "testuser@example.com",
            "id_date_of_birth": "01012000",
            "id_password1": "User12345",
            "id_password2": "User12345"
        }

        for field_id, value in user.items():
            self.fill_input_field(field_id, value)

        self.click_button(By.CSS_SELECTOR, "button[type='submit']")


        self.assertEqual(f"{self.live_server_url}/", self.selenium.current_url, "Incorrect redirect.")

        # Check the database to ensure the user was created
        custom_user = get_user_model()
        created_user = custom_user.objects.filter(email="testuser@example.com").first()
        self.assertIsNotNone(created_user, "User was not created in the database.")
        self.assertEqual(created_user.username, "testuser", "Username does not match.")
        self.assertEqual(created_user.first_name, "Test", "First name does not match.")
        self.assertEqual(created_user.last_name, "User", "Last name does not match.")

        self.logout_user()
        self.assertEqual(f"{self.live_server_url}/accounts/login/", self.selenium.current_url, "Incorrect redirect.")
