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
import { Component, Prop, Vue, Watch } from "vue-property-decorator";
import VueApexCharts from "vue-apexcharts";
import { GetCSSVar } from "@/assets/ts/common";
import axios from "axios";
import { format } from "date-fns";

Vue.use(VueApexCharts);
Vue.component("chart", VueApexCharts);

const subcountFormatter = (val: number) => {
  const thousand = 1000;
  const million = 1000000;
  if (val < thousand) return val;
  if (val < million) return `${val / thousand}K`;
  return `${val / million}M`;
};

const dateFormatter = (val: string) => {
  return format(new Date(val), "MMM dd");
};

@Component
export default class MemberChart extends Vue {
  @Prop() memberData!: {
    name: string;
    CSSname: string;
  };

  @Watch("memberData", { immediate: true, deep: true })
  async initializeData() {
    console.log(document.getElementById("chart"));
    await axios({
      method: "POST",
      url: "http://127.0.0.1:8000/send",
      headers: { "content-type": "application/json" },
      data: {
        days: 7,
        talent: this.memberData.name,
        countType: "sub"
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
          name: "Subscriber count",
          data: []
        }
      ],
      chartOptions: {
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
    };
  }
}
</script>

<style lang="scss" scoped>
.member-chart {
  background: #ffffff;
}
</style>
