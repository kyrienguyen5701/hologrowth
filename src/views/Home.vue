<template>
  <div class="home">
    <div class="sidebar">
      <div class="searchbar">
        <input
          type="text"
          v-on:keyup="search($event.target.value)"
          :placeholder="searchPlaceholder"
        />
      </div>
      <div class="members">
        <div
          class="member"
          v-for="mem in members"
          :key="mem.name"
          v-show="mem.shown"
          v-on:click="toggleTalentSeries"
        >
          <div :id="mem.name + '-banner'" class="member-banner" :rel="mem.rel">
            <div :id="mem.name + ' overlay'" class="overlay"></div>
            <img :src="mem.banner" width="320" :alt="mem.name" />
          </div>
          <div :id="mem.name + '-avatar'" class="member-avatar" :rel="mem.rel">
            <img :src="mem.avatar" :alt="mem.name" />
          </div>
        </div>
      </div>
    </div>
    <div
      class="chart-placeholder flex-centered"
      ref="chart-holder"
      style="border-left: 10px solid;border-image-slice: 1;border-image-source: linear-gradient(45deg,var(--color-Sora),var(--color-Sora))"
    >
      <div class="chart-background">
        <div class="overlay"></div>
        <div class="chart-background-col" v-for="i in background.nCol" :key="i">
          <div class="img-holder" v-for="j in background.nRow" :key="j">
            <img :src="getMemberIconURL(background.data[i][j])" />
          </div>
        </div>
      </div>
      <div
        class="chart-swiper"
        ref="swiper"
        style="border-image-slice: 1;border-image-source: linear-gradient(var(--angle),var(--color-Sora),var(--color-Sora))"
      >
        <div class="overlay-loading-container" v-if="loading">
          <div class="overlay-loading">
            <div class="left"></div>
            <div class="right"></div>
          </div>
        </div>
        <swiper class="swiper" :options="swiperOptionh">
          <swiper-slide v-for="countType in countTypes" :key="countType">
            <div class="chart" :ref="`holochart-${countType}`">
              <div v-if="loading">
                <div class="overlay-loading-container">
                  <div class="overlay-loading">
                    <div class="left"></div>
                    <div class="right"></div>
                  </div>
                </div>
              </div>
              <div v-else>
                <HoloChart
                  v-bind:countType="countType"
                  v-bind:sentSeries="[sentSeries[countType][0]]"
                  v-bind:sentColors="[sentColors[0]]"
                  v-bind:xaxis="fullXAxis[countType]"
                ></HoloChart>
              </div>
            </div>
          </swiper-slide>
          <div
            class="swiper-pagination swiper-pagination-h"
            slot="pagination"
          ></div>
        </swiper>
      </div>
    </div>
    <div class="section-2">
      <div class="section-inner">
        <div class="title-section">
          <div class="title-section-title">
            {{ aboutSection.aboutText }}
          </div>
        </div>
        <div
          class="text-section"
          v-for="text in aboutSection.data"
          v-bind:key="text.title"
        >
          <div class="text-section-title">{{ text.title }}</div>
          <div class="text-section-description">{{ text.description }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Watch } from "vue-property-decorator";
import Member from "@/components/MemberHome.vue";
import Stats from "@/components/Stats.vue";
import {
  GetCSSVar,
  dateFormatter,
  longDateFormatter,
  GetTalentCSSName,
  tickAmount
} from "@/assets/ts/common";
import { TalentDisplay } from "@/assets/ts/interfaces";
import talents from "@/assets/json/talents.json";
import ApexCharts from "apexcharts";
import axios from "axios";
import { GetLocalizedText } from "@/assets/ts/localize";
import { Swiper, SwiperSlide } from "vue-awesome-swiper";
import "swiper/swiper-bundle.css";

const about = ["what", "how", "why", "disclaimer", "who", "license"];
const goddess = "Tokino Sora";

Vue.component("swiper", Swiper);
Vue.component("swiper-slide", SwiperSlide);

