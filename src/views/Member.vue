<template>
  <div class="member-page">
    <div class="container">
      <div id="section-1" class="section">
        <div class="carousel">
          a
        </div>
        <div class="title">
          Member title
        </div>
      </div>
      <div class="section"></div>
      <div class="section"></div>
    </div>
  </div>
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
