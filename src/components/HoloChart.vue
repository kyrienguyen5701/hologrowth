<template>
  <div v-if="draw">
    <chart
      class="holo-chart"
      height="500"
      :options="chartOptions"
      :series="series"
      type="line"
      ref="chart"
    >
    </chart>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue, Watch } from "vue-property-decorator";
import VueApexCharts from "vue-apexcharts";
import { countFormatter, countTypesMap } from "@/assets/ts/common";
import ApexCharts from "apexcharts";

Vue.use(VueApexCharts);
Vue.component("chart", VueApexCharts);

@Component
export default class HoloChart extends Vue {
  @Prop() countType!: string;
  @Prop() sentSeries!: Array<object>;
  @Prop() sentColors!: Array<object>;
  @Prop() xaxis!: object;
  @Prop({ default: false }) draw!: boolean;

  // @Watch("sentSeries", { immediate: true, deep: true }) // fetch data after navigation
  // async initializeData() {
  //   this.$data.series = this.sentSeries;
  //   this.$data.chartOptions = {
  //     ...this.$data.chartOptions, ...{
  //       colors: this.sentColors,
  //       xaxis: this.xaxis
  //     }
  //   }
  // }

  // @Watch("sentSeries", { immediate: true, deep: true })
  // updateSeries() {
  //   this.$data.series = this.sentSeries[0] == undefined ? [{ data: [0], name: "null" }] : this.sentSeries;
  //   console.log("Series: " + this.sentSeries);
  //   // ApexCharts.exec(`holochart-${this.$data.countType}`, "render");
  //   // if (this.sentSeries.length == 0) return;
  //   // if (this.sentSeries[0] == undefined) return;
  //   // this.$data.series = this.sentSeries;
  //   // (this.$refs["chart"] as Vue).$forceUpdate();
  // }

  @Watch("draw", { immediate: true })
  drawChart() {
    if (this.draw) {
      console.log("Drawing chart...");
    }
  }

  data() {
    console.log("Data: ", this.sentSeries)
    console.log("Colors: ", this.sentColors)
    return {
      series: this.sentSeries[0] == undefined ? [{ data: [0], name: "null" }] : this.sentSeries,
      chartOptions: {
        chart: {
          id: `holochart-${this.countType}`,
          height: 350,
          type: "line"
        },
        colors: this.sentColors[0] == undefined ? ['#ffffff'] : this.sentColors,
        dataLabels: {
          enabled: false
        },
        legend: {
          show: false
        },
        stroke: {
          curve: "smooth"
        },
        title: {
          text: `Hololive Number of ${countTypesMap(this.countType)}s Growth`,
          align: "center"
        },
        grid: {
          row: {
            colors: ["#ffffff"],
            opacity: 0.5
          }
        },

        xaxis: (this.xaxis as object[])[0] == undefined ? { categories: [] } : this.xaxis,
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
