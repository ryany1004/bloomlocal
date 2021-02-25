<template>
  <div class="revenue" v-loading="loading">
    <p>Storefront Views</p>
    <div class="d-flex justify-content-between align-items-center mt-5">
      <div>{{ percent_increase.toFixed(0) }}% <span title="Month-over-Month (MoM) is a comparison of current month performance to the previous month performance" v-b-tooltip.hover>MoM</span></div>
      <div>
        This month
        <div class="d-flex justify-content-between align-items-center mt-2">
          <i :title="`${amount_increase >0 ? '+': ''}${amount_increase}`" v-b-tooltip.hover class="fas"
             :class="{
              'fa-arrow-up': amount_increase > 0,
              'fa-arrow-down': amount_increase < 0,
              'fa-horizontal-rule': amount_increase == 0,
              'color-1': amount_increase >= 0,
              'color-red': amount_increase < 0,}"></i>
          <span>{{ total_amount | numFormat }}</span>
        </div>
      </div>
    </div>
    <div class="progress mt-2" style="height: 20px;border-radius: 15px;">
      <div class="progress-bar bg-success" role="progressbar" :style="{width: `${progress_bar}%`}" aria-valuenow="25" aria-valuemin="0" aria-valuemax="100"></div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "StorefrontViewByMonth",
  data() {
    return {
      loading: false,
      month_data: {}
    }
  },
  computed: {
    progress_bar() {
      if (this.percent_increase > 0) {
        return this.percent_increase <= 100 ? this.percent_increase : 100
      }
      return 0
    },
    total_amount() {
      if (this.month_data.this_month) {
        return this.month_data.this_month;
      }
      return "N/A"
    },
    amount_increase() {
      let data = this.month_data
      if (data.this_month) {
        return data.this_month - data.last_month;
      }
      return 0;
    },
    percent_increase() {
      if (this.month_data.last_month > 0) {
        return this.amount_increase / this.month_data.last_month * 100;
      } else if (this.month_data.last_month == 0 && this.month_data.this_month > 0) {
        return 100;
      }
      return 0;
    }
  },
  created() {
    this.get_data();
  },
  methods: {
    get_data() {
      let that = this;
      that.loading = true
      axios.get("/api/analytics/storefront-view/?type=month").then(res => {
        that.loading = false;
        that.month_data = res.data;
      })
    }
  }
}
</script>

<style lang="scss">

</style>
