<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10 col-md-6 offset-sm-1 offset-md-3">
        <div class="container">
          <div class="row">
            <div class="col-sm-12 text-center">
              <h2 class="mb-4">Your Profile</h2>
            </div>
          </div>

          <form @submit.prevent="onSubmit" class="row">
            <div class="col-sm-12">
              <div class="container-fluid">
                <div class="row">
                  <div class="col-sm-6 px-1">
                    <div class="card text-center">
                      <label for="first_name" class="card-header form-label h4">First Name</label>
                      <input type="text" id="first_name" class="form-control border-0" v-model="form.first_name"
                        required />
                    </div>
                  </div>

                  <div class="col-sm-6 px-1">
                    <div class="card text-center">
                      <label for="last_name" class="card-header form-label h4">Last Name</label>
                      <input type="text" id="last_name" class="form-control border-0" v-model="form.last_name"
                        required />
                    </div>
                  </div>
                </div>

                <div class="row mt-2">
                  <div class="col-sm-6 px-1">
                    <div class="card text-center">
                      <label for="username" class="card-header form-label h4">Username</label>
                      <input type="text" id="username" class="form-control border-0" v-model="form.username" required />
                    </div>
                  </div>

                  <div class="col-sm-6 px-1">
                    <div class="card text-center">
                      <label for="email" class="card-header form-label h4">Email</label>
                      <input type="email" id="email" class="form-control border-0" v-model="form.email" required />
                    </div>
                  </div>
                </div>

                <div class="row mt-2">
                  <div class="col-sm-6 px-1 d-flex">
                    <div class="card text-center flex-grow-1">
                      <label for="dateOfBirth" class="card-header form-label h4">Date of
                        Birth</label>
                      <input type="date" id="dateOfBirth" class="form-control border-0" v-model="form.date_of_birth"
                        required />
                    </div>
                  </div>

                  <div class="col-sm-6 px-1 d-flex">
                    <div class="card text-center flex-grow-1">
                      <label for="newHobby" class="card-header form-label h4">Add Hobby</label>
                      <div class="d-flex align-items-center">
                        <div class="dropdown flex-grow-1">
                          <input type="text" id="newHobby" class="form-control border-0 dropdown-toggle"
                            data-bs-toggle="dropdown" v-model="newHobby" placeholder="Add a hobby" autocomplete="off"
                            @focus="showHobbies = true" @blur="hideHobbies" />
                          <ul class="dropdown-menu w-100 overflow-auto" style="max-height: 15rem;">
                            <li v-for="(hobby, index) in filteredHobbies" :key="index" class="dropdown-item"
                              @mousedown.prevent="selectHobby(hobby.name)">
                              {{ hobby.name }}
                            </li>
                          </ul>
                        </div>

                        <button type="button" id="addHobbyButton"
                          class="btn btn-outline-primary ms-2 flex-shrink-0 rounded-bottom-right on-hover-white-text"
                          @click="addHobby">
                          Add
                        </button>

                      </div>
                    </div>
                  </div>
                </div>

                <div class="row mt-2">
                  <div class="col-sm-12 px-1">
                    <div class="card text-center">
                      <label for="password" class="card-header form-label h4">Password</label>
                      <input type="password" id="password" class="form-control border-0"
                        placeholder="Enter new password" v-model="form.password" />
                    </div>
                  </div>
                </div>

                <div class="row mt-2">
                  <div class="col-sm-12 px-1">
                    <div class="card text-center">
                      <div class="card-header form-label h4">Your Hobbies</div>
                      <div class="card-body row">
                        <div class="col-12">
                          <div class="row row-cols-1 row-cols-sm-2 g-1 max-height-limit overflow-auto">
                            <div v-for="(hobby, index) in form.hobbies" :key="index"
                              class="col border-bottom px-3 py-2">
                              <div class="list-group-item d-flex justify-content-between align-items-center"
                                :id="hobby.name">
                                {{ hobby.name }}
                                <button type="button" id="removeHobbyButton"
                                  class="btn btn-outline-danger btn-sm hover-scale shadow-danger-sm"
                                  @click="removeHobby(hobby.id)">
                                  Remove
                                </button>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <div class="row mt-2">
                  <div class="col-sm-12 px-1">
                    <button type="submit"
                      class="btn btn-secondary border-0 hover-scale glow-link-secondary w-100 mb-2">Save
                      Changes
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useCurrentUserStore } from "../stores/useCurrentUserStore.ts";
import { useHobbiesStore } from "../stores/useHobbiesStore.ts";

export default {
  name: "Profile",
  data() {
    return {
      newHobby: "",
    };
  },
  computed: {
    currentUserStore() {
      return useCurrentUserStore();
    },
    hobbiesStore() {
      return useHobbiesStore();
    },
    form: {
      get() {
        return this.currentUserStore.currentUser;
      },
      set(value) {
        this.currentUserStore.updateCurrentUser(value);
      },
    },
    filteredHobbies() {
      console.log(this.form.hobbies)
      const userHobbyNames = this.form.hobbies.map(hobby => hobby.name.toLowerCase());
      return this.hobbiesStore.hobbies.filter(hobby =>
        hobby.name.toLowerCase().includes(this.newHobby.toLowerCase()) &&
        !userHobbyNames.includes(hobby.name.toLowerCase())
      );
    },

  },
  methods: {
    async addHobby() {
      if (this.newHobby.trim() !== "") {
        try {
          await this.currentUserStore.addHobby(this.newHobby.trim());
          this.newHobby = "";
        } catch (error) {
          console.error("Failed to add hobby:", error);
          alert("Error adding hobby.");
        }
      }
    },
    async removeHobby(hobbyId) {
      try {
        await this.currentUserStore.removeHobby(hobbyId);
      } catch (error) {
        console.error("Failed to remove hobby:", error);
        alert("Error removing hobby.");
      }
    },
    async onSubmit() {
      try {
        console.log("form when updating:", this.form)
        await this.currentUserStore.updateCurrentUser(this.form);
        alert("Your Profile Has Been Updated!!");
      } catch (error) {
        console.error("Error updating profile:", error);
        alert("Failed to update profile.");
      }
    },
    selectHobby(hobbyName) {
      this.newHobby = hobbyName;
    },
  },
  mounted() {
    this.currentUserStore.fetchCurrentUser();
    this.hobbiesStore.fetchHobbies();
  },
};
</script>
<style focused>
.rounded-bottom-right {
  border-radius: 0 0 0.25rem 0 !important;
}

.on-hover-white-text:hover {
  color: #ffffff !important;
}
</style>
