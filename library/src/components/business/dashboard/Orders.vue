<template>
  <div class="wbox sm-box" v-loading="loading">
    <div class="d-flex justify-content-between align-items-center d-filter-opts">
      <strong>Orders</strong>
      <time-filter v-model="filter_time"></time-filter>
    </div>
    <div class="summary-st d-flex align-items-center mt-3">
      <i class="a-icon a-orders"></i>
      <span>{{ count }}</span>
    </div>
  </div>
</template>

<script>
import TimeFilter from "@/components/business/dashboard/TimeFilter";
import axios from "axios";
export default {
  name: "Orders",
  components: {TimeFilter},
  data() {
    return {
      filter_time: "today",
      count: 0,
      loading: false
    }
  },
  watch: {
    filter_time: {
      handler() {
        this.get_data();
      }
    }
  },
  mounted() {
    this.get_data();
  },
  methods: {
    get_data() {
      let that = this;
      that.loading = true;
      axios.get(`/api/analytics/order-count/?type=${this.filter_time}`).then((res) => {
        that.count = res.data.count;
        that.loading = false;
      }).catch(() => {
        that.loading = false;
      })
    }
  }
}
</script>

<style scoped>

</style>
