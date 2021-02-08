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
  name: "MostViewProducts",
  components: {
    LineChart
  },
  data() {
    return {
      chartData: null,
      options: {
        maintainAspectRatio:false,
        responsive: true,
        tooltips: {
          callbacks: {
              label: function(tooltipItem, data) {
                  let dataset = data.datasets[tooltipItem.datasetIndex];
                  let index = tooltipItem.index;
                  return dataset.labels[index] + ': ' + dataset.data[index] + " views";
              }
          }
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
          label: 'Top Viewed Products',
          backgroundColor: 'rgba(28, 207, 247,0.1)',
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
            labels: ['iPhone', 'Airpods', 'Digital Pipe Fitting', 'V.NiceBag', 'iMac', 'V.NiceBag', 'iPhone',],
            label: 'Top Viewed Products',
            data: [100, 45, 56, 34, 86, 54, 94],
            backgroundColor: 'rgba(28, 28, 247, 0.2)',
          }],
          options: {
            title: {
              text: 'Top Viewed Products'
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
