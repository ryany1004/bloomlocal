<template>
  <div class="d-flex flex-column justify-content-center mt-4" v-loading.fullscreen="loading">
    <img src="../../assets/bloom.svg" style="height: 50px"/>
    <p class="text-center mb-1 mt-3">Dear</p>
    <p class="text-center mb-1">{{ order.shipping_address.first_name }} {{ order.shipping_address.last_name }}</p>
    <p class="text-center mb-3">Your order is confirmed</p>
    <i class="fas fa-check-circle fa-2x text-center color-1"></i>
    <p class="text-center mt-3 mb-5 font-14">Thank you for shopping with us.</p>

    <div class="order-content">
      <div class="order-details d-flex flex-column">
        <p class="text-center">Order</p>
        <span class="order-no mx-auto">#{{ order.id }}</span>

        <div class="row" style="padding: 20px;">
          <div class="col d-flex justify-content-center align-items-center border-right pr-5">
            <a href="/my-purchase/" class="btn btn-primary btn-manage-order white font-10">VIEW OR MANAGE YOUR ORDER</a>
          </div>
          <div class="col pl-5" style="line-height: 24px;">
            Subtotal: ${{ order.total_price }}<br>
            Tax: ${{ order.tax }}<br>
            Total: ${{ order.total_price + order.tax }}
          </div>
        </div>
      </div>

      <div class="d-flex justify-content-between mt-4 mb-5">
        <a href="/" class="btn btn-primary font-12 white">
          <svg width="17" height="14" viewBox="0 0 17 17" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M8.62757 11.7218L7.21641 13.139L0.838745 6.7888L7.18897 0.411133L8.60623 1.82229L4.82971 5.61514L15.1353 5.59292C17.3445 5.58815 19.1392 7.37515 19.144 9.58428L19.1612 17.5843L17.1612 17.5886L17.144 9.5886C17.1416 8.48403 16.2442 7.59053 15.1396 7.59291L4.50391 7.61584L8.62757 11.7218Z" fill="#FEFEFE"/>
          </svg>
          <span class="ml-2">Continue Shopping</span></a>
        <a href="/my-purchase/" class="color-1">Track your order</a>
      </div>
    </div>

  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "OrderSuccess",
  props: {
    uuidOrder: {
      type: String,
      required: true
    }
  },
  data: function () {
    return {
      loading: false,
      order: {
        shipping_address: {},
        shopper: {},
      }
    }
  },
  computed: {
    tax_value() {
      return this.order.total_price * this.order.com
    }
  },
  created() {
    let that = this;
    that.loading = true;
    axios.get(`/api/order/${this.uuidOrder}/details/`).then((res) => {
      that.order = res.data;
      that.loading = false;
    }).catch((err) => {
      console.log(err);
      that.loading = false;
      alert("Unable get your order");
    })
  },
  methods: {

  }
}
</script>

<style lang="scss" scoped>
.order-content {
  max-width: 600px;
  width: 100%;
  margin: 0 auto;

  .order-details {
    background: #FEFEFE;
    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.12);
    border-radius: 10px;
    padding: 15px;
    font-size: 14px;

    .border-right {
      border-color: #4FC5E9;
    }

    .order-no {
      padding: 10px 40px;
      background: #FDE8AF;
      border-radius: 10px;
      font-size: 14px;
    }
  }
}
</style>
