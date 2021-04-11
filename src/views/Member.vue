<template>
  <div class="member-page"></div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import Member from "@/components/Member.vue"; // @ is an alias to /src
import Stats from "@/components/Stats.vue";

@Component({
  components: {
    Member,
    Stats
  }
})
export default class Home extends Vue {}
</script>
