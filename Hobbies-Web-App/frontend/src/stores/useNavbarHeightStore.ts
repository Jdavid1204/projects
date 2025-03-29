import { defineStore } from "pinia";

interface NavbarState {
  height: number;
}

export const useNavbarStore = defineStore("navbar", {
  state: (): NavbarState => ({
    height: 0,
  }),

  actions: {
    setHeight(newHeight: number): void {
      this.height = newHeight;
    },
  },
});
