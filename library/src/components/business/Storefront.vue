<template>
  <div v-loading.fullscreen="loading">
    <ul style="list-style: decimal">
      <li v-for="product in products" :key="product.id">Product: {{product.title}} ${{product.price}}</li>
    </ul>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Storefront",
  data: function () {
    return {
      products: [],
      loading: false
    }
  },
  created() {
    let that = this;
    that.loading = true;
    axios.get('/api/shop/products/').then(function (res) {
      that.products = res.data
      that.loading = false
    }).catch(function () {
      that.loading = false
    })
  }
}
</script>

<style scoped>

</style>
