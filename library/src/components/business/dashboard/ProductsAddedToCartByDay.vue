<template>
  <div>
    <div class="d-flex justify-content-between">
      <p class="bolder font-14" style="margin: 0px 0 0 15px">Products Added To Cart</p>
      <chart-time-filter v-model="filter_time"></chart-time-filter>
    </div>
    <div v-loading="loading" style="padding: 10px;">
      <line-chart :chart-data="chartData" :options="options" style="height: 270px"></line-chart>
    </div>
  </div>
</template>

<script>
import LineChart from "@/components/charts/LineChart";
import axios from "axios";
import ChartTimeFilter from "@/components/business/dashboard/ChartTimeFilter";


export default {
  name: "ProductsAddedToCartByDay",
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
            ticks: {
              beginAtZero: true,
              callback: function(value) {if (value % 1 === 0) {return value;}}
            }
          }]
        }
      },
      loading: false,
      filter_time: "by_day"
    }
  },
  created() {
    this.get_data();
  },
  watch: {
    filter_time: {
      handler: function () {
        this.get_data()
      }
    }
  },
  methods: {
    get_data() {
      let that = this;
      that.loading = true
      axios.get(`/api/analytics/product-added-to-cart/?type=${this.filter_time}`).then(res => {
        let labels = []
        let dataset = {
          label: 'Products Added To Cart',
          data: []
        }
        res.data.forEach(item => {
          if (item.day_week) {
            labels.push(item.day_year + ' W' + item.day_week);
          } else if (item.day_month) {
            labels.push(item.day_year + '-' + item.day_month);
          } else {
            labels.push(item.added_date);
          }
          dataset.data.push(item.total_view);
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

</style>
