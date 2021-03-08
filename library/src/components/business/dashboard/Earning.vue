<template>
  <div class="wbox earning" v-loading="loading">
    <p class="head1 text-center mb-0">Your earning this month</p>
    <p class="earning-num text-center mb-1">{{ total | numFormat("0.00") }}</p>
    <p class="head2 text-center">Update your payout method in Settings</p>
    <div class="d-flex justify-content-center">
      <button class="btn btn-withdraw">Withdraw All Earning</button>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Earning",
  data() {
    return {
      loading: false,
      total: 0
    }
  },
  created() {
    this.get_data();
  },
  methods: {
    get_data() {
      let that = this;
      that.loading = true;
      axios.get(`/api/analytics/revenue-total/?type=this_month`).then((res) => {
        that.total = res.data.total;
        that.loading = false;
      }).catch(() => {
        that.loading = false;
      })
    }
  }
}
</script>

<style lang="scss">
  .earning {
    padding: 32px;
    .head1 {
      font-weight: bold;
      font-size: 18px;
    }
    .earning-num {
      font-weight: 900;
      font-size: 72px;
      color: #00AEEF;
    }
    .head2 {
      font-size: 14px;
      color: #919EAB;
    }
    .btn-withdraw {
      background: #F4F6F8;
      border-radius: 16px;
      font-weight: bold;
      font-size: 14px;
      color: #00AEEF;
      padding: 16px 50px;
    }
  }
</style>
