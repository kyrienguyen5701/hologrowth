<template>
  <div class="home">
    <div class="sidebar">
      <div class="searchbar">
        <input type="text" v-on:keyup="search($event.target.value)" />
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
            <img :src="mem.banner" width="320" height="105" :alt="mem.name" />
          </div>
          <div :id="mem.name + '-avatar'" class="member-avatar" :rel="mem.rel">
            <img :src="mem.avatar" :alt="mem.name" />
          </div>
        </div>
      </div>
    </div>
    <div class="chart flex-centered">
      <div class="col-11">
        <div v-show="loading">
          <div class="overlay-loading-container">
            <div class="overlay-loading">
              <div class="left"></div>
              <div class="right"></div>
            </div>
          </div>
        </div>
        <div>
          <HoloChart
            v-bind:countType="countType"
            v-bind:sentSeries="[fullSeries[0]]"
            v-bind:sentColors="[fullColors[0]]"
            v-bind:xaxis="fullXAxis"
          ></HoloChart>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Watch } from "vue-property-decorator";
import Member from "@/components/MemberHome.vue";
import Stats from "@/components/Stats.vue";
import { GetCSSVar, dateFormatter, GetTalentCSSName } from "@/assets/ts/common";
import { TalentDisplay } from "@/assets/ts/interfaces";
import talents from "@/assets/json/talents.json";
import ApexCharts from "apexcharts";
import axios from "axios";

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
      countType: "sub",
      members: (() => {
        const res = Array<TalentDisplay>();
        talents.forEach(talent => {
          res.push({
            rel: talent.id,
            name: talent.name,
            avatar: require(`@/assets/talentAvatars/medium/${talent.name}.png`),
            banner: require(`@/assets/talentBanners/medium/${talent.name}_320 x 52.png`),
            dataAvailable: talent.name === "Tokino Sora" ? true : false,
            shown: true
          });
        });
        return res;
      })(),
      fullSeries: [],
      fullColors: [],
      fullXAxis: [],
      sentSeries: [],
      sentColors: [],
      shown: 1
    };
  }

  @Watch("$route", { immediate: true, deep: true }) // fetch data after navigation
  async initializeData() {
    this.$data.loading = true;
    await axios({
      method: "POST",
      url: "http://127.0.0.1:8000/get-holo-data",
      headers: { "content-type": "application/json" },
      data: {
        countType: this.$data.countType
      }
    })
      .then(res => {
        Object.entries(res.data).forEach(([talent, countData]) => {
          this.$data.fullSeries.push({
            name: talent,
            data: Object.values(countData as object).reverse()
          });
        });
        this.$data.fullColors = Object.keys(res.data).map(talentName => {
          return GetCSSVar("--color-" + GetTalentCSSName(talentName));
        });
        this.$data.fullXAxis = {
          categories: Object.keys(res.data["Tokino Sora"])
            .reverse()
            .map(dateFormatter),
          tickAmount: 15
          // type: "datetime"
        };
        this.$data.sentSeries.push(this.$data.fullSeries[0]);
        this.$data.sentColors.push(this.$data.fullColors[0]);
      })
      .catch(e => console.log(e));
    this.$data.loading = false;
    const soraDiv = document.getElementById("Tokino Sora-banner")
      ?.parentElement as HTMLElement;
    soraDiv?.setAttribute("clicked", "");
  }
  toggleTalentSeries(event: Event) {
    let target = event.target as HTMLElement | null | undefined;
    let talentName = "";
    let talentRel = 0;
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
    } else {
      this.$data.shown++;
      target?.setAttribute("clicked", "");
    }
    if (!this.$data.members[talentRel].dataAvailable) {
      const series = this.$data.fullSeries[talentRel];
      const color = this.$data.fullColors[talentRel];
      this.$data.sentSeries.push(series);
      this.$data.sentColors.push(color);
      ApexCharts.exec(`holochart-${this.$data.countType}`, "updateOptions", {
        series: this.$data.sentSeries,
        colors: this.$data.sentColors
      });
      this.$data.members[talentRel].dataAvailable = true;
      if (this.$data.members[talentRel].dataAvailable) {
        ApexCharts.exec(
          `holochart-${this.$data.countType}`,
          "toggleSeries",
          talentName
        );
      }
    }
    if (this.$data.members[talentRel].dataAvailable) {
      ApexCharts.exec(
        `holochart-${this.$data.countType}`,
        "toggleSeries",
        talentName
      );
    }
  }
  search(input: string) {
    const queries = input.split(" ");
    const dp = Array<Array<boolean>>();
    for (let i = 0; i < queries.length; i++) {
      const query = queries[i];
      console.log(query);
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
      padding: 10px;
      background: $bg_sidebar;
      input {
        width: 100%;
        text-align: center;
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
  .chart {
    width: calc(100% - 100px);
  }
}
</style>
