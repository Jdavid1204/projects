from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from api.models import FriendRequest
from .base_test import BaseSeleniumTest
from api.tests.e2e_tests.test_utils import create_sender_receiver


class TestAcceptFriendRequest(BaseSeleniumTest):
    """
    Tests for accepting a friend request.
    """

    def setUp(self):
        self.sender, self.receiver = create_sender_receiver()
        super().setUp()

    def test_accept_friend_request(self):
        """
        Test accepting a friend request.
        """
        friend_request = FriendRequest.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            status="pending"
        )
        self.assertIsNotNone(friend_request, "Friend request creation failed.")

        self.login_user(email=self.receiver.email, password="User12345")
        WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.ID, "Received-Requests"))
        )

        self.click_button(By.ID, "acceptFriendRequest")
        WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.ID, "Friends-List"))
        )

        friend_request.refresh_from_db()
        self.assertEqual(friend_request.status, "accepted",
                         "Friend request status is not 'accepted'.")

        self.logout_user()
