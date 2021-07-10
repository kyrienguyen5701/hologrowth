<template>
  <div class="member-page" :key="$data.memberName">
    <div id="section-1" class="section">
      <b-carousel :interval="4000" background="#ababab">
        <b-carousel-slide img-src=""></b-carousel-slide>
        <!-- v-for member image use for background here -->
      </b-carousel>
      <div class="section-title section-title-right">
        <div class="section-title-title">
          {{ getMemberName() }}
        </div>
        <div class="section-title-subtitle">
          Lorem ipsum, dolor sit amet consectetur adipisicing elit.
        </div>
      </div>
    </div>
    <div id="section-2" class="section section-text-left">
      <div class="section-image">
        <img src="" alt="" />
      </div>
      <div class="section-text">
        <div class="section-text-title">
          {{ getMemberName() }}
        </div>
        <div class="section-text-description">
          Lorem ipsum, dolor sit amet consectetur adipisicing elit. Laudantium
          fugit sed cumque sit quisquam aspernatur et. Vitae provident labore ex
          molestias, facilis voluptatum, beatae officiis placeat possimus quia,
          assumenda exercitationem!
        </div>
      </div>
    </div>
    <div id="section-3" class="section section-text-right">
      <div class="section-image">
        <img src="" alt="" />
      </div>
      <div class="section-text">
        <div class="section-text-title">
          {{ getMemberName() }}
        </div>
        <div class="section-text-description">
          <!-- <MemberChart
            v-bind:memberData="{
              name: getMemberName(),
              CSSname: getMemberCSSName()
            }"
          ></MemberChart> -->
          <ChartSwiper></ChartSwiper>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue, Watch } from "vue-property-decorator";
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

  @Watch("$route")
  onMemberChange() {
    this.$data.memberName = this.$route.params.talentName;
  }

  getMemberName() {
    return Common.GetTalentName(this.$data.memberName);
  }

  getMemberCSSName() {
    return this.$data.memberName.split("-")[1];
  }

  getMemberData() {
    return {
      name: this.getMemberName(),
      CSSname: this.getMemberCSSName()
    };
  }
}
</script>

<style lang="scss" scoped>
#section-1 {
  position: relative;
}
.section-title {
  position: absolute;
  bottom: 25%;
  font-size: 150%;

  &-right {
    text-align: right;
    right: 20%;
  }

  &-left {
    text-align: left;
    left: 20%;
  }

  &-title {
    font-size: 200%;
    color: var(--color-current);
    -webkit-text-fill-color: var(--color-current);
    -webkit-text-stroke-color: var(--color-text);
    -webkit-text-stroke-width: 1px;
  }

  &-subtitle {
    color: var(--color-text);
  }
}
.section-text {
  &-left {
    background: var(--color-current);
    clip-path: polygon(0 0, 33.33% 0, 58.33% 100%, 0% 100%);
  }

  &-right {
    background: var(--color-current);
    clip-path: polygon(66.66% 0, 100% 0, 100% 100%, 41.66% 100%);

    .section-text {
      margin-left: auto;
      text-align: right;
    }
  }

  width: 40%;
  padding: 0px 100px; // change to var(--lg) later
  height: 100%;
  text-align: left;

  &-title {
    font-size: 255%;
    text-transform: capitalize;
    color: var(--color-text);
    margin-top: 30%;
  }

  &-description {
    font-size: 125%;
    color: var(--color-text);
    margin-top: 20%;
  }
}
</style>
