from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
from django.core.management import call_command


class BaseSeleniumTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        call_command('flush', verbosity=0, interactive=False)
        super().tearDownClass()

    def fill_input_field(self, field_id, value):
        """Utility method to fill input fields by their ID."""
        try:
            field = WebDriverWait(self.selenium, 10).until(
                EC.element_to_be_clickable((By.ID, field_id))
            )
            field.clear()
            field.send_keys(value)
        except Exception as e:
            raise RuntimeError(f"Failed to fill the input field with ID '{field_id}': {e}")

    def click_button(self, by_strategy, locator):
        """Utility method to click a button by its locator."""
        button = WebDriverWait(self.selenium, 10).until(
            EC.element_to_be_clickable((by_strategy, locator))
        )
        button.click()

    def handle_alert(self):
        """Utility method to handle and accept browser alerts."""
        try:
            WebDriverWait(self.selenium, 10).until(EC.alert_is_present())
            alert = self.selenium.switch_to.alert
            alert.accept()
            WebDriverWait(self.selenium, 10).until_not(EC.alert_is_present())
        except Exception as e:
            raise RuntimeError(f"Failed to handle the browser alert: {e}")

    def login_user(self, email, password):
        """Log in as a user using the provided credentials."""
        self.selenium.get(f"{self.live_server_url}/accounts/login/")
        self.fill_input_field("id_email", email)
        self.fill_input_field("id_password", password)
        self.selenium.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        WebDriverWait(self.selenium, 10).until(
            EC.url_to_be(f"{self.live_server_url}/")
        )
        WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.ID, "hobbies"))
        )

    def logout_user(self):
        """Log out current user."""
        self.selenium.get(f"{self.live_server_url}/accounts/logout/")
        WebDriverWait(self.selenium, 10).until(
            EC.url_to_be(f"{self.live_server_url}/accounts/login/")
        )
        WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.ID, "login-form"))
        )
