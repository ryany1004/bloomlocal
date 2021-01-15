<template>
  <div v-loading="loading" style="padding: 20px">
    <line-chart :chart-data="chartData" :options="options" style="height: 270px"></line-chart>
  </div>
</template>

<script>
import LineChart from "@/components/charts/LineChart";
import axios from "axios";

export default {
  name: "ProductSalesChart",
  components: {
    LineChart
  },
  data() {
    return {
      chartData: null,
      options: {
        maintainAspectRatio:false,
        responsive: true
      },
      loading: false
    }
  },
  created() {
    this.get_data();
  },
  methods: {
    get_data() {
      let that = this;
      that.loading = true
      axios.get('/api/statistic/order-revenue/by-year/').then(res => {
        let labels = []
        let dataset = {
          label: 'Product sales Chart',
          backgroundColor: 'rgba(28, 207, 247,0.1)',
          data: []
        }
        res.data.forEach(item => {
          labels.push(item.year);
          dataset.data.push(item.total);
        })
        that.loading = false;
        that.chartData = {
          "labels": labels,
          "datasets": [dataset]
        }
      })
    }
  }
}
</script>

<style scoped>

</style>