@Component({
  components: {
    Member,
    Stats
  }
})
export default class Home extends Vue {
  data() {
    return {
      loading: false,
      countTypes: ["sub", "view"],
      searchPlaceholder: GetLocalizedText("search-placeholder"),
      members: (() => {
        const res = Array<TalentDisplay>();
        talents.forEach(talent => {
          res.push({
            rel: talent.id,
            name: talent.name,
            avatar: require(`@/assets/talentAvatars/medium/${talent.name}.png`),
            banner: require(`@/assets/talentBanners/medium/${talent.name}_320 x 52.png`),
            dataAvailable: talent.name === goddess ? true : false,
            shown: true
          });
        });
        return res;
      })(),
      fullSeries: {
        sub: [],
        view: []
      },
      fullColors: [],
      fullXAxis: {
        sub: {
          categories: [],
          tickAmount: 15
        },
        view: {
          categories: [],
          tickAmount: 15
        }
      },
      sentSeries: {
        sub: [],
        view: []
      },
      sentColors: [],
      shown: 1,
      background: {
        nCol: 0, //Math.round(window.innerWidth / 250),
        nRow: 0, //Math.round(window.innerHeight / 250),
        data: [["Sora"]]
      },
      aboutSection: {
        aboutText: GetLocalizedText("about"),
        data: (() => {
          const res = [] as Array<{ title: string; description: string }>;
          about.forEach(part => {
            res.push({
              title: GetLocalizedText(part),
              description: GetLocalizedText(`${part}-content`)
            });
          });
          return res;
        })()
      },
      swiperOptionh: {
        spaceBetween: 50,
        pagination: {
          el: ".swiper-pagination-h",
          clickable: true
        }
      }
    };
  }

  @Watch("$route", { immediate: true, deep: true }) // fetch data after navigation
  async initializeData() {
    this.$data.loading = true;
    for (let i = 0; i < 2; i++) {
      const countType = this.$data.countTypes[i];
      await axios({
        method: "POST",
        url: "https://tools.kekstudio.com/get-member-data",
        headers: { "content-type": "application/json" },
        data: {
          range: 0,
          talent: goddess,
          countType: countType
        }
      })
        .then(res => {
          const size = Object.keys(res.data).length;
          this.$data.sentSeries[countType].push({
            name: GetLocalizedText(goddess),
            data: Object.values(res.data)
          });
          if (countType === "sub") {
            this.$data.sentColors.push(
              GetCSSVar("--color-" + GetTalentCSSName(goddess))
            );
          }
          this.$data.fullXAxis[countType] = {
            categories: Object.keys(res.data),
            labels: {
              formatter: size >= 365 ? longDateFormatter : dateFormatter
            },
            tickAmount: tickAmount
          };
        })
        .catch(e => console.error(e));
    }
    this.$data.loading = false;
    const soraDiv = document.getElementById(`${goddess}-banner`)
      ?.parentElement as HTMLElement;
    soraDiv?.setAttribute("clicked", "");
  }

  async getData(talent: string) {
    this.$data.loading = true;
    for (let i = 0; i < 2; i++) {
      const countType = this.$data.countTypes[i];

      await axios({
        method: "POST",
        url: "https://tools.kekstudio.com/get-member-data",
        headers: { "content-type": "application/json" },
        data: {
          range: 0,
          talent: talent,
          countType: countType
        }
      })
        .then(res => {
          this.$data.sentSeries[countType].push({
            name: GetLocalizedText(talent),
            data: Object.values(res.data)
          });
          if (countType === "sub") {
            this.$data.sentColors.push(
              GetCSSVar("--color-" + GetTalentCSSName(talent))
            );
          }
        })
        .catch(e => console.error(e));
    }
    this.$data.loading = false;
  }

