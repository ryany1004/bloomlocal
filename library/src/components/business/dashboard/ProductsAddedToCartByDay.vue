<template>
  <div v-loading="loading" style="padding: 10px">
    <line-chart :chart-data="chartData" :options="options" style="height: 270px"></line-chart>
  </div>
</template>

<script>
import LineChart from "@/components/charts/LineChart";
import axios from "axios";


export default {
  name: "ProductsAddedToCartByDay",
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
        }
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
      axios.get('/api/analytics/product-added-to-cart/').then(res => {
        let labels = []
        let dataset = {
          label: 'Products added to cart by day',
          data: []
        }
        res.data.forEach(item => {
          labels.push(item.added_date);
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
