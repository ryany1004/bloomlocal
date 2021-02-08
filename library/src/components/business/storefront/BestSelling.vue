<template>
  <div v-loading.fullscreen="loading" class="row product-cards">
    <div class="col-lg-3 col-md-4 col-6 mb-5" v-for="product in data_products" :key="product.id">
      <business-product-card :product="product" :media-url="mediaUrl"></business-product-card>
    </div>
    <div class="col-12" v-if="products.length == 0">
      {{ loading ? "Loading...": "No data" }}
    </div>
  </div>
</template>

<script>
import axios from "axios";
import _ from "lodash";

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
    data_products() {
      if (this.orderBy == 'title') {
        return _.orderBy(this.products, this.orderBy)
      } else if (this.orderBy == 'price') {
        return _.orderBy(this.products, this.orderBy);
      } else {
        return this.products
      }
    }
  },
  methods: {

  }
}
</script>

<style scoped>

</style>
