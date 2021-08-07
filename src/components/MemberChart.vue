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
import { Component, Prop, Vue, Watch } from "vue-property-decorator";
import VueApexCharts from "vue-apexcharts";
import {
  GetCSSVar,
  countFormatter,
  dateFormatter,
  availableRangesMap,
  countTypesMap
} from "@/assets/ts/common";
import axios from "axios";

Vue.use(VueApexCharts);
Vue.component("chart", VueApexCharts);

@Component
export default class MemberChart extends Vue {
  @Prop() memberData!: {
    name: string;
    CSSname: string;
  };

  @Prop() chartData!: {
    range: number;
    countType: string;
  };

  @Watch("memberData", { immediate: true, deep: true })
  async initializeData() {
    await axios({
      method: "POST",
      url: "http://127.0.0.1:8000/get-member-data",
      headers: { "content-type": "application/json" },
      data: {
        range: this.chartData.range,
        talent: this.memberData.name,
        countType: this.chartData.countType
      }
    })
      .then(res => {
        this.$data.series = [
          {
            data: Object.values(res.data)
          }
        ];
        this.$data.chartOptions = {
          xaxis: {
            categories: Object.keys(res.data).map(dateFormatter)
          }
        };
      })
      .catch(e => console.log(e));
  }

  data() {
    return {
      series: [
        {
          name: `${countTypesMap(this.chartData.countType)} Count`,
          data: []
        }
      ],
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
        colors: [GetCSSVar(`--color-${this.memberData.CSSname}`)],
        dataLabels: {
          enabled: false
        },
        stroke: {
          curve: "smooth"
        },
        title: {
          text: `${this.memberData.name}'s ${availableRangesMap(this.chartData.range)} ${countTypesMap(this.chartData.countType)} Counts`,
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
        xaxis: {
          categories: []
        },
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
            formatter: countFormatter
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
