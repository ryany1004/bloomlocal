<template>
  <div class="wbox sm-box" v-loading="loading">
    <div class="d-flex justify-content-between align-items-center d-filter-opts">
      <strong>Revenue</strong>
      <time-filter v-model="filter_time"></time-filter>
    </div>
    <div class="summary-st d-flex align-items-center mt-3">
      <i class="a-icon a-revenue"></i>
      <span>${{ total | numFormat }}</span>
    </div>
  </div>
</template>

<script>
import TimeFilter from "@/components/business/dashboard/TimeFilter";
import axios from "axios";
export default {
  name: "Revenue",
  components: {TimeFilter},
  data() {
    return {
      filter_time: "today",
      total: 0,
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
      axios.get(`/api/analytics/revenue-total/?type=${this.filter_time}`).then((res) => {
        that.total = res.data.total;
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
