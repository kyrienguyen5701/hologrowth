<template>
  <div>
    <chart
      class="holo-chart"
      height="1000"
      :options="chartOptions"
      :series="series"
    >
    </chart>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue, Watch } from "vue-property-decorator";
import VueApexCharts from "vue-apexcharts";
import {
  GetCSSVar,
  countFormatter,
  dateFormatter,
  countTypesMap
} from "@/assets/ts/common";
import axios from "axios";

Vue.use(VueApexCharts);
Vue.component("chart", VueApexCharts);

@Component
export default class HoloChart extends Vue {
  @Prop() countType!: string;

  @Watch("$route", { immediate: true, deep: true }) // fetch data after navigation
  async initializeData() {
    await axios({
      method: "POST",
      url: "http://127.0.0.1:8000/get-holo-data",
      headers: { "content-type": "application/json" },
      data: {
        countType: this.countType
      }
    })
      .then(res => {
        Object.entries(res.data).forEach(([talent, countData]) => {
          this.$data.series.push({
            name: talent,
            data: Object.values(countData as object).reverse()
            // data: Object.entries(countData).map(f => { return [new Date(f[0]).getTime(), f[1]]})
          });
        });
        this.$data.chartOptions = {
          colors: Object.keys(res.data).map(talentName =>
            GetCSSVar(
              ("--color-" + talentName.split(" ").slice(-1)).toLowerCase()
            ).trim()
          ),
          xaxis: {
            categories: Object.keys(res.data["Tokino Sora"]).reverse().map(dateFormatter),
            tickAmount: 15
            // type: "datetime"
          }
        };
      })
      .catch(e => console.log(e));
  }

  data() {
    return {
      series: [],
      chartOptions: {
        chart: {
          height: 350,
          type: "line",
        },
        colors: [],
        dataLabels: {
          enabled: false
        },
        stroke: {
          curve: "smooth"
        },
        title: {
          text: ``,
          align: "center"
        },
        grid: {
          row: {
            colors: [
              "#ffffff"
            ],
            opacity: 0.5
          }
        },
        xaxis: {
          categories: []
          // type: 'datetime'
        },
        yaxis: {
          labels: {
            formatter: countFormatter
          },
          title: {
            text: `${countTypesMap(this.countType)} Count`
          }
        },
        tooltip: {
          shared: false,
          y: {
            formatter: countFormatter
          }
        }
      }
    };
  }
}
</script>

<style lang="scss" scoped>
.holo-chart {
  background: #ffffff;
}
</style>