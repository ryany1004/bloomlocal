<template>
  <div v-loading="loading" style="padding: 10px;overflow: auto">
    <line-chart :chart-data="chartData" :options="options" style="height: 270px"></line-chart>
  </div>
</template>

<script>
import LineChart from "@/components/charts/LineChart";
import axios from "axios";

export default {
  name: "RevenueByDay",
  components: {
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
              beginAtZero: true
            }
          }]
        }
      },
      loading: false,
    }
  },
  computed: {
    top_products() {
      return Array.from(new Set(this.labels))
    }
  },
  created() {
    this.get_data();
  },
  methods: {
    get_data() {
      let that = this;
      that.loading = true
      axios.get('/api/analytics/shop-revenue/').then(res => {
        let labels = []
        let dataset = {
          label: 'Revenue by Day',
          data: []
        }
        res.data.forEach(item => {
          labels.push(item.day);
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