  async toggleTalentSeries(event: Event) {
    let target = event.target as HTMLElement | null | undefined;
    let talentName = "";
    let talentRel = 0;
    let isShown = false;
    while (
      (target = target?.parentElement) &&
      !target.classList.contains("member")
    ) {
      talentName = target?.id.split("-")[0];
      if (target?.hasAttribute("rel")) {
        talentRel = parseInt(target?.getAttribute("rel") as string);
      }
      continue;
    }
    if (target?.hasAttribute("clicked")) {
      if (this.$data.shown === 1) {
        return;
      }
      --this.$data.shown;
      target?.removeAttribute("clicked");
      isShown = false;
    } else {
      this.$data.shown++;
      target?.setAttribute("clicked", "");
      isShown = true;
    }
    this.toggleChartBorder(talentName, isShown);
    if (!this.$data.members[talentRel].dataAvailable) {
      await this.getData(talentName).then(() => {
        this.$data.countTypes.forEach((countType: "sub" | "view") => {
          ApexCharts.exec(`holochart-${countType}`, "updateOptions", {
            series: this.$data.sentSeries[countType],
            colors: this.$data.sentColors
          });
          this.$data.members[talentRel].dataAvailable = true;
        });
      });
    } else {
      this.$data.countTypes.forEach((countType: "sub" | "view") => {
        ApexCharts.exec(`holochart-${countType}`, "toggleSeries", talentName);
      });
    }
  }

  toggleChartBorder(talentName: string, isShown: boolean) {
    const cssVar = `var(--color-${GetTalentCSSName(talentName)})`;
    const currentGrad = (this.$refs["swiper"] as HTMLElement).style
      .borderImageSource;
    const matches = currentGrad.match(/var\(--color-.*?\)/gm) || [];
    if (matches.length == 2 && matches[0] == matches[1]) {
      matches.pop();
    }
    if (isShown) {
      matches.push(cssVar);
    } else {
      const i = matches.indexOf(cssVar);
      matches.splice(i, 1);
    }
    if (matches.length == 1) matches.push(matches[0]);
    (this.$refs[
      "swiper"
    ] as HTMLElement).style.borderImageSource = `linear-gradient(var(--angle),${matches.join(
      ","
    )}`;
  }

  search(input: string) {
    const queries = input.split(" ");
    const dp = Array<Array<boolean>>();
    for (let i = 0; i < queries.length; i++) {
      const query = queries[i];
      let countThisQuery = 0;
      const shownThisQuery = Array<boolean>(this.$data.members.length);
      this.$data.members = this.$data.members.map((member: TalentDisplay) => {
        const talent = talents[member.rel];
        const { branch, genNumber, genName, name, tags } = talent;
        const meta = `${branch} ${genNumber} ${genName} ${name} ${tags.join(
          " "
        )}`.toLowerCase();
        const shown = meta.includes(query);
        shownThisQuery[member.rel] = shown;
        shown && countThisQuery++;
        return {
          ...member,
          ...{
            shown: i === 0 ? shown : shown && dp[i - 1][member.rel]
          }
        };
      });
      if (!countThisQuery) break;
      dp.push(shownThisQuery);
    }
  }

  getMemberIconURL(memberName: string) {
    return require(`@/assets/talentIcons/default/${memberName}.svg`);
  }
}
</script>

<style lang="scss" scoped>
$bg_sidebar: #ccc;
.home {
  display: flex;
  height: calc(100vh - 80px);
  .sidebar {
    max-width: 320px;
    .searchbar {
      background: $bg_sidebar;
      input {
        width: 100%;
        text-align: center;
        height: 60px;
      }
    }
    .members {
      height: calc(100% - 60px);
      overflow-y: scroll;
      &::-webkit-scrollbar {
        display: none;
      }
      scrollbar-width: none;
      .member {
        position: relative;
        height: 105px;
        &[clicked] {
          .overlay {
            display: none;
          }
          .member-avatar {
            opacity: 1;
          }
        }
        &:hover {
          cursor: pointer;
          background: mix(black, $bg_sidebar, 25);
          &-avatar {
            background: black;
          }
          .member-banner {
            .overlay {
              opacity: 0;
            }
          }
          .member-avatar {
            opacity: 1;
          }
        }
        &-banner {
          position: relative;
          .overlay {
            position: absolute;
            width: 100%;
            height: 100%;
            background: white;
            opacity: 0.6;
            transition: all 0.75s ease;
          }

          img {
            height: 105px;
          }
        }
        &-avatar {
          background: white;
          position: absolute;
          right: 0;
          bottom: 0;
          border-radius: 50%;
          border: 1px solid var(--color-current);
          padding: 4px;
          opacity: 0;
          transition: all 0.5s ease;
          img {
            border: 1px solid var(--color-current);
            height: 40px;
            width: 40px;
            border-radius: 50%;
          }
        }
        &-banner {
          display: flex;
          height: 100%;
          img {
            height: 100%;
          }
        }
      }
    }
  }
}
.chart-placeholder {
  width: calc(100% - 320px);
  position: relative;

  .chart-background {
    position: absolute;
    top: 0;
    width: 100%;
    height: 100%;
    z-index: -1;

    .overlay {
      height: 100%;
      // background: #00000030;
    }

    &-col {
      cursor: pointer;
    }
  }

  .chart-swiper {
    --angle: 0deg;
    background: white;
    width: calc(100% * 11 / 12);
    padding: 2%;
    border: 10px solid;
    animation: rotate-border 8s linear infinite;
    position: relative;
    min-height: calc(565px + 2%);
  }
}

