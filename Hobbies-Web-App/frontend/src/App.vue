<template>
    <main class="container-fluid">
        <Navigation />
        <RouterView class="flex-shrink-0" />
    </main>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { RouterView } from "vue-router";
import Navigation from "./components/Navigation.vue";

export default defineComponent({
    components: { RouterView, Navigation },
});

</script>