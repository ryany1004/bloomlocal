<template>
  <div class="order-overview" v-loading.fullscreen="cartLoading || loading">
    <div class="mb-2">
      <div class="form-check form-check-inline">
        <input class="form-check-input" type="checkbox" id="inlineCheckbox1" v-model="sms_update">
        <label class="form-check-label" for="inlineCheckbox1">SMS Update</label>
      </div>
      <div class="form-check form-check-inline">
        <input class="form-check-input" type="checkbox" id="inlineCheckbox2" v-model="shopper_share_info">
        <label class="form-check-label" for="inlineCheckbox2">Support Local Businesses by Sharing your information</label>
      </div>
    </div>

    <div class="row">
      <div class="col-4">
        <ul class="cart-items">
          <li v-for="item in cart_items" :key="item.product.id">
            <div class="d-flex">
              <a :title="item.product.title" :href="item.product.url">
                <div class="item-img" :style="{backgroundImage: `url('${mediaUrl}${item.product.thumbnail}')`}">
                </div>
              </a>

              <div class="product-details d-flex align-items-center">
                <div>
                  <div class="product-title">{{item.product.title}}</div>
                  <div class="product-price">US ${{item.quantity * item.price | numFormat("0.00")}}</div>
                  <div class="shop-name">{{item.product.shop_name}}</div>
                  <div class="form-row product-qty">
                    <div class="col-2 d-flex align-items-center justify-content-end">Qty</div>
                    <div class="col-1 d-flex align-items-center justify-content-end">
                      <a href="javascript:void(0)" @click="descreate_quantity(item)"><i class="fal fa-minus color4f"></i></a>
                    </div>
                    <div class="col-3 d-flex align-items-center">
                      <input class="form-control quantity form-control-sm" readonly="" v-model="item.quantity" type="number" step="1" min="1">
                    </div>
                    <div class="col-1 d-flex align-items-center justify-content-start">
                      <a href="javascript:void(0)" @click="increate_quantity(item)"><i class="fal fa-plus color4f"></i></a>
                    </div>

                    <a class="product-delete" href="javascript:void(0)" @click="delete_product(item)"><i class="fal fa-times"></i></a>
                  </div>
                </div>
              </div>
            </div>
          </li>
        </ul>
      </div>
      <div class="col-5">
        <div class="shipping">
          <div class="d-flex justify-content-between align-items-center mb-3">
            <header class="shipping-title mb-0">Shipping Address</header>
            <a v-if="isLoggedIn" href="javascript:void(0)" @click="dialogVisible=true" class="font-12">Saved Addresses</a>
          </div>

          <div class="form-row">
            <div class="form-group col-md-6">
              <label for="country">Country or Region</label>
              <country-select id="country" v-model="shipping_address.country" :country="shipping_address.country" topCountry="US" className="form-control" :class="{'is-invalid': errors.country}"/>
            </div>
          </div>
          <div class="form-row">
            <div class="form-group col-md-6">
              <label for="first_name">First Name</label>
              <input type="text" class="form-control capitalize" id="first_name" name="first_name" v-model="shipping_address.first_name" :class="{'is-invalid': errors.first_name}">
            </div>
            <div class="form-group col-md-6">
              <label for="last_name">Last Name</label>
              <input type="text" class="form-control capitalize" id="last_name" name="last_name" v-model="shipping_address.last_name" :class="{'is-invalid': errors.last_name}">
            </div>
          </div>
          <div class="form-row">
            <div class="form-group col-md-6">
              <label for="first_name">Street Address</label>