@keyframes rotate-border {
  to {
    --angle: 360deg;
  }
}

@property --angle {
  syntax: "<angle>";
  initial-value: 0deg;
  inherits: false;
}

.section-2 {
  position: absolute;
  top: 100vh;
  border-top: 10px solid var(--color-current);
  width: 100%;
  background: var(--color-current-tint-50);

  .section-inner {
    width: calc(100% - 320px * 2);
    margin: auto;
    border-left: 10px solid var(--color-current);
    border-right: 10px solid var(--color-current);
    background: #fff;
    padding: 40px 30px;
  }

  .title-section {
    &-title {
      color: var(--color-current);
      font-size: 2.5rem;
    }
    margin-bottom: 30px;
  }

  .text-section {
    text-align: left;
    &-title {
      position: relative;
      width: 50%;
      margin-left: -30px;
      padding: 10px 0px 10px 30px;
      background: var(--color-current);
      color: var(--color-text);

      &:before {
        content: "";
        position: absolute;
        bottom: 0;
        right: 0;
        // border-right: 52px solid white;
        // border-bottom: 52px solid transparent;
        border-top-right-radius: 100px;
        background: var(--color-current);
      }

      &:after {
        content: "";
        position: absolute;
        bottom: 0;
        left: 0;
        width: calc(200% + 60px);
        height: 3px;
        background: var(--color-current);
      }
    }

    &-description {
      margin-bottom: 15px;
    }
  }
}
</style>

<style lang="scss" scoped>
@media (max-width: 600px) {
  .home {
    height: initial;
    flex-direction: column;

    .sidebar {
      width: 100%;
      max-width: initial;

      .searchbar {
        input {
          height: 40px;
        }
      }

      .members {
        height: 30vh;

        .member {
          &-banner {
            img {
              width: 100%;
              height: initial;
            }
          }
        }
      }
    }
  }
  .chart-placeholder {
    width: 100%;
    border-left: none !important;
    border-top: 10px solid;

    .chart-swiper {
      height: 100%;
      padding: 0;
      border: none;
    }
  }
  .section-2 {
    top: calc(100vh + 70px);

    .section-inner {
      width: 100%;
      margin: auto;
      border: none;
      background: #fff;
      padding: 20px 0;
    }

    .title-section {
      &-title {
        font-size: 2rem;
      }
    }

    .text-section {
      text-align: left;
      &-title {
        width: 100%;
        margin-left: 0px;

        &:after {
          display: none;
        }
      }

      &-description {
        padding: 15px;
        margin-bottom: 15px;
      }
    }
  }
}
</style>
<style lang="scss" scoped>
@media (min-width: 601px) and (max-width: 768px) {
  .home {
    .sidebar {
      width: 250px;

      .members {
        .member {
          height: 80px;

          &-banner {
            img {
              width: 250px;
            }
          }
        }
      }
    }
  }
  .chart-placeholder {
    width: calc(100% - 250px);
    border-left: 5px solid !important;

    .chart-swiper {
      border-width: 5px;
    }
  }
  .section-2 {
    border-width: 5px;
    top: calc(100vh - 20px);

    .section-inner {
      border: none;
      width: 100%;
    }
  }
}
</style>
