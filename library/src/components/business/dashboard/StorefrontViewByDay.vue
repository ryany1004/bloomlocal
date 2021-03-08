<template>
  <div>
    <div class="d-flex justify-content-between">
      <p class="bolder font-14" style="margin: 0px 0 0 15px">Storefront views</p>
      <time-filter v-model="filter_time"></time-filter>
    </div>
    <div v-loading="loading" style="padding: 10px;">
      <line-chart :chart-data="chartData" :options="options" style="height: 270px"></line-chart>
    </div>
  </div>
</template>

<script>
import LineChart from "@/components/charts/LineChart";
import moment from "moment";
import axios from "axios";
import TimeFilter from "@/components/business/dashboard/TimeFilter";

let timeFormat = 'MMM D';

export default {
  name: "StorefrontViewByDay",
  components: {
    TimeFilter,
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
      filter_time: "today"
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
      axios.get(`/api/analytics/storefront-view/?type=${this.filter_time}`).then(res => {
        let labels = []
        let dataset = {
          label: 'Storefront views',
          data: []
        }
        res.data.forEach(item => {
          labels.push(item.viewed_date);
          dataset.data.push(item.count);
        })
        that.loading = false;
        that.chartData = {
          labels: labels,
          datasets: [dataset]
        }
      });
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
