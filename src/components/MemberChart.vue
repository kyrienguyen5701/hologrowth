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
  xTooltipDateFormatter
} from "@/assets/ts/common";
import { GetLocalizedText } from "@/assets/ts/localize";
import { XAxis } from "@/assets/ts/interfaces";

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
    xaxis: XAxis;
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
          text: `
          ${GetLocalizedText(this.memberData.name)}${GetLocalizedText(
            "'s"
          )}${GetLocalizedText("space")}${GetLocalizedText(
            availableRangesMap(this.chartData.range)
          )}${GetLocalizedText("'s")}${GetLocalizedText(
            "space"
          )}${GetLocalizedText(this.chartData.countType)}`,
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
            text: `${GetLocalizedText(this.chartData.countType)}`
          }
        },
        tooltip: {
          shared: false,
          x: {
            formatter: (val: string, obj: {series: Array<string>, seriesIndex: number, dataPointIndex: number}) => {
              return xTooltipDateFormatter(this.chartData.xaxis, val, obj);
            }
          },
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
