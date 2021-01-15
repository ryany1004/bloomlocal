<template>
  <div v-loading.fullscreen="loading" class="search-results">
    <p class="mt-4 font-14">Search results for "{{ query }}":</p>
    <div v-if="type == 'all' || type == 'shop'">
      <h3 class="group-title">Shops:</h3>
      <div class="row shop-cards" v-if="shops.length > 0">
        <div class="col-lg-2 col-md-3 col-6 mb-5" v-for="shop in shops" :key="shop.id">
          <shop-card :shop="shop" :media-url="mediaUrl"></shop-card>
        </div>
      </div>
      <div v-else class="mb-5 font-14">
        <span v-if="!loading">Not Found</span>
        <span v-else>Searching...</span>
      </div>
    </div>

    <div v-if="type == 'all' || type == 'product'">
      <h3 class="group-title">Products:</h3>
      <div  class="row product-cards" v-if="products.length > 0">
        <div class="col-lg-2 col-md-3 col-6 mb-5" v-for="product in products" :key="product.id">
          <business-product-card v-if="user.role_type == '1'" :product="product" :media-url="mediaUrl"></business-product-card>
          <product-card v-else :product="product" :media-url="mediaUrl"></product-card>
        </div>
      </div >
      <div v-else class="mb-5 font-14">
        <span v-if="!loading">Not Found</span>
        <span v-else>Searching...</span>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import {mapState} from "vuex";

export default {
  name: "SearchPage",
  props: {
    mediaUrl: {
      type: String,
      default: ""
    },
    type: {
      type: String,
      default: ""
    },
    query: {
      type: String,
      default: ""
    }
  },
  data: function () {
    return {
      products: [],
      shops: [],
      loading: false
    }
  },
  beforeMount() {
    this.$store.dispatch('get_user');
  },
  created() {
    if (this.type == 'product') {
      this.search_product()
    } else if (this.type == 'shops') {
      this.search_shop()
    } else {
      this.search_product();
      this.search_shop()
    }
  },
  computed: {
    ...mapState([
        'user'
    ])
  },
  methods: {
    search_product() {
      let that = this;
      that.loading = true;
      axios.get(`/api/product/search/?query=${this.query}`).then((res) => {
        that.products = res.data;
        that.loading = false;
      }).catch(() => {
        that.loading = false;
      })
    },
    search_shop() {
      let that = this;
      that.loading = true;
      axios.get(`/api/shop/search/?query=${this.query}`).then((res) => {
        that.shops = res.data;
        that.loading = false;
      }).catch(() => {
        that.loading = false;
      })
    }
  }
}
</script>

<style lang="scss">
.search-results {
  .group-title {
    font-size: 20px;
    margin-bottom: 25px;
  }
}
</style>
