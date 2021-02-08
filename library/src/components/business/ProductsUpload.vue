<template>
  <div v-loading.fullscreen="loading">
    <div class="d-flex justify-content-between align-items-center mb-3">
      <div class="form-check">
        <input type="checkbox" class="form-check-input" id="exampleCheck1" v-model="checked_all" :checked="checked_all" @change="handleCheckAll()">
        <label class="form-check-label font-14" for="exampleCheck1">Select all products</label>
      </div>
      <div>
        <button class="btn btn-primary white font-14" type="button" @click="showPreviewGMC()">Upload to Google Merchant</button>
      </div>
    </div>

    <div class="row product-cards">
      <div class="col-lg-3 col-md-4 col-6 mb-5" v-for="product in products" :key="product.id">
        <business-product-card :product="product" :media-url="mediaUrl" :selectable="true"></business-product-card>
      </div>
    </div>

    <el-dialog title="Preview imported products to Google Merchant" :visible.sync="visibleDlg" width="95%">
      <div class="row product-cards">
        <div class="col-lg-3 col-md-4 col-6 mb-5" v-for="product in selected_products" :key="product.id">
          <business-product-card :product="product" :media-url="mediaUrl"></business-product-card>
        </div>
      </div>
      <div slot="footer" class="dialog-footer">
        <el-button @click="visibleDlg = false">Cancel</el-button>
        <el-button type="primary" @click="importGoogleMerchant()">Upload</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "ProductsUpload",
  props: {
    mediaUrl: {
      type: String,
      default: ""
    },
    enableImport: {
      type: Boolean,
      default: false
    }
  },
  data: function () {
    return {
      products: [],
      loading: false,
      checked_all: false,
      visible: false,
      visibleDlg: false
    }
  },
  created() {
    let that = this;
    that.loading = true;
    axios.get('/api/shop/products/').then(function (res) {
      that.products = res.data
      that.loading = false
      that.total = res.data.length;
    }).catch(function () {
      that.loading = false
    })
  },
  computed: {
    selected_products() {
      return this.products.filter((p) => p.checked)
    }
  },
  methods: {
    showPop() {
      if (confirm("You didn't connect to Shopify. Do you want to connect now?")) {
        window.location.href = '/users/shopify-integration/';
      }
    },
    showPreviewShopify() {
      if (this.selected_products.length > 0) {
        this.visible = true;
      } else {
        alert("Please select at least one product");
      }
    },
    showPreviewGMC() {
      if (this.selected_products.length > 0) {
        this.visibleDlg = true;
      } else {
        alert("Please select at least one product");
      }
    },
    handleCheckAll() {
      this.products.forEach((p) => {
          this.$set(p, 'checked', this.checked_all);
        })
    },
    importShopify() {
      let product_ids = []
      this.selected_products.forEach(p => {
        if (p.checked) {
          product_ids.push(p.id);
        }
      })
      let that = this;
      that.loading = true;
      if (product_ids.length > 0) {
        axios.post("/business/google-merchant/upload/", {product_ids: product_ids}).then(() => {
          that.loading = false;
          that.visible = false;
          setTimeout(() => {
            alert("Selected product(s) successfully posted to google shopping")
          }, 1000)
        }).catch(() => {
          that.loading = false;
        })
      }
    },
    importGoogleMerchant() {
      let product_ids = []
      if (confirm("Are you sure?")) {
        this.selected_products.forEach(p => {
          if (p.checked) {
            product_ids.push(p.id);
          }
        })
        let that = this;
        that.loading = true;
        if (product_ids.length > 0) {
          axios.put("/business/google-merchant/upload/", {product_ids: product_ids}).then(() => {
            that.loading = false;
            that.visibleDlg = false;
            alert("Selected product(s) successfully posted to google shopping")
          }).catch(() => {
            that.loading = false;
          })
        }
      }
    }
  }
}
</script>

<style scoped>

</style>
