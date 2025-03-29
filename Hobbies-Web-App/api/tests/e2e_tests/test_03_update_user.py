from selenium.common import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait

from .base_test import BaseSeleniumTest
from selenium.webdriver.common.by import By
from api.models import Hobby
from selenium.webdriver.support import expected_conditions as EC
from api.tests.e2e_tests.test_utils import create_user


class TestUpdateUser(BaseSeleniumTest):
    def setUp(self):
        self.user = create_user()
        super().setUp()


    def test_update_user(self):
        """
        Test updating a user profile by adding and removing a hobby.
        """
        # Log in as the test user
        self.login_user(email=self.user.email, password="User12345")

        # Navigate to the profile page
        self.click_button(By.ID, "profileLink")

        # Update user profile fields
        user_updates = {
            "username": "usertest",
            "first_name": "User",
            "last_name": "Test",
            "email": "usertest@example.com",
            "dateOfBirth": "12121990",
            "password": "Test12345",
        }

        for field_id, value in user_updates.items():
            self.fill_input_field(field_id, value)

        # Add a new hobby
        self.fill_input_field("newHobby", "Gardening")
        self.click_button(By.ID, "addHobbyButton")

        # Submit the changes
        self.click_button(By.CSS_SELECTOR, "button[type='submit']")
        self.handle_alert()

        self.user.refresh_from_db()

        # Verify the user profile fields were updated
        self.assertEqual(self.user.username, "usertest")
        self.assertEqual(self.user.first_name, "User")
        self.assertEqual(self.user.last_name, "Test")
        self.assertEqual(self.user.email, "usertest@example.com")
        self.assertEqual(self.user.date_of_birth.strftime("%d%m%Y"), "12121990")

        # Verify hobby was added to the database
        hobby = Hobby.objects.filter(name="Gardening").first()
        self.assertIsNotNone(hobby, "Hobby was not added to the database.")
        self.assertIn(hobby, self.user.hobbies.all(), "Hobby was not added to the user's hobby list.")

        # Verify hobby was added to user's hobby list
        hobbies = self.user.hobbies.all()
        self.assertIn("Gardening", [hobby.name for hobby in hobbies],
                      "Hobby 'Gardening' was not added to the user's hobby list.")

        # Verify hobby was added to UI
        try:
            WebDriverWait(self.selenium, 10).until(
                EC.presence_of_element_located((By.ID, "Gardening"))
            )
            hobby = self.selenium.find_element(By.ID, "Gardening").text
            self.assertIn("Gardening", hobby, "Hobby was not added successfully.")
        except TimeoutException:
            self.fail("Hobby 'Gardening' was not found in the UI within the timeout period.")

        # Remove the hobby
        self.click_button(By.ID, "removeHobbyButton")
        self.click_button(By.CSS_SELECTOR, "button[type='submit']")
        self.handle_alert()

        # Verify hobby was removed from user's hobby list
        hobbies = self.user.hobbies.all()
        self.assertNotIn("Gardening", [hobby.name for hobby in hobbies],
                      "Hobby 'Gardening' was not added to the user's hobby list.")

        # Verify hobby was removed from UI
        hobby_elements = self.selenium.find_elements(By.ID, "Gardening")
        self.assertFalse(hobby_elements, "Hobby was not removed successfully.")

        self.logout_user()
