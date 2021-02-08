<template>
  <div v-loading="loading" style="padding: 20px">
    <line-chart :chart-data="chartData" :options="options" style="height: 270px"></line-chart>
  </div>
</template>

<script>
import LineChart from "@/components/charts/LineChart";
import moment from "moment";

let timeFormat = 'MMM D';

export default {
  name: "ProductsAddedToCart",
  components: {
    LineChart
  },
  data() {
    return {
      chartData: null,
      options: {
        maintainAspectRatio:false,
        responsive: true,
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
      setTimeout(() => {
        let labels = []
        let dataset = {
          label: 'Top Viewed Products',
          data: []
        }
        let data = []
        data.forEach(item => {
          labels.push(item.name);
          dataset.data.push(item.total);
        })
        that.loading = false;
        that.chartData = {
          labels: [
            that.newDateString(-6),
            that.newDateString(-5),
            that.newDateString(-4),
            that.newDateString(-5),
            that.newDateString(-2),
            that.newDateString(-1),
            that.newDateString(0)
          ],
          datasets: [{
            label: 'Products Added To Cart',
            data: [2, 5, 3, 4, 6, 3, 2],
            backgroundColor: 'rgba(28, 207, 247,0.2)',
          }]
        }
      }, 1000);
    },
    newDate(days) {
			return moment().add(days, 'd').toDate();
		},

		newDateString(days) {
			return moment().add(days, 'd').format(timeFormat);
		}
  }
}
</script>

<style scoped>

</style>
