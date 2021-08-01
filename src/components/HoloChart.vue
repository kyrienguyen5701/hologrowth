<template>
  <div>
    <chart
      class="holo-chart"
      height="500"
      :options="chartOptions"
      :series="series"
      type="line"
    >
    </chart>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue, Watch } from "vue-property-decorator";
import VueApexCharts from "vue-apexcharts";
import { countFormatter, countTypesMap } from "@/assets/ts/common";

Vue.use(VueApexCharts);
Vue.component("chart", VueApexCharts);

@Component
export default class HoloChart extends Vue {
  @Prop() countType!: string;
  @Prop() sentSeries!: Array<object>;
  @Prop() sentColors!: Array<object>;
  @Prop() xaxis!: object;

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

  data() {
    return {
      series: this.sentSeries,
      chartOptions: {
        chart: {
          id: `holochart-${this.countType}`,
          height: 350,
          type: "line"
        },
        colors: this.sentColors,
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
            colors: [
              "#ffffff"
            ],
            opacity: 0.5
          }
        },
        xaxis: this.xaxis,
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
