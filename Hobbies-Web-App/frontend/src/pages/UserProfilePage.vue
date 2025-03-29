<template>
    <div class="container">
        <div class="row">
            <div class="col-sm-6 offset-sm-3">
                <div v-if="user" class="container">
                    <div class="row">
                        <div class="col-sm-12 text-center">
                            <h2 class="mb-4">{{ user.username }}'s Profile</h2>
                        </div>
                    </div>

                    <div class="row">
                        <div class="col-sm-6 px-1">
                            <div class="card text-center">
                                <h5 class="card-header">First Name</h5>
                                <div class="card-body">{{ user.first_name }}</div>
                            </div>
                        </div>

                        <div class="col-sm-6 px-1">
                            <div class="card text-center">
                                <h5 class="card-header">Last Name</h5>
                                <div class="card-body">{{ user.last_name }}</div>
                            </div>
                        </div>
                    </div>

                    <div class="row mt-2">
                        <div class="col-sm-6 px-1">
                            <div class="card text-center">
                                <h5 class="card-header">Email</h5>
                                <div class="card-body">{{ user.email }}</div>
                            </div>
                        </div>

                        <div class="col-sm-6 px-1">
                            <div class="card text-center">
                                <h5 class="card-header">Date of Birth</h5>
                                <div class="card-body">{{ user.date_of_birth }}</div>
                            </div>
                        </div>
                    </div>

                    <div class="row mt-2">
                        <div class="col-sm-12 px-1">
                            <div class="card text-center">
                                <h5 class="card-header">Hobbies</h5>
                                <div class="card-body">
                                    <span v-for="(hobby, index) in user.hobbies" :key="index" :class="[
                                        'badge',
                                        'rounded-pill',
                                        'ms-1',
                                        'my-1',
                                        'px-3',
                                        'py-2',
                                        index % 2 === 0
                                            ? 'text-bg-primary text-white shadow-primary'
                                            : 'text-bg-secondary text-white shadow-secondary',
                                    ]">
                                        {{ hobby.name }}
                                    </span>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="row mt-2">
                        <div class="col-sm-12 px-1">
                            <div class="card text-center">
                                <h5 class="card-header">Friends</h5>
                                <div class="card-body">
                                    <ul v-if="user.friends.length > 0" class="list-group">
                                        <li v-for="friend in user.friends" :key="friend.id" class="list-group-item">
                                            {{ friend.username }}
                                        </li>
                                    </ul>
                                    <p v-else>No friends ;-;</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div v-else>
                    <p>Loading user data...</p>
                </div>
            </div>
        </div>
    </div>



</template>

<script>
import { defineComponent, onMounted, computed } from "vue";
import { useRoute } from "vue-router";
import { useUsersStore } from "../stores/useUsersStore.ts";

export default defineComponent({
    name: "UserProfilePage",
    setup() {
        const route = useRoute();
        const userId = route.params.user_id;
        const usersStore = useUsersStore();

        const user = computed(() => usersStore.user);

        onMounted(() => {
            usersStore.fetchUser(userId);
        });

        return {
            user,
        };
    },
});
</script>