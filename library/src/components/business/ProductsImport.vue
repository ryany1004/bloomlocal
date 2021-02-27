<template>
  <div v-loading.fullscreen="loading">
    <div class="d-flex justify-content-between align-items-center mb-3">
      <div class="form-check">
        <input type="checkbox" class="form-check-input" id="exampleCheck1" v-model="checked_all" :checked="checked_all" @change="handleCheckAll()">
        <label class="form-check-label font-14" for="exampleCheck1">Select all products</label>
      </div>
      <div>
        <button v-if="enableImport" class="btn btn-primary white font-14 mr-2" type="button" @click="showPreviewShopify()">Import</button>
        <button v-else class="btn btn-primary white font-14 mr-2" type="button" @click="showPop()">Import</button>
      </div>
    </div>

    <div class="row product-cards" v-if="products.length > 0">
      <div class="col-lg-2 col-md-3 col-6 mb-5" v-for="product in products" :key="product.id">
        <shopify-product-card v-loading="product.loading" element-loading-background="rgba(0, 0, 0, 0.8)" :product="product" :handle-click="handleClick"></shopify-product-card>
      </div>
    </div>
    <div v-else>
      {{ loading ? "Loading...": "No data" }}
    </div>

    <el-dialog title="Preview imported products" :close-on-click-modal="false" :visible.sync="visible" width="95%">
      <div class="row product-cards">
        <div class="col-lg-2 col-md-3 col-6 mb-5" v-for="product in selected_products" :key="product.id">
          <shopify-product-card v-loading="product.loading" element-loading-background="rgba(0, 0, 0, 0.8)" :product="product" :handle-click="handleClick"></shopify-product-card>
        </div>
      </div>
      <div slot="footer" class="dialog-footer">
        <el-button @click="visible = false">Cancel</el-button>
        <el-button type="primary" @click="importShopify()" :disabled="uploading">{{ uploading ? "Importing...": "Import" }}</el-button>
      </div>
    </el-dialog>

    <el-dialog
      title="Edit product"
      :visible.sync="dialogVisible"
      width="80%">
      <import-product-edit v-if="edit_product" :product.sync="edit_product"></import-product-edit>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="dialogVisible = false">Close</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import axios from "axios";
import pLimit from "p-limit";
import ImportProductEdit from "@/components/business/ImportProductEdit";

const limit = pLimit(2);

export default {
  name: "ProductsImport",
  components: {ImportProductEdit},
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
      dialogVisible: false,
      edit_product: null,
      uploading: false
    }
  },
  created() {
    let that = this;
    that.loading = true;
    that.$store.dispatch('get_categories')
    axios.get('/api/shopify/retrieve-products/').then(function (res) {
      that.products = res.data
      that.loading = false
      that.total = res.data.length;
    }).catch(function () {
      that.loading = false
      alert("Unable to load products!")
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

    handleCheckAll() {
      this.products.forEach((p) => {
          this.$set(p, 'checked', this.checked_all);
        })
    },
    async importShopify() {
      let requests = [], that = this;
      if (confirm("Are you sure?")) {
        that.uploading = true;
        this.selected_products.forEach(p => {
          requests.push(limit(() => new Promise((resolve, reject) => {
            that.$set(p, "loading", true);
            axios.post("/api/shopify/import-product/", p).then((res) => {
              that.$set(p, "loading", false);
              that.$set(p, "checked", false);
              resolve(res)
            }).catch((err) => {
              that.$set(p, "loading", false);
              reject(err)
            })
          })));
        });

        Promise.all(requests).then((res) => {
          console.log(res)
          that.visible = false;
          that.checked_all = false;
          that.uploading = false;
          setTimeout(() => {
            alert("The import was successful!")
          }, 1000)
        });
      }
    },
    handleClick(product) {
      this.edit_product = product;
      this.dialogVisible = true;
    }
  }
}
</script>

<style scoped>

</style>
