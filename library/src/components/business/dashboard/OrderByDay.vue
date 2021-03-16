<template>
  <div>
    <div class="d-flex justify-content-between">
      <p class="chart-title" style="margin: 0px">Orders by Day</p>
      <chart-time-filter v-model="filter_time"></chart-time-filter>
    </div>
    <div v-loading="loading" style="padding: 10px;">
      <line-chart ref="chart" :chart-data="chartData" :options="options" style="height: 270px"></line-chart>
    </div>
  </div>
</template>

<script>
import LineChart from "@/components/charts/LineChart";
import axios from "axios";
import ChartTimeFilter from "@/components/business/dashboard/ChartTimeFilter";


export default {
  name: "OrderByDay",
  components: {
    ChartTimeFilter,
    LineChart
  },
  data() {
    return {
      chartData: null,
      options: {
        maintainAspectRatio:false,
        responsive: true,
        legend: {
          display: false
        },
        scales: {
          yAxes: [{
            gridLines: {
                drawOnChartArea: false
            },
            ticks: {
              beginAtZero: true,
              fontColor: "rgba(43, 48, 52, 0.4)",
              callback: function(value) {if (value % 1 === 0) {return value;}}
            },
          }],
          xAxes: [{
            gridLines: {
                drawOnChartArea: false
            },
            ticks: {
              fontColor: "rgba(43, 48, 52, 0.4)",
            }
          }]
        }
      },
      loading: false,
      filter_time: 'by_day'
    }
  },
  computed: {
    top_products() {
      return Array.from(new Set(this.labels));
    }
  },
  created() {
    this.get_data();
  },
  watch: {
    filter_time: {
      handler: function () {
        this.get_data();
      }
    }
  },
  methods: {
    get_data() {
      let that = this;
      that.loading = true;
      axios.get(`/api/analytics/order/?type=${this.filter_time}`).then(res => {
        let labels = [];

        let dataset = {
          label: 'Orders by Day',
          data: [],
        }
        res.data.forEach(item => {
          if (item.day_week) {
            labels.push(item.day_year + ' W' + item.day_week);
          } else if (item.day_month) {
            labels.push(item.day_year + '-' + item.day_month);
          } else {
            labels.push(item.day);
          }
          dataset.data.push(item.total);
        })
        that.loading = false;
        that.chartData = {
          labels: labels,
          datasets: [dataset]
        }
      });
    },
  }
}
</script>

<style scoped>
.top-products {
  list-style: none;
}
</style>