<!--              <input type="text" class="form-control" id="street_address" name="street_address" v-model="shipping_address.street_address" :class="{'is-invalid': errors.street_address}">-->
              <place-autocomplete-field ref="input_address"
                      v-model="shipping_address.street_address" placeholder="" class="form-group" :class="{'is-invalid': errors.street_address}"
                      name="street_address" :api-key="googleMapApiKey"
                      v-place-autofill:street="shipping_address.street_address"
                      v-place-autofill:city="shipping_address.city"
                      v-place-autofill:state="shipping_address.state"
                      v-place-autofill:zipcode="shipping_address.zip_code"></place-autocomplete-field>
            </div>
            <div class="form-group col-md-6">
              <label for="last_name">Street Address 2 (Optional)</label>
              <input type="text" class="form-control" id="street_address_2" name="street_address_2" v-model="shipping_address.street_address_2" :class="{'is-invalid': errors.street_address_2}">
            </div>
          </div>
          <div class="form-row">
            <div class="form-group col-md-3">
              <label for="city">City</label>
              <input type="text" class="form-control" id="city" name="city" v-model="shipping_address.city" :class="{'is-invalid': errors.city}">
            </div>
            <div class="form-group col-md-6">
              <label for="state">State/Province/Region</label>
              <input type="text" class="form-control" id="state" name="state" v-model="shipping_address.state" :class="{'is-invalid': errors.state}">
            </div>
            <div class="form-group col-md-3">
              <label for="zip_code">Zip Code</label>
              <input type="text" class="form-control" id="zip_code" name="zip_code" v-model="shipping_address.zip_code" :class="{'is-invalid': errors.zip_code}">
            </div>
          </div>
          <div class="form-row">
            <div class="form-group col-md-6">
              <label for="email">Email</label>
              <input type="text" class="form-control" id="email" name="email" v-model="shipping_address.email" :class="{'is-invalid': errors.email}">
            </div>
            <div class="form-group col-md-6">
              <label for="confirm_email">Confirm Email</label>
              <input type="text" class="form-control" id="confirm_email" name="confirm_email" v-model="shipping_address.confirm_email" :class="{'is-invalid': errors.confirm_email}">
            </div>
          </div>
          <div class="form-row">
            <div class="form-group col-md-12">
              <label for="phone">Phone</label>
              <vue-phone-number-input ref="phone_input" id="phone" @update="onUpdate" v-model="shipping_address.phone" name="phone_number" :required="true" :class="{'is-invalid': errors.phone_number}"/>
            </div>
          </div>

          <button class="btn btn-primary btn-block white" @click="validShippingAddress()"><i v-if="valid_shipping" class="fas fa-check-circle"></i> Done</button>
        </div>
      </div>
      <div class="col-3">
        <div class="order-summary">
          <div class="d-flex justify-content-between mb-1">
            <span>Items ({{ cart_items.length }})</span><span>CA ${{ total_price | numFormat("0.00") }}</span>
          </div>
          <div class="d-flex justify-content-between mb-1">
            <span>Shipping</span><span>Free</span>
          </div>
          <div class="d-flex justify-content-between mb-1">
            <span>Discount</span><span>$0.00</span>
          </div>
          <hr style="margin: 10px 0;border-color: #4F4F4F"/>
          <div class="d-flex justify-content-between">
            <span>Order Total</span><span>${{ total_price | numFormat("0.00") }}</span>
          </div>
          <div class="mt-4">
            <button :disabled="loading || cart_items.length == 0" class="btn btn-primary btn-block white" type="button" @click="orderConfirm()">Confirm & Pay</button>
          </div>
        </div>
      </div>
    </div>

    <el-dialog
      title="Saved Addresses"
      :visible.sync="dialogVisible" width="75%">
      <saved-addresses :select-address="handleSelect"></saved-addresses>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">Close</el-button>
      </span>
    </el-dialog>

    <el-dialog
      title="Place Order"
      :visible.sync="dialogPaymentVisible" width="40%" :close-on-click-modal="false">
      <payment-request-button :client-secret="clientSecret" :publishable-key="stripePublishableKey"
        :total-price="total_price"
        :success-url="success_url"></payment-request-button>
    </el-dialog>
  </div>
</template>

<script>
import {mapState} from "vuex";
import axios from "axios";
import SavedAddresses from "@/components/shopper/account/SavedAddresses";
import { parsePhoneNumberFromString } from 'libphonenumber-js';
import PaymentRequestButton from "./PaymentRequestButton";

