import {createRouter, createWebHistory} from "vue-router";
import {useCurrentUserStore} from "../stores/useCurrentUserStore.ts";

// 1. Define route components.
import ProfilePage from "../pages/ProfilePage.vue";
import HobbiesPage from "../pages/HobbiesPage.vue";
import UserProfilePage from "../pages/UserProfilePage.vue";

let base = import.meta.env.VITE_API_BASE_URL;

// 2. Define the router
const router = createRouter({
    history: createWebHistory(base),
    routes: [
        {
            path: "/",
            name: "Hobbies Page",
            component: HobbiesPage,
            meta: {requiresAuth: true},
        },
        {
            path: "/profile/",
            name: "Profile Page",
            component: ProfilePage,
            meta: {requiresAuth: true},
        },
        {
            path: "/user-profile/:user_id",
            name: "User Profile Page",
            component: UserProfilePage,
            meta: {requiresAuth: true},
        },
        {
            path: "/login/",
            name: "Login Page",
            redirect: () => {
                window.location.href = `/accounts/login/`;
                return "";
            },
        },
        {
            path: "/sign-up/",
            name: "Sign Up Page",
            redirect: () => {
                window.location.href = `/accounts/signup/`;
                return "";
            },
        },
    ],
    linkActiveClass: "active-link",
});

router.beforeEach(async (to, _, next) => {
    const currentUserStore = useCurrentUserStore();

    await currentUserStore.fetchCurrentUser();

    if (to.meta.requiresAuth && !currentUserStore.isLoggedIn) {
        next({name: "Login Page"});
    } else {
        next();
    }
});

export default router;
