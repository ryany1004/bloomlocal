<template>
  <div v-loading="loading">
    <div class="row" v-if="order.shipping_address">
      <div class="col-6" v-if="order.shopper">
        <div class="shopper-info">
          <h3 class="font-16 ml-3">Personal Details</h3>
          <ul>
            <li>
              {{ order.shopper.first_name }} {{ order.shopper.last_name }}
            </li>
            <li>
              {{ order.shopper.email }}
            </li>
            <li v-if="order.shopper.phone_number">
              {{ order.shopper.phone_number }}
            </li>
          </ul>
        </div>
      </div>
      <div class="col-6">
        <div class="shopper-info">
          <h3 class="font-16 ml-3">Billing Address</h3>
          <ul>
            <li>
              {{ order.shipping_address.first_name }} {{ order.shipping_address.last_name }}
            </li>
            <li>
              {{ order.shipping_address.email }}
            </li>
            <li>
              {{ order.shipping_address.phone_number }}
            </li>
            <li>
              {{ get_full_address(order.shipping_address) }}
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "ShopperInfo",
  props: {
    mediaUrl: {
      type: String,
      default: ""
    },
    uuid: {
      type: String,
      required: true
    }
  },
  data: function () {
    return {
      loading: false,
      order: {}
    }
  },
  watch: {
    uuid: {
      immediate: true,
      handler(val) {
        this.get_order(val);
      }
    }
  },
  created() {

  },
  methods: {
    get_order(uuid) {
      let that = this;
      that.loading = true;
      axios.get(`/api/order/${uuid}/details/`).then((res) => {
        that.order = res.data;
        that.loading = false
      }).catch(() => {
        alert("Unable to load data");
      })
    },
    get_full_address(obj) {
      let address = [obj.street_address];
      if (obj.state) {
        address.push(obj.state)
      }
      if (obj.city) {
        address.push(obj.city)
      }
      if (obj.zip_code) {
        address.push(obj.zip_code)
      }
      return address.join(", ")
    }
  }
}
</script>

<style scoped lang="scss">
.shopper-info {
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.12);
  border-radius: 10px;
  padding-top: 20px;
  h3 {
    font-weight: bolder;
  }
  ul {
    padding-left: 0;
    list-style: none;
    li {
      border-bottom: 1px solid #f1f1f1;
      padding: 10px 20px;
    }
    li:last-child {
      border-bottom: none;
    }
  }
}
</style>
