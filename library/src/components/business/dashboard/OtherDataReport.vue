<template>
  <div class="per-order" style="height: 100%" v-loading="loading">
    <ul class="store-summary">
      <li>
        <strong>Avg. order amount:</strong> <span>${{ data.avg_order_amount | numFormat("0.00") }}</span>
      </li>
      <li class="d-flex align-items-center">
        <strong>Avg. product count per order:</strong> <span>{{ data.avg_product_per_order }}</span>
      </li>
    </ul>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "OtherDataReport",
  data() {
    return {
      data: {},
      loading: false
    }
  },
  created() {
    this.get_data();
  },
  methods: {
    get_data() {
      let that = this;
      that.loading = true;
      axios.get('/api/analytics/other-data-report/').then(res => {
        that.loading = false;
        that.data = res.data;
      })
    }
  }
}
</script>

<style scoped lang="scss">
.store-summary {
  list-style: none;
  padding-left: 0;
  margin-bottom: 0;
  li {
    display: flex;
    margin-bottom: 10px;
    span {
      margin-left: auto !important;
    }
  }
  li:last-child {
    margin-bottom: 0;
  }
}
</style>
