<template>
  <div class="row mt-5">
    <div class="col-sm-12 mb-2">
      <h2 class="text-center">Find People with Similar Hobbies!</h2>
    </div>

    <div class="col-sm-2">
      <div class="container">
        <div class="row">
          <div class="col-sm-12">
            <h4 class="text-center">Filters</h4>
          </div>
        </div>
        <div class="row">
          <div class="col-sm-12 border py-2 rounded">
            <form @submit.prevent="applyFilters" class="text-center">
              <label for="minAge" class="form-label">Min Age</label>
              <input type="number" id="minAge" class="form-control mb-2 text-center" v-model.number="filters.minAge"/>
              <label for="maxAge" class="form-label">Max Age</label>
              <input type="number" id="maxAge" class="form-control mb-2 text-center" v-model.number="filters.maxAge"/>
              <button type="submit" id="Apply-Filters"
                      class="btn btn-primary text-white w-100 shadow-primary hover-scale">Apply
                Filters
              </button>
            </form>
          </div>
        </div>
      </div>

    </div>

    <div class="col-sm-7 px-0" id="hobbies">
      <div v-if="users.length > 0">
        <ul class="list-group" id="Similar-Users">
          <li v-for="user in filteredUsers" :key="user.id" class="list-group-item" :id="user.username">
            <div class="container-fluid">
              <div class="row">

                <div class="col-sm-9 d-flex flex-column">
                  <h5>{{ user.username }} ({{ user.age }} Years Old)</h5>
                  <p class="overflow-auto mt-2">
                    <strong>{{ user.similar_hobbies_count }}</strong> Common Hobbies:
                    <span v-for="(hobby, index) in user.common_hobbies" :key="index" :class="[
                      'badge',
                      'rounded-pill',
                      'ms-1',
                      'my-1',
                      'px-3',
                      'py-2',
                      index % 2 === 0
                        ? 'text-bg-primary text-white'
                        : 'text-bg-secondary text-white',
                    ]">
                      {{ hobby }}
                    </span>
                  </p>
                </div>
                <div class="col-sm-3 d-flex justify-content-center align-items-center">
                  <template
                      v-if="currentUser.received_requests.some(request => request.sender_id === user.id && request.status === 'pending')">
                    <button class="btn button-outline-secondary hover-scale shadow-secondary me-2"
                            @click="acceptFriendRequest(
              currentUser.received_requests.find(request => request.sender_id === user.id && request.status === 'pending').id
            )">
                      Accept
                    </button>
                    <button class="btn btn-outline-danger hover-scale shadow-danger me-2"
                            @click="declineFriendRequest(
              currentUser.received_requests.find(request => request.sender_id === user.id && request.status === 'pending').id
            )">
                      Decline
                    </button>
                  </template>
                  <template v-else>
                    <button class="btn button-outline-secondary hover-scale shadow-secondary me-2"
                            id="sendFriendRequest" @click="sendFriendRequest(user.id)">
                      Request
                    </button>
                  </template>
                  <router-link
                      class="btn btn-outline-primary hover-scale link-underline link-underline-opacity-0 shadow-primary"
                      :to="{ path: `/user-profile/${user.id}` }">
                    Profile
                  </router-link>
                </div>

              </div>
            </div>
          </li>
        </ul>

        <Pagination :currentPage="currentPage" :totalPages="totalPages" @change-page="changePage"/>
      </div>
      <div id="Error-Message" v-else class="alert alert-warning mt-4">
        No users found with the selected filters.
      </div>
    </div>


    <div class="col-sm-3">
      <div class="container px-0">
        <div class="row">
          <div class="col-sm-12">
            <h4 class="text-center">Sent Requests</h4>
            <ul class="list-group overflow-auto max-height-limit" id="Sent-Requests">
              <li v-for="request in requestsUsers" :key="request.id"
                  class="list-group-item d-flex justify-content-between align-items-center">
                <span :id="request.username">
                  {{ request.username }}
                </span>
                <span>
                  <span class="badge text-bg-primary text-white rounded-pill shadow-primary">Pending</span>
                  <router-link
                      class="badge text-bg-secondary text-white rounded-pill ms-2 hover-scale glow-link-secondary link-underline link-underline-opacity-0"
                      :to="{ path: `/user-profile/${request.id}` }">Profile</router-link>
                </span>
              </li>
            </ul>
            <div v-if="currentUser.sent_requests.length === 0" class="alert alert-info mt-3">
              No pending sent requests.
            </div>
          </div>
        </div>
        <div class="row mt-4">
          <div class="col-sm-12">
            <h4 class="text-center">Received Requests</h4>
            <ul class="list-group overflow-auto max-height-limit" id="Received-Requests">
              <li v-for="request in currentUser.received_requests.filter(req => req.status === 'pending')"
                  :key="request.id" class="list-group-item d-flex justify-content-between align-items-center">
                <span>
                  {{ request.sender_username }}
                </span>
                <span>
                  <button
                      class="badge text-bg-secondary text-white rounded-pill hover-scale glow-link-secondary link-underline link-underline-opacity-0 border-0"
                      id="acceptFriendRequest" @click="acceptFriendRequest(request.id)">Accept</button>
                  <button
                      class="badge text-bg-danger text-white rounded-pill ms-2 hover-scale shadow-danger link-underline link-underline-opacity-0 border-0"
                      id="declineFriendRequest" @click="declineFriendRequest(request.id)">Decline</button>
                </span>
              </li>
            </ul>
            <div v-if="currentUser.received_requests.filter(req => req.status === 'pending').length === 0"
                 class="alert alert-primary mb-0">
              No pending received requests.
            </div>
          </div>
        </div>
        <div class="row mt-4">
          <div class="col-sm-12">
            <h4 class="text-center">Friends List</h4>
            <ul class="list-group overflow-auto max-height-limit" id="Friends-List">
              <li v-for="friend in friendUsers" :key="friend.id"
                  class="list-group-item d-flex justify-content-between align-items-center" :id="friend.username">
                {{ friend.username }}
                <span>
                  <span class="badge text-bg-primary text-white rounded-pill shadow-primary">Common:
                    {{
                      friend.similar_hobbies_count
                    }}</span>
                  <router-link
                      class="badge text-bg-secondary text-white rounded-pill ms-2 hover-scale glow-link-secondary link-underline link-underline-opacity-0"
                      :to="{ path: `/user-profile/${friend.id}` }">Profile</router-link>
                </span>

              </li>
            </ul>
            <div v-if="currentUser.friends.length === 0">
              No friends...
            </div>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script>
