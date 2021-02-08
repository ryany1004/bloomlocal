<template>
  <div v-loading.fullscreen="loading" class="search-results">
    <div class="mt-4 row">
      <p class="font-14 col-6">Search results for "{{ query }}":</p>
      <div class="form-check col-6">
        <input class="form-check-input" type="checkbox" v-model="nearest_by_me"
               id="defaultCheck1" :checked="nearest_by_me" @change="init_search_nearest()">
        <label class="form-check-label font-14" for="defaultCheck1">
          Nearest by me (within {{ limitDistance }}km from your current location)
        </label>
      </div>
    </div>
    <div v-if="type == 'all' || type == 'shop'">
      <h3 class="group-title">Shops:</h3>
      <div class="row shop-cards" v-if="shops.length > 0">
        <div class="col-lg-2 col-md-3 col-6 mb-5" v-for="shop in data_shops" :key="shop.id">
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
        <div class="col-lg-2 col-md-3 col-6 mb-5" v-for="product in data_products" :key="product.id">
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
import _ from "lodash";

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
    },
    limitDistance: {
      type: Number,
      default: 20
    }
  },
  data: function () {
    return {
      products: [],
      shops: [],
      loading: false,
      nearest_by_me: false
    }
  },
  beforeMount() {
    this.$store.dispatch('get_user');
  },
  created() {
    let nearest_by_me = localStorage.getItem("nearest_by_me")
    if (nearest_by_me == "true") {
      this.nearest_by_me = true;
      this.init_search_nearest();
    } else {
      this.search_normal();
    }
  },
  computed: {
    ...mapState([
        'user'
    ]),
    data_shops() {
      if (this.nearest_by_me) {
        return _.orderBy(this.shops, 'distance')
      }
      return this.shops;
    },
    data_products() {
      if (this.nearest_by_me) {
        return _.orderBy(this.products, 'distance')
      }
      return this.products;
    }
  },
  methods: {
    search_product(location) {
      let that = this;
      that.loading = true;
      let url = `/api/product/search/?query=${this.query}`;
      if (location) {
        url = `${url}&lat=${location.coords.latitude}&long=${location.coords.longitude}`
      }
      axios.get(url).then((res) => {
        that.products = res.data;
        that.loading = false;
      }).catch(() => {
        that.loading = false;
      })
    },
    search_shop(location) {
      let that = this;
      that.loading = true;
      let url = `/api/shop/search/?query=${this.query}`;
      if (location) {
        url = `${url}&lat=${location.coords.latitude}&long=${location.coords.longitude}`
      }
      axios.get(url).then((res) => {
        that.shops = res.data;
        that.loading = false;
      }).catch(() => {
        that.loading = false;
      })
    },
    init_search_nearest() {
      localStorage.setItem('nearest_by_me', this.nearest_by_me);
      if (this.nearest_by_me) {
        if (navigator.geolocation) {
          navigator.geolocation.getCurrentPosition(this.search_nearest.bind(this), () => {
            alert("Unable to get your location! Please allow enable your location on your browser if you want location search");
          });
        } else {
          alert("Geolocation is not supported by this browser.");
        }
      } else {
        this.search_normal();
      }
    },
    search_normal() {
      if (this.type == 'product') {
        this.search_product()
      } else if (this.type == 'shop') {
        this.search_shop()
      } else {
        this.search_product();
        this.search_shop()
      }
    },
    search_nearest(location) {
      if (this.type == 'product') {
        this.search_product(location)
      } else if (this.type == 'shop') {
        this.search_shop(location)
      } else {
        this.search_product(location);
        this.search_shop(location)
      }
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
