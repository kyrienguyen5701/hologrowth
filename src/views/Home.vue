<template>
  <div class="home">
    Home
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import Stats from "@/components/Stats.vue";

@Component({
  components: {
    Stats
  }
})
export default class Home extends Vue {}
</script>
