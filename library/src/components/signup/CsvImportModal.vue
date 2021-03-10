<template>
  <div>
    <el-dialog
      title="CSV Import"
      :visible.sync="dialogVisible" :close-on-click-modal="false"
      :append-to-body="true" width="90%">
        <div v-loading="loading">
          <div class="d-flex align-items-center mb-4">
            <div class="custom-file" style="width: auto">
              <input type="file" class="custom-file-input" id="customFile" @change="loadFile" accept=".csv">
              <label class="custom-file-label" for="customFile">Choose CSV file</label>
            </div>
            <a href="/static/files/product_template.csv" class="font-12 ml-3" download><i class="fas fa-file-csv"></i> Sample CSV template</a>
          </div>

          <div v-if="products.length > 0">
            <div class="form-check">
              <input type="checkbox" class="form-check-input" id="exampleCheck1" v-model="checked_all" :checked="checked_all" @change="handleCheckAll()">
              <label class="form-check-label font-14" for="exampleCheck1">Select all products</label>
            </div>
            <div class="row product-cards mt-3">
              <div class="col-lg-2 col-md-3 col-6 mb-5" v-for="product in products" :key="product.id">
                <shopify-product-card v-loading="product.loading" element-loading-background="rgba(0, 0, 0, 0.8)" :product="product"></shopify-product-card>
              </div>
            </div>
          </div>
        </div>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">Cancel</el-button>
        <el-button type="primary" @click="importData()" :disabled="selected_products.length == 0">Import</el-button>
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
  name: "CsvImportModal",
  props: {
    value: {
      default: false,
      type: Boolean
    },
    nextStep: {
      type: Function,
      required: true
    }
  },
  data() {
    return {
      products: [],
      loading: false,
      checked_all: false
    }
  },
  watch: {

  },
  computed: {
    selected_products() {
      return this.products.filter((p) => p.checked)
    },
    dialogVisible: {
      get() {
        return this.value;
      },
      set(val) {
        this.products = [];
        this.$emit('input', val);
      }
    }
  },
  methods: {
    handleCheckAll() {
      this.products.forEach((p) => {
          this.$set(p, 'checked', this.checked_all);
        })
    },
    loadFile(e) {
      let that = this;
      if (!e.target.files[0].name.endsWith(".csv")) {
        alert("Please choose csv file");
        return;
      }
      that.loading = true;
      let formData = new FormData();
      formData.append("file", e.target.files[0]);
      $.ajax({
        url: "/business/products/file/import/",
        type: 'POST',
        data: formData,
        success: function (data) {
          that.products = data;
          that.loading = false;
        },
        error: function (result) {
          that.loading = false;
          console.log(result);
          setTimeout(() => {
            alert("Unable load your CSV file. Please make sure your file is the correct format.");
          }, 1000);
        },
        cache: false,
        processData: false,
        contentType: false,
      });
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
          that.checked_all = false;
          that.uploading = false;
          that.dialogVisible = false;
          setTimeout(() => {
            alert("The import was successful!");
            setTimeout(() => {
              that.nextStep();
            }, 500);
          }, 1000)
        }).catch(() => {
          that.uploading = false;
          setTimeout(() => {
            alert("Something went wrong!")
          }, 1000)
        });
      }
    },
  }
}
</script>

<style scoped>

</style>
