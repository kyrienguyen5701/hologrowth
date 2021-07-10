<template>
  <swiper class="swiper" :options="swiperOptionh">
    <swiper-slide>Horizontal Slide 1</swiper-slide>
    <swiper-slide>
      <swiper class="swiper vertical" :options="swiperOptionv">
        <swiper-slide>Vertical Slide 1</swiper-slide>
        <swiper-slide>Vertical Slide 2</swiper-slide>
        <swiper-slide>Vertical Slide 3</swiper-slide>
        <swiper-slide>Vertical Slide 4</swiper-slide>
        <swiper-slide>Vertical Slide 5</swiper-slide>
        <div class="swiper-pagination swiper-pagination-v" slot="pagination"></div>
      </swiper>
    </swiper-slide>
    <swiper-slide>Horizontal Slide 1</swiper-slide>
    <swiper-slide>Horizontal Slide 2</swiper-slide>
    <swiper-slide>Horizontal Slide 3</swiper-slide>
    <swiper-slide>Horizontal Slide 4</swiper-slide>
    <div class="swiper-pagination swiper-pagination-h" slot="pagination"></div>
  </swiper>
</template>

<script lang="ts">
  import { Component, Vue } from "vue-property-decorator";
  import { Swiper, SwiperSlide } from "vue-awesome-swiper";
  import "swiper/swiper-bundle.css";

  Vue.component('swiper', Swiper);
  Vue.component('swiper-slide', SwiperSlide);

  @Component  
  export default class ChartSwiper extends Vue{
    data() {
      return {
        swiperOptionh: {
          spaceBetween: 50,
          pagination: {
            el: '.swiper-pagination-h',
            clickable: true
          }
        },
        swiperOptionv: {
          direction: 'vertical',
          spaceBetween: 50,
          pagination: {
            el: '.swiper-pagination-v',
            clickable: true
          }
        }
      }
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