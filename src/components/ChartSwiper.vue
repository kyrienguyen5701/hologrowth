<template>
  <swiper class="swiper" :options="swiperOptionh">
    <swiper-slide v-for="countType in countTypes" :key="countType">
      <swiper class="swiper vertical" :options="swiperOptionv">
        <swiper-slide v-for="range in ranges" :key="range">
          <MemberChart
            v-bind:memberData="{
              name: memberData.name,
              CSSname: memberData.CSSname
            }"
            v-bind:chartData="{
              range: range,
              countType: countType
            }"
          ></MemberChart>
        </swiper-slide>
        <div
          class="swiper-pagination swiper-pagination-v"
          slot="pagination"
        ></div>
      </swiper>
    </swiper-slide>
    <div class="swiper-pagination swiper-pagination-h" slot="pagination"></div>
  </swiper>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";
import { Swiper, SwiperSlide } from "vue-awesome-swiper";
import "swiper/swiper-bundle.css";

Vue.component("swiper", Swiper);
Vue.component("swiper-slide", SwiperSlide);

@Component
export default class ChartSwiper extends Vue {
  @Prop() memberData!: {
    name: string;
    CSSname: string;
  };

  data() {
    return {
      ranges: [7, 30, 365, 0],
      countTypes: ["sub", "view"],
      swiperOptionh: {
        spaceBetween: 50,
        pagination: {
          el: ".swiper-pagination-h",
          clickable: true
        }
      },
      swiperOptionv: {
        direction: "vertical",
        spaceBetween: 50,
        pagination: {
          el: ".swiper-pagination-v",
          clickable: true
        }
      }
    };
  }
}
</script>

<style lang="scss" scoped>
.swiper {
  height: 300px;
  width: 100%;

  .swiper-slide {
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: center;
    font-weight: bold;
    font-size: 14 * 2;
    background-color: #000000;
  }
}

.swiper.vertical {
  background-color: beige;
}
</style>
