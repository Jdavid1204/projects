from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .base_test import BaseSeleniumTest
from selenium.webdriver.common.by import By
from django.contrib.auth import get_user_model


class TestHobbyFilter(BaseSeleniumTest):
    """
    Tests the user hobbies page filtering functionality.
    """

    def test_user_hobbies(self):
        """
        Test the user hobbies page functionality:
        - Navigate to hobbies page
        - Apply age filters
        - Verify filter results
        """
        custom_user = get_user_model()

        self.user = custom_user.objects.create_user(
            email="pepeg1@example.com",
            username="testuser",
            password="User12345",
            first_name="Test",
            last_name="User",
            date_of_birth="2000-01-01"
        )

        self.oldUser = custom_user.objects.create_user(
            email="oldUser@example.com",
            username="oldUser",
            password="User12345",
            first_name="Old",
            last_name="User",
            date_of_birth="1960-01-01"
        )

        self.youngUser = custom_user.objects.create_user(
            email="youngUser@example.com",
            username="youngUser",
            password="User12345",
            first_name="Young",
            last_name="User",
            date_of_birth="2010-01-01"
        )

        self.login_user(email=self.user.email, password="User12345")

        min_age = 10
        max_age = 20

        self.fill_input_field("minAge", str(min_age))
        self.fill_input_field("maxAge", str(max_age))
        self.click_button(By.ID, "Apply-Filters")

        filtered_user = WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.ID, self.youngUser.username))
        )

        self.assertIsNotNone(filtered_user, "Young user should not have been filtered out")

        min_age = 20
        max_age = 70

        self.fill_input_field("minAge", str(min_age))
        self.fill_input_field("maxAge", str(max_age))
        self.click_button(By.ID, "Apply-Filters")

        filtered_user = WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.ID, self.oldUser.username))
        )

        self.assertIsNotNone(filtered_user, "Old user should not have been filtered out")

        self.logout_user()
