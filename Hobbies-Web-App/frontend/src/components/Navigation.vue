<template>
    <div class="row navbar" ref="navbar">
        <nav class="col-12">
            <ul class="nav justify-content-end">
                <li v-if="isLoggedIn" class="nav-item mx-2 hover-scale">
                    <router-link class="nav-link rounded" :to="{ name: 'Hobbies Page' }" id="hobbiesLink">
                        Hobbies
                    </router-link>
                </li>

                <li v-if="isLoggedIn" class="nav-item mx-2 hover-scale">
                    <router-link class="nav-link rounded" :to="{ name: 'Profile Page' }" id="profileLink">
                        Profile
                    </router-link>
                </li>

                <li v-if="!isLoggedIn" class="nav-item mx-2 hover-scale">
                    <router-link class="nav-link rounded" id="login" :to="{ name: 'Login Page' }">
                        Login
                    </router-link>
                </li>

                <li v-if="!isLoggedIn" class="nav-item mx-2 hover-scale">
                    <router-link class="nav-link rounded" id="signup" :to="{ name: 'Sign Up Page' }">
                        Sign Up
                    </router-link>
                </li>

                <li v-if="isLoggedIn" class="nav-item mx-2 hover-scale">
                    <button class="btn btn-danger nav-link rounded" id="logout" @click="logout">
                        Logout
                    </button>
                </li>
            </ul>
        </nav>
    </div>
</template>

<script>
import { useNavbarStore } from "../stores/useNavbarHeightStore.ts";
import { useCurrentUserStore } from "../stores/useCurrentUserStore.ts";

export default {
    name: "Navigation",
    computed: {
        isLoggedIn() {
            const currentUserStore = useCurrentUserStore();
            return currentUserStore.isLoggedIn;
        },
    },
    methods: {
        async initialiseUser() {
            const currentUserStore = useCurrentUserStore();
            await currentUserStore.requireAuthentication();
        },
        async logout() {
            const currentUserStore = useCurrentUserStore();
            await currentUserStore.logout();
        },
    },
    async mounted() {
        const navbar = this.$refs.navbar;
        if (navbar) {
            const navbarHeight = navbar.offsetHeight;
            const navbarStore = useNavbarStore();
            navbarStore.setHeight(navbarHeight);
        }

        await this.initialiseUser();
    },
};
</script>