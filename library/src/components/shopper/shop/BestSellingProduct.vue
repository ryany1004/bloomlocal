<template>
  <div v-loading.fullscreen="loading">
    <div  class="row product-cards" v-if="products.length > 0">
      <div class="col-lg-3 col-md-4 col-6 mb-5" v-for="product in data_products" :key="product.id">
        <product-card :product="product" :media-url="mediaUrl"></product-card>
      </div>
    </div >
    <div v-else>
      No Data
    </div>
  </div>
</template>

<script>
import _ from "lodash";
import axios from "axios";

export default {
  name: "BestSellingProduct",
  props: {
    shopId: {
      type: Number,
      required: true
    },
    orderBy: {
      type: String
    },
    mediaUrl: {
      type: String,
      default: ""
    }
  },
  data: function () {
    return {
      products: [],
      loading: false
    }
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
  created() {
    let that = this;
    that.loading = true;
    axios.get(`/api/shop/${this.shopId}/products/?view=best_selling`).then(function (res) {
      that.products = res.data
      that.loading = false
    }).catch(function () {
      that.loading = false
    })
  },
  methods: {

  }
}
</script>

<style scoped>

</style>
