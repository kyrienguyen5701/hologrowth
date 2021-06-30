<template>
  <div>
    <chart 
      class="member-chart"
      height="350" 
      :options="chartOptions" 
      :series="series"
    >
    </chart>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";
import VueApexCharts from "vue-apexcharts";
import { GetCSSVar } from "@/assets/ts/common";

Vue.use(VueApexCharts);
Vue.component('chart', VueApexCharts);

const subcountFormatter = (val: number) => {
  const thousand = 1000;
  const million = 1000000;
  if (val < thousand) return val;
  if (val < million) return `${val / thousand}K`;
  return `${val / million}M`;
};

@Component
export default class MemberChart extends Vue {
  @Prop() memberData!: {
    name: string,
    CSSname: string
  }

  data() {
    return {
      series: [{
        name: "Subscriber count",
        data: [965000, 968000, 970000, 973000, 975000, 978000, 981000]
      }],
      chartOptions:{
        chart: {
          height: 350,
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
          text: `${this.memberData.name}'s last 7 days subscriber counts`,
          align: "center"
        },
        grid: {
          row: {
            colors: [GetCSSVar(`--color-${this.memberData.CSSname}-tint-50`), "transparent"],
            opacity: .5
          },
        },
        xaxis: {
          categories: ["Jun 14", "Jun 15", "Jun 16", "Jun 17", "Jun 18", "Jun 19", "Jun 20"]
        },
        yaxis: {
          labels: {
            formatter: subcountFormatter
          },
          title: {
            text: "Subscriber Count"
          }
        },
        tooltip: {
          shared: false,
          y: {
            formatter: subcountFormatter
          }
        }
      }
    }  
  }
}
</script>

<style lang="scss" scoped>
.member-chart {
  background: #ffffff;
}
</style>