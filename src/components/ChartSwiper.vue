<template>
  <swiper class="swiper" :options="swiperOptionh">
    <swiper-slide v-for="countType in countTypes" :key="countType">
      <swiper class="swiper vertical" :options="swiperOptionv">
        <swiper-slide v-for="range in ranges" :key="range">
          <div v-if="loading">
            <div class="overlay-loading-container">
              <div class="overlay-loading">
                <div class="left"></div>
                <div class="right"></div>
              </div>
            </div>
          </div>
          <div v-else style="width: 100%">
            <MemberChart
              v-bind:memberData="{
                name: memberData.name,
                CSSname: memberData.CSSname
              }"
              v-bind:chartData="{
                countType: countType,
                range: range,
                seriesData: allSeries[`${countType}-${range}`],
                xaxis: xaxis
              }"
            ></MemberChart>
          </div>
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
import { Component, Prop, Watch, Vue } from "vue-property-decorator";
import { dateFormatter, countTypesMap } from "@/assets/ts/common";
import axios from "axios";
import { Swiper, SwiperSlide } from "vue-awesome-swiper";
import "swiper/swiper-bundle.css";

Vue.component("swiper", Swiper);
Vue.component("swiper-slide", SwiperSlide);

const ranges = [7, 30, 365, 0];
const countTypes = ["sub", "view"];

@Component
export default class ChartSwiper extends Vue {
  @Prop() memberData!: {
    name: string;
    CSSname: string;
  };

  @Watch("memberData", { immediate: true, deep: true })
  async initializeData() {
    this.$data.loading = true;
    for (let i = 0; i < countTypes.length; i++) {
      const countType = countTypes[i];
      for (let j = 0; j < ranges.length; j++) {
        const range = ranges[j];
        await axios({
          method: "POST",
          url: "http://127.0.0.1:8000/get-member-data",
          headers: { "content-type": "application/json" },
          data: {
            range: range,
            talent: this.memberData.name,
            countType: countType
          }
        })
          .then(res => {
            this.$data.allSeries[`${countType}-${range}`] = [
              {
                name: `${countTypesMap(countType)} Count`,
                data: Object.values(res.data)
              }
            ];
            this.$data.xaxis = {
              categories: Object.keys(res.data).map(dateFormatter),
              tickAmount:
                window.innerWidth <= 600
                  ? 7
                  : Math.min(15, Object.keys(res.data).length)
            };
          })
          .catch(e => console.log(e));
      }
    }
    this.$data.loading = false;
  }

  data() {
    return {
      loading: false,
      ranges: ranges,
      countTypes: countTypes,
      allSeries: {
        "sub-7": [],
        "sub-30": [],
        "sub-365": [],
        "sub-0": [],
        "view-7": [],
        "view-30": [],
        "view-365": [],
        "view-0": []
      },
      xaxis: [],
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
  height: 514px;
  width: 100%;

  .swiper-slide {
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: center;
    font-weight: bold;
    font-size: 14 * 2;
  }

  &.vertical {
    background-color: #fff;
  }
}
.overlay-loading-container {
  background: #fff;
}
</style>
