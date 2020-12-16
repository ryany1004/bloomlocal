<template>
  <div v-loading.fullscreen="loading">No data</div>
</template>

<script>
import axios from "axios";

export default {
  name: "BestSelling",
  props: {
    orderBy: {
      type: String
    },
    mediaUrl: {
      type: String,
      default: ""
    },
  },
  data: function () {
    return {
      products: [],
      loading: false,
    }
  },
  created() {
    let that = this;
    that.loading = true;
    axios.get('/api/shop/products/?view=best_selling').then(function (res) {
      that.products = res.data
      that.loading = false
    }).catch(function () {
      that.loading = false
    })
  },
  computed: {

  },
  methods: {

  }
}
</script>

<style scoped>

</style>
