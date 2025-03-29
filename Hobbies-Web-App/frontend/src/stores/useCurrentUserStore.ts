import { defineStore } from "pinia";

interface Hobby {
  id: number;
  name: string;
}

interface FriendRequest {
  id: number;
  sender_id: number;
  sender_username: string;
  receiver_id: number;
  receiver_username: string;
  status: string;
}

interface User {
  id: number | null;
  username: string;
  first_name: string;
  last_name: string;
  email: string;
  password: string;
  date_of_birth: string;
  hobbies: Hobby[];
  friends: User[];
  sent_requests: FriendRequest[];
  received_requests: FriendRequest[];
}

interface CurrentUserState {
  currentUser: User;
  lastFetched: Date | null;
}

const getCsrfToken = (): string | null => {
  const match = document.cookie.match(/csrftoken=([^;]+)/);
  return match ? match[1] : null;
};

export const useCurrentUserStore = defineStore("currentUser", {
  state: (): CurrentUserState => ({
    currentUser: {
      id: null,
      username: "",
      first_name: "",
      last_name: "",
      email: "",
      password: "",
      date_of_birth: "",
      hobbies: [],
      friends: [],
      sent_requests: [],
      received_requests: [],
    },
    lastFetched: null,
  }),

  getters: {
    isLoggedIn: (state): boolean => state.currentUser.id !== null,
  },

  actions: {
    async fetchCurrentUser(): Promise<void> {
      const csrfToken = getCsrfToken();
      try {
        const response = await fetch(
          `/users/user-info/`,
          {
            method: "GET",
            credentials: "include",
            headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": csrfToken!,
            },
          }
        );

        if (response.redirected) {
          this.currentUser = {
            id: null,
            username: "",
            first_name: "",
            last_name: "",
            email: "",
            password: "",
            date_of_birth: "",
            hobbies: [],
            friends: [],
            sent_requests: [],
            received_requests: [],
          };
          this.lastFetched = new Date();
          return;
        }

        if (!response.ok) {
          throw new Error(`Unexpected error: ${response.status}`);
        }

        const data = await response.json();
        this.currentUser = data.user;
        this.lastFetched = new Date();
      } catch (error) {
        console.error("Unexpected error fetching current user:", error);
      }
    },

    async requireAuthentication(): Promise<void> {
      if (
        !this.isLoggedIn &&
        (!this.lastFetched ||
          new Date().getTime() - this.lastFetched.getTime() > 60000)
      ) {
        await this.fetchCurrentUser();
      }
    },

    async updateCurrentUser(updatedUser: Partial<User>): Promise<void> {
      try {
        const response = await fetch(
          `/users/update/`,
          {
            method: "PATCH",
            credentials: "include",
            headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": getCsrfToken()!,
            },
            body: JSON.stringify(updatedUser),
          }
        );

        if (!response.ok) {
          throw new Error("Failed to update user");
        }

        const updatedData = await response.json();
        this.currentUser = {
          ...this.currentUser,
          ...updatedData.user,
          hobbies: updatedData.user.hobbies || this.currentUser.hobbies,
        };
      } catch (error) {
        console.error("Error updating user:", error);
      }
    },

    async addHobby(hobbyName: string): Promise<void> {
      try {
        const response = await fetch(
          `/hobbies/add/`,
          {
            method: "POST",
            credentials: "include",
            headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": getCsrfToken()!,
            },
            body: JSON.stringify({ name: hobbyName }),
          }
        );

        if (!response.ok) {
          throw new Error("Failed to add hobby");
        }

        const data = await response.json();
        this.currentUser.hobbies.push({
          id: data.hobby_id,
          name: data.hobby_name,
        });
      } catch (error) {
        console.error("Error adding hobby:", error);
      }
    },

    async removeHobby(hobbyId: number): Promise<void> {
      try {
        const response = await fetch(
          `/users/hobbies/delete/${hobbyId}/`,
          {
            method: "DELETE",
            credentials: "include",
            headers: {
              "X-CSRFToken": getCsrfToken()!,
            },
          }
        );

        if (!response.ok) {
          throw new Error("Failed to remove hobby");
        }

        this.currentUser.hobbies = this.currentUser.hobbies.filter(
          (hobby) => hobby.id !== hobbyId
        );
      } catch (error) {
        console.error("Error removing hobby:", error);
      }
    },

    async logout(): Promise<void> {
      try {
        const response = await fetch(
          `/accounts/logout/`,
          {
            method: "GET",
            credentials: "include",
            headers: {
              "X-CSRFToken": getCsrfToken()!,
            },
          }
        );

        if (!response.ok) {
          throw new Error("Failed to logout");
        }
        window.location.href = "/";
      } catch (error) {
        console.error("Error logging out:", error);
        alert("Failed to logout. Please try again.");
      }
    },
  },
});
