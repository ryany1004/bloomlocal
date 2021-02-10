<template>
  <div v-loading="loading">
    <line-chart :chart-data="chartData" :options="options" style="height: 190px"></line-chart>
  </div>
</template>

<script>
import LineChart from "@/components/charts/LineChart";
import moment from "moment";

let timeFormat = 'MMM D';

export default {
  name: "Earning",
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
      setTimeout(() => {
        let labels = []
        let dataset = {
          label: '',
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
            "Oct",
            "Nov",
            "Dec",
            "Jan",
            "Feb",
          ],
          datasets: [{
            label: 'Earning',
            data: [3, 20, 15, 40, 25],
            backgroundColor: 'rgba(108, 93, 211,0.3)',
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
