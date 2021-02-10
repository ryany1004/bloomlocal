<template>
  <div class="pie-chart h-100" v-loading="loading" style="padding: 20px">
    <div class="h-100">
      <div class="mb-4">
        <div class="d-flex justify-content-around align-items-center">
          <a href="javascript:void(0)" @click="go_back()"><i class="far fa-chevron-left"></i></a>
          <a class="month-normal"  href="javascript:void(0)" @click="go_back()"><span >{{ last_month | moment("MMM") }}</span></a>
          <span class="active-month">{{ this_month | moment("MMM") }}</span>
          <a class="month-normal" href="javascript:void(0)" @click="go_next()"><span >{{ next_month | moment("MMM") }}</span></a>
          <a href="javascript:void(0)" @click="go_next()"><i class="far fa-chevron-right"></i></a>
        </div>
      </div>

      <pie-chart v-if="titles.length > 0" :chart-data="chartData" :options="options" style="height: 215px"></pie-chart>
      <div class="d-flex justify-content-center" v-if="titles.length > 0">
        <ul class="titles">
          <li class="d-flex align-items-center font-12" v-for="(title, index) in titles" :key="index">
            <span class="circle-chart" :style="{backgroundColor: backgroundColor[index]}"></span> <span>{{ title }}</span>
          </li>
        </ul>
      </div>

      <div class="mt-3 h-100 d-flex align-items-center justify-content-center" v-if="titles.length == 0 && !loading">
        <p style="color: #eee">No Data</p>
      </div>
    </div>
  </div>
<!--    <img src="../../../assets/pie-chart.png" height="499" width="350"/>-->
</template>

<script>
import PieChart from "../../charts/PieChart";
import axios from "axios";
import moment from "moment";

export default {
  name: "SalePieChart",
  components: {
    PieChart
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
      loading: false,
      this_month: new Date(),
      titles: [],
      backgroundColor: [
        'green',
        'blue',
        'orange',
        'red',
        'brown',
        'yellow'
      ]
    }
  },
  computed: {
    last_month() {
      let month = this.this_month;
      if (month.getMonth() == 0) {
        return null
      }
      return new Date(month.getFullYear(), month.getMonth() - 1, month.getDate())
    },
    next_month() {
      let month = this.this_month;
      if (month.getMonth() == 11) {
        return null;
      }
      return new Date(month.getFullYear(), month.getMonth() + 1, month.getDate())
    }
  },
  watch: {
    this_month: {
      handler(val) {
        this.get_data(val);
      }
    }
  },
  created() {
    this.get_data(this.this_month);
  },
  methods: {
    get_data(val) {
      let that = this;
      that.loading = true;
      let month = moment(val).format("YYYY-MM-DD")
      axios.get(`/api/analytics/sale-pie-chart/?month=${month}`).then((res) => {
        that.loading = false;
        that.chartData = {
          datasets: [{
            data: res.data.data,
            backgroundColor: that.backgroundColor
          }],
          labels: res.data.labels
        }
        that.titles = res.data.titles;
      }).catch(err => {
        console.log(err);
        that.loading = false;
      })
    },
    go_next() {
      if (this.this_month.getMonth() < 11) {
        let month = this.this_month;
        this.this_month = new Date(month.getFullYear(), month.getMonth() + 1, month.getDate());
      }
    },
    go_back() {
      if (this.this_month.getMonth() > 0) {
        let month = this.this_month;
        this.this_month = new Date(month.getFullYear(), month.getMonth() - 1, month.getDate());
      }
    }
  }
}
</script>

<style scoped lang="scss">
.active-month {
  font-size: 16px;
  color: #4FC5E9;
}
.month-normal {
  font-size: 12px;
  color: #8D9AA9;
}
.titles {
  list-style: none;
  padding-left: 0;
  margin-top: 50px;

  li {
    margin-bottom: 15px;
  }
  .circle-chart {
    width: 25px;
    height: 25px;
    border-radius: 50%;
    display: inline-block;
    margin-right: 10px;
  }
}
</style>
