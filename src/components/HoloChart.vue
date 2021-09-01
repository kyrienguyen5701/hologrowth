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
import { Component, Prop, Vue } from "vue-property-decorator";
import VueApexCharts from "vue-apexcharts";
import { countFormatter, xTooltipDateFormatter } from "@/assets/ts/common";
import { GetLocalizedText } from "@/assets/ts/localize";
import { XAxis } from "@/assets/ts/interfaces";

Vue.use(VueApexCharts);
Vue.component("chart", VueApexCharts);

@Component
export default class HoloChart extends Vue {
  @Prop() countType!: string;
  @Prop() sentSeries!: Array<object>;
  @Prop() sentColors!: Array<object>;
  @Prop() xaxis!: XAxis;

  data() {
    return {
      series: this.sentSeries,
      chartOptions: {
        chart: {
          id: `holochart-${this.countType}`,
          height: 500,
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
          curve: "smooth",
          width: 3
        },
        title: {
          text: GetLocalizedText(`${this.countType}-growth`),
          align: "center"
        },
        grid: {
          row: {
            colors: ["#ffffff", "transparent"],
            opacity: 0.5
          }
        },
        xaxis: this.xaxis,
        yaxis: {
          labels: {
            formatter: countFormatter
          },
          title: {
            text: GetLocalizedText(this.countType)
          }
        },
        tooltip: {
          shared: false,
          x: {
            formatter: (
              val: string,
              obj: {
                series: Array<string>;
                seriesIndex: number;
                dataPointIndex: number;
              }
            ) => {
              return xTooltipDateFormatter(this.xaxis, val, obj);
            }
          },
          y: {
            formatter:
              this.countType === "sub"
                ? countFormatter
                : (val: number) => {
                    return val;
                  }
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
