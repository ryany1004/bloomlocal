<template>
  <div class="report-box" style="height: 100%" v-loading="loading">
    <div class="d-flex justify-content-between">
      <p class="chart-title">Products Add To Cart</p>
      <time-filter v-model="filter_time"></time-filter>
    </div>
    <ul class="popular-products mb-0" v-if="products.length > 0">
      <li class="d-flex align-items-center" v-for="product in products" :key="product.id">
        <div class="product-thumb">
          <img :src="`${mediaUrl}${product.thumbnail}`">
        </div>
        <div class="product-title flex-grow-1">
          {{ product.title }}
        </div>
        <div class="product-price">
          ${{ product.price | numFormat("0.00") }}
        </div>
        <div class="data-count">
          {{ product.analytics.product_add_to_cart_count }}
        </div>
      </li>
    </ul>
    <p v-if="products.length == 0" class="font-14 mt-2">{{ loading ? "Loading...": "No data"}}</p>
  </div>
</template>

<script>
import axios from "axios";
import TimeFilter from "@/components/business/dashboard/TimeFilter";

export default {
  name: "TopProductsAddToCart",
  components: {TimeFilter},
  props: {
    mediaUrl: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      loading: false,
      products: [],
      filter_time: "today"
    }
  },
  created() {
    this.get_data()
  },
  watch: {
    filter_time: {
      handler: function () {
        this.get_data();
      }
    }
  },
  methods: {
    get_data() {
      let that = this;
      that.loading = true
      axios.get(`/api/analytics/top-products-add-to-cart/?type=${this.filter_time}`).then(res => {
        that.loading = false;
        that.products = res.data;
      }).catch(err => {
        console.log(err);
        that.loading = false;
      })
    }
  }
}
</script>

<style  lang="scss">
.report-box {
  background: #FFFFFF;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.12);
  .popular-products {
    list-style: none;
    padding-left: 0;
    height: 250px;
    overflow-y: auto;

    li {
      margin-bottom: 24px;
      .product-thumb {
        border: 1px solid #F4F6F8;
        filter: drop-shadow(0px 28px 32px rgba(0, 0, 0, 0.03));
        background-color: #fff;
        border-radius: 16px;
        width: 64px;
        height: 64px;
        img {
          width: 64px;
          height: 64px;
          border-radius: 16px;
        }
      }
      .product-title {
        font-size: 14px;
        color: #212B36;
        margin-left: 17px;
      }
      .product-price {
        flex: 0 0 21%;
        text-align: right;
        font-size: 16px;
        color: #212B36;
      }
      .data-count {
        flex: 0 0 21%;
        text-align: center;
        font-size: 16px;
        color: #212B36;
      }
    }
    li:last-child {
      margin-bottom: 0;
    }
  }
}
</style>
