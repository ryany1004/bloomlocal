<template>
  <div v-loading.fullscreen="loading" class="row">
    <div class="order-details mb-5 col-12 col-md-12 col-lg-9" v-for="order in orders" :key="order.id">
      <div class="d-flex justify-content-between order-header mb-3">
        <span>Order #{{ order.order_no }}</span>
        <span>Total price = ${{ order.total_price | numFormat("0.00") }}</span>
      </div>
      <div class="order-items row">
        <div class="col-6 d-flex mb-4" v-for="item in order.order_items" :key="item.id">
          <a :href="item.product.url" style="flex: 0 0 160px">
            <div class="product-image" :style="{backgroundImage: `url('${mediaUrl}${item.product.thumbnail}')`}">
            </div>
          </a>
          <div>
            <h3 class="font-14 product-title mt-1">{{ item.product.title }}</h3>
            <p class="font-10 product-desc mt-2" style="white-space: pre-line">{{ item.product.description }}</p>
            <div class="d-flex align-items-center mt-3">
              <span class="item-status mr-4">{{ order.order_status}}</span>
              <a class="btn btn-primary btn-sm font-10 white" :href="item.product.url">Buy it again</a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "MyPurchase",
  props: {
    mediaUrl: {
      type: String,
      default: ""
    }
  },
  data: function () {
    return {
      orders: [],
      loading: false
    }
  },
  computed: {

  },
  created() {
    this.get_orders();
  },
  methods: {
    get_orders() {
      let that = this;
      that.loading = true;
      axios.get('/api/user/orders/').then(res => {
        that.orders = res.data;
        that.loading = false;
      }).catch(() => {
        that.loading = false;
      })
    }
  }
}
</script>

<style lang="scss">
.order-details {
  .order-header {
    padding: 15px;
    background-color: #4FC5E9;
    color: white;
    border-radius: 10px;
  }
  .product-image {
    width: 140px;
    height: 140px;
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    border: 1px solid #f8f8f8;
    border-radius: 10px;
  }
  .item-status {
    color: #27AE60;
    font-size: 10px;
  }
  .product-title {
    height: 32px;
    overflow: hidden;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    font-weight: bolder;
  }
  .product-desc {
    height: 45px;
    overflow: hidden;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
  }
}
</style>
