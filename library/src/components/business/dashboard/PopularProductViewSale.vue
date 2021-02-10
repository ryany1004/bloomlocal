<template>
  <div class="report-box" style="height: 100%" v-loading="loading">
    <p class="font-14">Popular Products View and Sale</p>
    <ul class="popular-products mb-0" v-if="products.length > 0" v-slimscroll="{height: '270px'}">
      <li class="d-flex align-items-center" v-for="product in products" :key="product.id">
        <div class="d-flex">
          <img :src="`${mediaUrl}${product.thumbnail}`">
          <strong class="ml-3">{{ product.title }}</strong>
        </div>
        <a class="ml-auto" style="color: #333" :href="product.url"><i class="far fa-chevron-right"></i></a>
      </li>
    </ul>
    <p v-else class="font-14 mt-2">{{ loading ? "Loading...": "No data"}}</p>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "PopularProductViewSale",
  props: {
    mediaUrl: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      loading: false,
      products: []
    }
  },
  created() {
    this.get_data()
  },
  methods: {
    get_data() {
      let that = this;
      that.loading = true
      axios.get('/api/analytics/popular-products-sale-and-view/').then(res => {
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

<style scoped lang="scss">
.report-box {
  background: #FFFFFF;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.12);
  .popular-products {
    list-style: none;
    padding-left: 0;
    li {
      margin-bottom: 35px;
      padding-right: 20px;
      img {
        width: 56px;
        height: 56px;
      }
    }
    li:last-child {
      margin-bottom: 0;
    }
  }
}
</style>