import Pagination from "../components/Pagination.vue";
import {useUsersStore} from "../stores/useUsersStore.ts";
import {useCurrentUserStore} from "../stores/useCurrentUserStore.ts";

export default {
  name: "Hobbies Page",
  components: {
    Pagination,
  },
  data() {
    return {
      filters: {
        minAge: 0,
        maxAge: 100,
      },
      currentPage: 1,
      resultsPerPage: 10,
    };
  },
  computed: {
    usersStore() {
      return useUsersStore();
    },
    currentUserStore() {
      return useCurrentUserStore();
    },
    currentUser() {
      return this.currentUserStore.currentUser;
    },
    users() {
      return this.usersStore.users;
    },
    totalPages() {
      const friendIds = this.currentUserStore.currentUser.friends.map(friend => friend.id);
      const requestIds = this.currentUserStore.currentUser.sent_requests.map(request => request.receiver_id);
      let filteredUsers = this.users.filter(user => !friendIds.includes(user.id));
      filteredUsers = filteredUsers.filter(user => !requestIds.includes(user.id));
      const totalUsersWithData = filteredUsers.length;
      return Math.ceil(totalUsersWithData / this.resultsPerPage);
    },
    filteredUsers() {
      const friendIds = this.currentUserStore.currentUser.friends.map(friend => friend.id);
      const requestIds = this.currentUserStore.currentUser.sent_requests.map(request => request.receiver_id);
      let filteredUsers = this.users.filter(user => !friendIds.includes(user.id));
      filteredUsers = filteredUsers.filter(user => !requestIds.includes(user.id));
      const startIndex = (this.currentPage - 1) * this.resultsPerPage;
      const endIndex = startIndex + this.resultsPerPage;
      return filteredUsers.slice(startIndex, endIndex);
    },
    friendUsers() {
      const friendIds = this.currentUserStore.currentUser.friends.map(friend => friend.id);
      const friendUsers = this.users.filter(user => friendIds.includes(user.id));
      return friendUsers;
    },
    requestsUsers() {
      const pendingRequests = this.currentUserStore.currentUser.sent_requests.filter(req => req.status === 'pending');
      const requestIds = pendingRequests.map(request => request.receiver_id);
      const requestsUsers = this.users.filter(user => requestIds.includes(user.id));
      return requestsUsers;
    },
  },
  methods: {
    async fetchUsers() {
      await this.usersStore.fetchSimilarUsers(this.filters.minAge, this.filters.maxAge);
      if (this.currentPage > this.totalPages) {
        this.currentPage = this.totalPages || 1;
      }
    },
    applyFilters() {
      this.currentPage = 1;
      this.fetchUsers();
    },
    changePage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page;
      } else if (page < 1) {
        this.currentPage = 1;
      } else if (page > this.totalPages) {
        this.currentPage = this.totalPages;
      }
    },
    async sendFriendRequest(userId) {
      await this.usersStore.sendFriendRequest(userId);
      alert(`Friend request sent to user`);
      this.currentUserStore.fetchCurrentUser();
    },
    async acceptFriendRequest(requestId) {
      await this.usersStore.acceptFriendRequest(requestId);
      this.currentUserStore.fetchCurrentUser();
    },
    async declineFriendRequest(requestId) {
      await this.usersStore.declineFriendRequest(requestId);
      alert(`Friend request declined`);
      this.currentUserStore.fetchCurrentUser();
    },
  },
  mounted() {
    this.fetchUsers();
    this.currentUserStore.fetchCurrentUser();
  },
};
</script>
