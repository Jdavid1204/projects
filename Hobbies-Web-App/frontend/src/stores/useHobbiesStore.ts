import { defineStore } from "pinia";

interface Hobby {
  id: number;
  name: string;
  description: string;
}

interface HobbiesState {
  hobbies: Hobby[];
}

const getCsrfToken = (): string | null => {
  const match = document.cookie.match(/csrftoken=([^;]+)/);
  return match ? match[1] : null;
};

export const useHobbiesStore = defineStore("hobbies", {
  state: (): HobbiesState => ({
    hobbies: [],
  }),

  actions: {
    async fetchHobbies(): Promise<void> {
      const csrfToken = getCsrfToken();
      try {
        const response = await fetch(`/hobbies/`, {
          method: "GET",
          credentials: "include",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken!,
          },
        });

        if (!response.ok) {
          throw new Error(`Failed to fetch hobbies: ${response.status}`);
        }

        const data = await response.json();
        this.hobbies = data.hobbies;
      } catch (error) {
        console.error("Error fetching hobbies:", error);
      }
    },
  },
});
