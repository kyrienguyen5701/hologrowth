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
                xaxis: xaxis[`${countType}-${range}`]
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
import {
  dateFormatter,
  longDateFormatter,
  tickAmount
} from "@/assets/ts/common";
import { XAxis } from "@/assets/ts/interfaces";
import axios from "axios";
import { Swiper, SwiperSlide } from "vue-awesome-swiper";
import "swiper/swiper-bundle.css";
import { GetLocalizedText } from "@/assets/ts/localize";

Vue.component("swiper", Swiper);
Vue.component("swiper-slide", SwiperSlide);

const ranges = [7, 30, 365];
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
          url: "https://hologrowth-server.kyrie5701.com/get-member-data",
          headers: { "content-type": "application/json" },
          data: {
            range: range,
            talent: this.memberData.name,
            countType: countType
          }
        })
          .then(res => {
            const size = Object.values(res.data).length;
            this.$data.allSeries[`${countType}-${range}`] = [
              {
                name: GetLocalizedText(countType),
                data: Object.values(res.data)
              }
            ];
            this.$data.xaxis[`${countType}-${range}`] = {
              categories: Object.keys(res.data),
              labels: {
                formatter: size >= 365 ? longDateFormatter : dateFormatter
              },
              tickAmount: tickAmount
            };
          })
          .catch(e => console.error(e));
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
        "view-7": [],
        "view-30": [],
        "view-365": []
      },
      xaxis: {
        "sub-7": {} as XAxis,
        "sub-30": {} as XAxis,
        "sub-365": {} as XAxis,
        "view-7": {} as XAxis,
        "view-30": {} as XAxis,
        "view-365": {} as XAxis
      },
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
