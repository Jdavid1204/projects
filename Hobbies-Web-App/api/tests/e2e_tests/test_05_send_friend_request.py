import time

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from api.models import FriendRequest
from .base_test import BaseSeleniumTest
from api.tests.e2e_tests.test_utils import create_sender_receiver


class TestSendFriendRequest(BaseSeleniumTest):
    """
    Tests for sending a friend request.
    """

    def setUp(self):
        self.sender, self.receiver = create_sender_receiver()
        super().setUp()

    def test_send_friend_request(self):
        """
        Test sending a friend request.
        """
        self.login_user(email=self.sender.email, password="User12345")
        WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.ID, "Similar-Users"))
        )
        time.sleep(2)

        self.click_button(By.ID, "sendFriendRequest")
        self.handle_alert()

        friend_request = FriendRequest.objects.get(sender=self.sender, receiver=self.receiver)
        self.assertIsNotNone(friend_request, f"Friend request between {self.sender.username} and {self.receiver.username} was not found.")
        self.assertEqual(friend_request.status, "pending",
                         "Friend request status is not 'pending'.")

        self.logout_user()
