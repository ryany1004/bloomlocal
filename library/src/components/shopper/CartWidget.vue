<template>
  <div class="cart-widget">
    <a href="javascript:void(0)" class="btn-my-cart" @click="cart_visible = true">
      <i ref="icon" class="fal fa-shopping-cart cart-color"></i>
      <span ref="count" class="cart-count" v-if="cart_items.length > 0"> {{cart_items.length}}</span>
    </a>

    <b-sidebar id="sidebar-right" v-model="cart_visible" title="Sidebar" shadow right header-class="header-cart" width="380px">
      <template #header="{ hide }">
       <div class="d-flex align-items-center justify-content-between" style="flex: 1">
        <span>My Cart</span>
        <a href="javascript:void(0)" @click="hide"><i class="fal fa-times white"></i></a>
       </div>
      </template>
      <cart :media-url="mediaUrl"></cart>
      <template #footer>
        <div class="p-3" v-if="cart_items.length > 0">
          <a href="/order/overview/" class="btn btn-primary btn-lg btn-block" style="font-size: 16px">Proceed To Checkout</a>
        </div>
      </template>
    </b-sidebar>
  </div>
</template>

<script>
import {mapState} from "vuex";

export default {
  name: "CartWidget",
  props: {
    mediaUrl: {
      type:String,
      required: true
    }
  },
  data: function () {
    return {
      cart_visible: false
    }
  },
  computed: {
    ...mapState([
      "cart_items",
    ]),
  },
  created() {
    this.$store.dispatch('get_cart');
  },
  methods: {

  }
}
</script>

<style lang="scss">
.cart-widget {
  .btn-my-cart {
    margin-left: 20px;
    text-decoration: none;
    .cart-color {
      color: #0C242E;
    }
    .cart-count {
      color: #4F4F4F;
    }
  }
  .header-cart {
    background-color: #4FC5E9;
    color: #FFFCFF;
    font-size: 16px;
    padding: 0.75rem 1rem;
  }
  .b-sidebar {
    background-color: #fff !important;
  }
  .b-sidebar-footer a {
    color: #FFFCFF !important;
  }
}
</style>