export default {
  name: "OrderOverview",
  components: {
    PaymentRequestButton,
    SavedAddresses,
  },
  props: {
    mediaUrl: {
      type: String,
      required: true
    },
    stripePublishableKey: {
      type: String,
      required: true
    },
    googleMapApiKey: {
      type: String,
      required: true
    }
  },
  data: function () {
    return {
      shipping_address: {
        country: "",
        first_name: "",
        last_name: "",
        street_address: "",
        street_address_2: "",
        city: "",
        state: "",
        zip_code: "",
        email: "",
        confirm_email: "",
        phone_number: "",
        phone: ""
      },
      sms_update: true,
      shopper_share_info: true,
      errors: {},
      valid_shipping: false,
      loading: false,
      dialogVisible: false,
      querySearch: "",
      dialogPaymentVisible: false,
      clientSecret: "",
      success_url: ""
    }
  },
  computed: {
    ...mapState([
      "cart_items", 'sizes', 'colors', "cartLoading", 'isLoggedIn'
    ]),
    mapSizes() {
      let sizes = {};
      this.sizes.forEach((size) => {
        sizes[size.value] = size.text
      })
      return sizes
    },
    mapColors() {
      let colors = {};
      this.colors.forEach((color) => {
        colors[color.value] = color.text
      })
      return colors
    },
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
    onUpdate(payload) {
      this.shipping_address.phone_number = payload.formatInternational || '';
    },
    handleSelect(address) {
      this.shipping_address = JSON.parse(JSON.stringify(address));
      this.shipping_address.confirm_email = address.email;
      let parsed = parsePhoneNumberFromString(address.phone_number);
      this.$refs.phone_input.countryCode = parsed.country;
      this.$refs.phone_input.phoneNumber = address.phone_number;
      this.dialogVisible = false;

    },
    productVariant(item) {
      let variants = [];
      if (item.color) {
        variants.push(this.mapColors[item.color] || item.color)
      }
      if (item.size) {
        variants.push(this.mapSizes[item.size] || item.size)
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
    },
    validShippingAddress() {
      let data = this.shipping_address, that = this;
      that.valid_shipping = false;
      axios.post("/api/order/shipping-address/valid/", data).then(() => {
        that.errors = {};
        that.valid_shipping = true;
      }).catch((err) => {
        if (err.response.data) {
          that.errors = err.response.data;
        }
      })
    },
    orderConfirm() {
      let data = this.shipping_address, that = this;
      if (confirm("Are you sure?")) {
        data.sms_update = that.sms_update
        data.shopper_share_info = that.shopper_share_info
        that.loading = true;
        axios.post("/api/order/confirm/", data).then((res) => {
          // let strip = window.Stripe(this.stripePublishableKey);
          // strip.redirectToCheckout({sessionId: res.data.session.id})
          that.clientSecret = res.data.clientSecret;
          that.dialogPaymentVisible = true;
          that.success_url = res.data.success_url;
          setTimeout(() => that.loading = false, 100);
          console.log(res);
        }).catch((err) => {
          that.loading = false;
          if (err.response.data) {
            that.errors = err.response.data;
          } else {
            alert("Something went wrong. Please try again!")
          }
        })
      }
    }
  }
}
</script>

<style lang="scss">
.order-overview {
  .form-check-inline {
    font-size: 12px;
  }
  .is-invalid .form-group-inner .form-control {
      border-color: #dc3545;
      padding-right: calc(1.5em + 0.75rem);
      background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='%23dc3545' viewBox='-2 -2 7 7'%3e%3cpath stroke='%23dc3545' d='M0 0l3 3m0-3L0 3'/%3e%3ccircle r='.5'/%3e%3ccircle cx='3' r='.5'/%3e%3ccircle cy='3' r='.5'/%3e%3ccircle cx='3' cy='3' r='.5'/%3e%3c/svg%3E");
      background-repeat: no-repeat;
      background-position: center right calc(0.375em + 0.1875rem);
      background-size: calc(0.75em + 0.375rem) calc(0.75em + 0.375rem);
  }
  .shipping-title {
    color: #4FC5E9;
    font-size: 20px;
    margin-bottom: 15px;
  }
  .order-summary {
    padding: 15px;
    background: #FFFCFF;
    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.12);
    border-radius: 5px;
    font-size: 14px;
  }
  .shipping {
    background: #FFFCFF;
    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.12);
    padding: 15px;
    font-size: 14px;
  }
  .is-invalid .input-tel__input, .is-invalid .form-control {
      border-color: #dc3545;
      padding-right: calc(1.5em + 0.75rem);
      background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='%23dc3545' viewBox='-2 -2 7 7'%3e%3cpath stroke='%23dc3545' d='M0 0l3 3m0-3L0 3'/%3e%3ccircle r='.5'/%3e%3ccircle cx='3' r='.5'/%3e%3ccircle cy='3' r='.5'/%3e%3ccircle cx='3' cy='3' r='.5'/%3e%3c/svg%3E");
      background-repeat: no-repeat;
      background-position: center right calc(0.375em + 0.1875rem);
      background-size: calc(0.75em + 0.375rem) calc(0.75em + 0.375rem);
  }
  .cart-items {
    list-style: none;
    padding-left: 0;
    li {
      background: #FFFCFF;
      box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.12);
      margin-bottom: 15px;
      padding: 15px;
      position: relative;

      .product-delete {
        position: absolute;
        position: absolute;
        top: 10px;
        right: 10px;
        i {
          font-size:16px
        }
      }

      .product-details {
        padding-left: 15px;
      }
      .item-img {
        flex: 0 0 120px;
        width: 120px;
        height: 120px;
        background-size: contain;
        background-position: center;
        background-repeat: no-repeat;
      }
      .form-control-sm {
        background: #4FC5E9;
        border-radius: 2px;
        font-size: 12px;
      }
      .product-title {
        font-size: 16px;
        overflow: hidden;
        white-space: nowrap;
        text-overflow: ellipsis;
        max-width: 180px;
        font-weight: bold;
      }
      .product-price {
        color: #4F4F4F;
        font-size: 14px;
      }
      .shop-name {
        font-size:12px;
      }
      .product-qty {
        font-size:12px;
        color: #4F4F4F;
      }
    }
  }
}
</style>
