<template>
  <div style="width: 100%">
    <chart
      class="member-chart"
      height="500"
      :options="chartOptions"
      :series="series"
    >
    </chart>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";
import VueApexCharts from "vue-apexcharts";
import {
  GetCSSVar,
  countFormatter,
  availableRangesMap,
  countTypesMap
} from "@/assets/ts/common";

Vue.use(VueApexCharts);
Vue.component("chart", VueApexCharts);

@Component
export default class MemberChart extends Vue {
  @Prop() memberData!: {
    name: string;
    CSSname: string;
  };

  @Prop() chartData!: {
    countType: "sub" | "view";
    range: number;
    seriesData: Array<{ name: string; data: Array<number> }>;
    xaxis: Array<string>;
  };

  data() {
    return {
      series: this.chartData.seriesData,
      chartOptions: {
        chart: {
          width: "100%",
          height: 500,
          type: "line",
          zoom: {
            type: "x",
            enabled: true,
            autoScaleYaxis: true
          }
        },
        colors: [GetCSSVar(`--color-${this.memberData.CSSname}-complement`)],
        dataLabels: {
          enabled: false
        },
        stroke: {
          curve: "smooth"
        },
        title: {
          text: `${this.memberData.name}'s ${availableRangesMap(
            this.chartData.range
          )} ${countTypesMap(this.chartData.countType)} Counts`,
          align: "center"
        },
        grid: {
          row: {
            colors: [
              GetCSSVar(`--color-${this.memberData.CSSname}-tint-50`),
              "transparent"
            ],
            opacity: 0.5
          }
        },
        xaxis: this.chartData.xaxis,
        yaxis: {
          labels: {
            formatter: countFormatter
          },
          title: {
            text: `${countTypesMap(this.chartData.countType)} Count`
          }
        },
        tooltip: {
          shared: false,
          y: {
            formatter:
              this.chartData.countType === "sub"
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
.member-chart {
  background: #ffffff;
}
</style>
