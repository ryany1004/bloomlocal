<template>
  <div>
    <div class="d-flex justify-content-between">
      <p class="bolder font-14" style="margin: 0px 0 0 15px">Product Views by Day</p>
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
  name: "ProductsViewByDay",
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
  computed: {
    top_products() {
      return Array.from(new Set(this.labels))
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
      axios.get(`/api/analytics/product-view/?type=${this.filter_time}`).then(res => {
        let labels = []
        let dataset = {
          label: 'Product Views by Day',
          data: []
        }
        res.data.forEach(item => {
          labels.push(item.viewed_date);
          dataset.data.push(item.total_view);
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
.top-products {
  list-style: none;
}
</style>
