<template>

  <div class="row main-container">
    <div class="col-sm-5 offset-sm-1 d-flex flex-column justify-content-center ">
      <div class="container background-gradient p-5 rounded shadow-lg hover-scale smooth-transition">
        <h1 class="display-5 fw-bold text-white">Welcome to the Hobbies App</h1>
        <p class="lead text-muted">
          Discover and connect with people who share your interests. Join a
          vibrant community of hobby enthusiasts today!
        </p>
      </div>
    </div>

    <div class="col-sm-4 offset-1 d-flex flex-column justify-content-center align-items-center">
      <router-link class="btn btn-primary shadow-primary hover-scale text-white btn-lg w-100 mb-3"
        :to="{ name: 'Login Page' }">
        Log In
      </router-link>
      <router-link class="btn btn-outline-secondary shadow-secondary hover-scale btn-lg w-100"
        :to="{ name: 'Sign Up Page' }">
        Sign Up
      </router-link>
    </div>
  </div>

</template>

<script>
import { useNavbarStore } from "../stores/useNavbarHeightStore.ts";

export default {
  name: "HomePage",
  mounted() {
    const navbarStore = useNavbarStore();

    document.documentElement.style.setProperty(
      "--navbar-height",
      `${navbarStore.height}px`
    );
  },
};
</script>

<style scoped>
h1 {
  color: #343a40;
}

.btn:hover {
  color: white;
}

.background-gradient {
  background: linear-gradient(-45deg, #007bff, #28a745, #007bff, #23d5ab);
  background-size: 400% 400%;
  animation: gradient 5s ease infinite;
}

@keyframes gradient {
  0% {
    background-position: 0% 50%;
  }

  50% {
    background-position: 100% 50%;
  }

  100% {
    background-position: 0% 50%;
  }
}
</style>
