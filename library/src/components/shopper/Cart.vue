<template>
  <div class="my-cart p-3">
    <ul class="cart-items">
      <li v-for="item in cart_items" :key="item.product.id">
        <div class="d-flex">
          <a :title="item.product.title" :href="item.product.url">
            <div class="item-img" :style="{backgroundImage: `url('${mediaUrl}${item.product.thumbnail}')`}">
            </div>
          </a>
          <div class="d-flex flex-column pl-2" style="flex: 0 0 120px;width: 120px">
            <small>{{item.product.shop_name}}</small>
            <a :title="item.product.title" class="product-title" :href="item.product.url">{{ item.product.title }}</a>
            <small>{{ productVariant(item) }}</small>
          </div>
          <div class="form-row">
            <div class="col-2 d-flex align-items-center justify-content-end">
              <a href="javascript:void(0)" @click="descreate_quantity(item)"><i class="fal fa-minus color4f"></i></a>
            </div>
            <div class="col-3 d-flex align-items-center">
              <ValidationProvider rules="positive" v-slot="{ errors }">
              <input class="form-control quantity form-control-sm" readonly="" v-model="item.quantity" type="number" step="1" min="1" :class="{'is-invalid': errors.length > 0}">
              </ValidationProvider>
            </div>
            <div class="col-2 d-flex align-items-center justify-content-start">
              <a href="javascript:void(0)" @click="increate_quantity(item)"><i class="fal fa-plus color4f"></i></a>
            </div>
            <div class="col-3 d-flex align-items-center justify-content-end">
              <span class="font12">${{ item.quantity * item.price | numFormat("0.00") }}</span>
            </div>
            <div class="col-2 d-flex align-items-center justify-content-end">
              <a href="javascript:void(0)" @click="delete_product(item)"><i class="fal fa-times"></i></a>
            </div>
          </div>
        </div>
      </li>
    </ul>

    <div class="d-flex mt-4" v-if="cart_items.length > 0">
      <span class="ml-auto">Total: ${{ total_price | numFormat("0.00") }}</span>
    </div>
    <div class="mt-2" v-else>
      No product here.
    </div>
  </div>
</template>

<script>
import {mapState} from "vuex";
import { ValidationProvider, extend } from 'vee-validate';

extend('positive', value => {
  return value >= 1;
});

export default {
  name: "Cart",
  props: {
    mediaUrl: {
      type: String,
      required: true
    }
  },
  components: {
    ValidationProvider
  },
  computed: {
    ...mapState([
      "cart_items", 'sizes', 'colors'
    ]),
    total_price() {
      let total = 0;
      this.cart_items.forEach((item) => {
        total += (item.quantity * item.price);
      })
      return total;
    }
  },
  created() {
    this.$store.dispatch('get_colors');
    this.$store.dispatch('get_sizes');
  },
  methods: {
    productVariant(item) {
      let variants = [];
      if (item.color) {
        variants.push(item.color)
      }
      if (item.size) {
        variants.push(item.size)
      }
      return variants.join(", ");
    },
    increate_quantity(item) {
      item.quantity += 1;

      this.$store.dispatch("add_to_cart", {
        product_id: item.product.id,
        size: item.size,
        color: item.color,
        quantity: 1
      })
    },
    descreate_quantity(item) {
      if (item.quantity == 1) {
        this.delete_product(item);
        return;
      }
      item.quantity -= 1;
      this.$store.dispatch("add_to_cart", {
        product_id: item.product.id,
        size: item.size,
        color: item.color,
        quantity: -1
      })
    },
    delete_product(item) {
      if (confirm("Do you want to delete this product?")) {
        this.$store.dispatch("remove_item_cart", {
          product_id: item.product.id,
          size: item.size,
          color: item.color
        })
      }
    }
  }
}
</script>

<style lang="scss">
.my-cart {
  .cart-items {
    list-style: none;
    padding-left: 0;
    .font12 {
      font-size: 12px;
    }
    li {
      margin-bottom: 15px;
      background: #FEFEFE;
      border-radius: 10px;
      box-shadow: 0px 1px 6px rgba(0, 0, 0, 0.12);
      -webkit-box-shadow: 0px 1px 6px rgba(0, 0, 0, 0.12);
      -moz-box-shadow: 0px 1px 6px rgba(0, 0, 0, 0.12);
      -o-box-shadow: 0px 1px 6px rgba(0, 0, 0, 0.12);
      padding: 12px;

      .item-img {
        flex: 0 0 50px;
        width: 50px;
        height: 50px;
        background-size: contain;
        background-position: center;
        background-repeat: no-repeat;
      }
      .product-title {
        font-size: 12px;
        color: #0C242E;
        text-overflow: ellipsis;
        overflow: hidden;
        white-space: nowrap;
      }
      small {
        font-size: 10px;
      }
      input::-webkit-outer-spin-button,
      input::-webkit-inner-spin-button {
          /* display: none; <- Crashes Chrome on hover */
          -webkit-appearance: none;
          margin: 0; /* <-- Apparently some margin are still there even though it's hidden */
      }

      input[type=number] {
          -moz-appearance:textfield; /* Firefox */
      }
      .quantity {
        text-align: center;
        background-color: #F2F2F2;
      }
    }
  }
}
</style>
