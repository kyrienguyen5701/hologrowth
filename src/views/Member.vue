<template>
  <div class="member-page">
    <div class="container">
      <div id="section-1" class="section">
        <div class="carousel">
          a
        </div>
        <div class="title">
          {{ getMemberName() }}
        </div>
      </div>
      <div class="section"></div>
      <div class="section"></div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";
import Stats from "@/components/Stats.vue";
import * as Common from "@/assets/ts/common";

@Component({
  components: {
    Stats
  }
})
export default class MemberPage extends Vue {
  data() {
    return {
      memberName: this.$route.params.talentName
    };
  }

  getMemberName() {
    return Common.GetTalentName(this.$data.memberName);
  }
  // computed() {
  //   this.$data.memberName = this.$route.params.talentName;
  // }
}
</script>
