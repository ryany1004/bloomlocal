<template>
  <div class="product-import" v-loading.fullscreen="loading">
    <div v-if="!uploaded">
      <div>
        <h3 class="text-center font-16 mb-4">Import products from CSV or Google Spreadsheet</h3>
        <div class="d-flex justify-content-center align-items-start file-import">
          <div class="d-flex flex-column justify-content-center align-items-center">
            <el-upload
              class="csv-import d-flex"
              drag
              :show-file-list="false"
              :http-request="handleCSVUpload"
              :before-upload="beforeUpload">
              <i class="el-icon-upload"></i>
              <div class="el-upload__text">Upload CSV file</div>
            </el-upload>
            <a href="/static/files/product_template.csv" class="font-12 mt-3" download><i class="fas fa-file-csv"></i> Sample CSV template</a>
          </div>
          <div class="d-flex flex-column justify-content-center align-items-center ml-3" @click="dialogURLVisible = true">
            <div class="google-sheet d-flex flex-column justify-content-center align-items-center">
              <i class="fas fa-file-spreadsheet fa-3x" style="color: #C0C4CC"></i>
              <p class="gs-text">From Google Spreadsheet</p>
            </div>
            <a href="https://docs.google.com/spreadsheets/d/1zbYx3OjDVaJMxJlFnUb80ClhAU7oUV_Z_xqG2IWplys/edit?usp=sharing"
               target="_blank" class="font-12 mt-3"><i class="fas fa-file-spreadsheet"></i> Google Spreadsheet template</a>
          </div>
        </div>
      </div>
    </div>
    <div v-else>
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

      <div class="row product-cards">
        <div class="col-lg-2 col-md-3 col-6 mb-5" v-for="product in products" :key="product.id">
          <shopify-product-card v-loading="product.loading" element-loading-background="rgba(0, 0, 0, 0.8)" :product="product" :handle-click="handleClick"></shopify-product-card>
        </div>
      </div>

      <el-dialog title="Preview imported products to Shopify" :close-on-click-modal="false" :visible.sync="visible" width="95%">
        <div class="row product-cards">
          <div class="col-lg-2 col-md-3 col-6 mb-5" v-for="product in selected_products" :key="product.id">
            <shopify-product-card v-loading="product.loading" element-loading-background="rgba(0, 0, 0, 0.8)"
                                  :product="product" :handle-click="handleClick"></shopify-product-card>
          </div>
        </div>
        <div slot="footer" class="dialog-footer">
          <el-button @click="visible = false">Cancel</el-button>
          <el-button type="primary" @click="importData()" :disabled="uploading">{{ uploading ? "Importing...": "Import" }}</el-button>
        </div>
      </el-dialog>
    </div>

    <el-dialog
      title="Edit product"
      :visible.sync="dialogVisible"
      width="80%">
      <shopify-product-edit v-if="edit_product" :product.sync="edit_product"></shopify-product-edit>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="dialogVisible = false">Close</el-button>
      </span>
    </el-dialog>

    <el-dialog
      title="Google Spreadsheet URL"
      :visible.sync="dialogURLVisible"
      width="50%">
      <p>Click <a href="https://docs.google.com/spreadsheets/d/1zbYx3OjDVaJMxJlFnUb80ClhAU7oUV_Z_xqG2IWplys/edit?usp=sharing" target="_blank">Google Spreadsheet template</a> to see an example of the format required.</p>
      <div class="mb-3">
        <label for="file_url" class="form-label">Google Sheet URL:</label>
        <input v-model="file_url" type="url" class="form-control" id="file_url" placeholder="https://docs.google.com/spreadsheets/d/1zbYx3OjDVaJMxJlFnUb80ClhAU7oUV_Z_xqG2IWplys/">
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="getPermissionURL()" :disabled="submitting">Submit</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import axios from "axios";
import pLimit from "p-limit";
import $ from "jquery";

const limit = pLimit(2);

export default {
  name: "ProductsFileImport",
  props: {
    mediaUrl: {
      type: String,
      default: ""
    },
    enableImport: {
      type: Boolean,
      default: false
    },
    hasItems: {
      type:Boolean,
      default: false
    },
    items: {
      type: Object,
      default: () => []
    }
  },
  data: function () {
    return {
      products: [],
      loading: false,
      checked_all: false,
      visible: false,
      dialogURLVisible: false,
      dialogVisible: false,
      edit_product: null,
      uploading: false,
      uploaded: false,
      file_url: '',
      submitting: false
    }
  },
  created() {
    if (this.hasItems) {
      this.products = this.items;
      this.uploaded = true;
    }
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
    async importData() {
      let requests = [], that = this;
      if (confirm("Are you sure?")) {
        that.uploading = true;
        this.selected_products.forEach(p => {
          requests.push(limit(() => new Promise((resolve, reject) => {
            that.$set(p, "loading", true);
            axios.post("/api/file/import-product/", p).then((res) => {
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
        }).catch(() => {
          that.uploading = false;
          setTimeout(() => {
            alert("Something went wrong!")
          }, 1000)
        });
      }
    },
    handleClick(product) {
      this.edit_product = product;
      this.dialogVisible = true;
    },
    beforeUpload: function (file) {
      const isCSV = file.name.toLowerCase().endsWith(".csv");
      const isLt1M = file.size / 1024 / 1024 <= 1;

      if (!isCSV) {
        this.$message.error('File must be CSV format!');
      }
      if (!isLt1M) {
        this.$message.error('File size can not exceed 1MB!');
      }
      return isCSV && isLt1M;
    },
    handleCSVUpload(data) {
      let that = this;
      that.loading = true;
      let formData = new FormData();
      formData.append("file", data.file);
      $.ajax({
            url: "/business/products/file/import/",
            type: 'POST',
            data: formData,
            success: function (data) {
              that.products = data;
              that.loading = false;
              that.uploaded = true;
            },
            error: function (result) {
                that.loading = false;
                console.log(result);
                setTimeout(() => {
                  alert("Error while uploading.");
                }, 1000);
            },
            cache: false,
            processData: false,
            contentType: false,
        });
    },
    getPermissionURL() {
      if (this.file_url.startsWith("https://docs.google.com/spreadsheets/d/")) {
        let that = this;
        that.submitting = true;
        axios.post("/api/spreadsheet/authorization-url/", {file_url: this.file_url}).then(res => {
          that.submitting = false
          location.href = res.data.auth_url;
        }).catch((err) => {
          that.submitting = false;
          console.log(err);
        })
      } else {
        alert("Spreadsheet URL is wrong");
      }
    }
  }
}
</script>

<style lang="scss">
.product-import {
  .file-import {
    .csv-import {
      .el-upload-dragger {
        width: 260px;
      }
    }
    .google-sheet {
      width: 260px;
      height: 180px;
      background-color: #fff;
      border: 1px dashed #d9d9d9;
      border-radius: 6px;
      box-sizing: border-box;
      text-align: center;
      position: relative;
      overflow: hidden;
      cursor: pointer;
      .gs-text {
        color: #606266;
        font-size: 14px;
        margin-top: 20px;
      }
    }
  }
}
</style>
