import { defineStore } from "pinia";

interface User {
  id: number;
  username: string;
  age?: number;
  similar_hobbies_count?: number;
  common_hobbies?: string[];
}

interface FriendRequest {
  id: number;
  sender_id: number;
  sender_username: string;
  receiver_id: number;
  receiver_username: string;
  status: string;
}

interface UsersState {
  users: User[];
  totalUsers: number;
  pendingRequests: FriendRequest[];
  user: User | null;
}

const getCsrfToken = (): string | null => {
  const match = document.cookie.match(/csrftoken=([^;]+)/);
  return match ? match[1] : null;
};

export const useUsersStore = defineStore("users", {
  state: (): UsersState => ({
    users: [],
    totalUsers: 0,
    pendingRequests: [],
    user: null,
  }),

  actions: {
    async fetchUser(userId: number): Promise<void> {
      const csrfToken = getCsrfToken();
      try {
        const response = await fetch(`/users/user-info/${userId}/`, {
          method: "GET",
          credentials: "include",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken!,
          },
        });

        if (!response.ok) {
          throw new Error(`Failed to fetch user: ${response.status}`);
        }

        const data = await response.json();
        this.user = data.user;
      } catch (error) {
        console.error("Error fetching user data:", error);
      }
    },

    async fetchSimilarUsers(min_age?: number, max_age?: number): Promise<void> {
      const csrfToken = getCsrfToken();
      try {
        const response = await fetch(
          `/users/similar/?min_age=${min_age ?? ""}&max_age=${max_age ?? ""}`,
          {
            method: "GET",
            headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": csrfToken!,
            },
            credentials: "include",
          }
        );

        if (response.redirected || response.status === 403) {
          console.warn("User not authenticated. Redirecting to login.");
          window.location.href = "/login/";
          return;
        }

        if (!response.ok) {
          throw new Error("Failed to fetch similar users");
        }

        const data = await response.json();
        this.users = data.similar_users.map((user: any) => ({
          id: user.id,
          username: user.username,
          age: user.age,
          similar_hobbies_count: user.similarity,
          common_hobbies: user.common_hobbies,
        }));
        this.totalUsers = this.users.length;
      } catch (error) {
        console.error("Error fetching similar users:", error);
      }
    },

    async sendFriendRequest(receiverId: number): Promise<void> {
      const csrfToken = getCsrfToken();
      try {
        const response = await fetch(`/users/request/${receiverId}/`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken!,
          },
          credentials: "include",
        });

        if (!response.ok) {
          throw new Error("Failed to send friend request");
        }

        console.log("Friend request sent successfully");
      } catch (error) {
        console.error("Error sending friend request:", error);
      }
    },

    async acceptFriendRequest(requestId: number): Promise<void> {
      const csrfToken = getCsrfToken();
      try {
        const response = await fetch(
          `
            /users/request/accept/${requestId}/`,
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": csrfToken!,
            },
            credentials: "include",
          }
        );

        if (!response.ok) {
          throw new Error("Failed to accept friend request");
        }

        console.log("Friend request accepted successfully");
        await this.fetchPendingRequests();
      } catch (error) {
        console.error("Error accepting friend request:", error);
      }
    },

    async declineFriendRequest(requestId: number): Promise<void> {
      const csrfToken = getCsrfToken();
      try {
        const response = await fetch(`/users/request/decline/${requestId}/`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken!,
          },
          credentials: "include",
        });

        if (!response.ok) {
          throw new Error("Failed to decline friend request");
        }

        console.log("Friend request declined successfully");
        await this.fetchPendingRequests();
      } catch (error) {
        console.error("Error declining friend request:", error);
      }
    },

    async fetchPendingRequests(): Promise<void> {
      console.log("Fetching pending requests...");
    },
  },
});
