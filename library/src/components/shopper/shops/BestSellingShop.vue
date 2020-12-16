<template>
  <div v-loading.fullscreen="loading">
    No Data
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "BestSellingShop",
  data: function () {
    return {
      shops: [],
      loading: false
    }
  },
  computed: {

  },
  created() {
    let that = this;
    that.loading = true
    axios.get("/api/shops/?view=best_selling").then((res) => {
      that.loading = false;
      that.shops = res.data;
    })
  },
  methods: {

  }
}
</script>

<style scoped>

</style>
