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
  name: "StorefrontView",
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
        that.loading = false;
        that.chartData = {
          labels: [
            that.newDateString(-10),
            that.newDateString(-9),
            that.newDateString(-8),
            that.newDateString(-7),
            that.newDateString(-6),
            that.newDateString(-5),
            that.newDateString(-4),
            that.newDateString(-5),
            that.newDateString(-2),
            that.newDateString(-1),
            that.newDateString(0)
          ],
          datasets: [{
            label: 'Storefront views',
            data: [33, 72, 60, 50, 80, 100, 200, 150, 180, 160, 57]
          }],
          options: {
            title: {
              text: 'Storefront views'
            },
          }
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
