<template>
  <div class="box-import">
    <div class="step_3">
      <h3>
          Import your products from <br />
          Shopify, WooCommerce Or Big Commerce
      </h3>
      <h4>Select Your Platform</h4>
      <div class="clearfix"></div>
      <div class="d-flex align-items-center justify-content-center">
          <div class="p-2 bd-highlight col-example box_div" :class="{active: selected_platform == 'shopify'}">
              <a href="javascript:void(0)" @click="selectPlatform('shopify')"><img src="../../assets/images/shopify.png" alt="" /></a>
          </div>
          <div class="p-2 bd-highlight col-example box_div" :class="{active: selected_platform == 'big'}">
              <a href="javascript:void(0)" @click="selectPlatform('big')"><img src="../../assets/images/bigcommorce.png" alt="" /></a>
          </div>
          <div class="p-2 bd-highlight col-example box_div" :class="{active: selected_platform == 'woo'}">
              <a href="javascript:void(0)" @click="selectPlatform('woo')"><img src="../../assets/images/woocommerce.png" alt="" /></a>
          </div>
          <div class="p-2 bd-highlight col-example box_div" :class="{active: selected_platform == 'csv'}">
              <a href="javascript:void(0)" @click="selectPlatform('csv')"><img src="../../assets/images/csv.png" alt="" /></a>
          </div>
      </div>
    </div>
    <div class="row">
      <div class="col-md-12 mb-3">
          <ul class="list-inline next_btn_div">
              <li><button type="button" :disabled="selected_platform == 'woo' || selected_platform == 'big'" class="default-btn import_btn" v-on:click="showDialog()">Import Now</button></li>
          </ul>
      </div>
      <div class="col-md-12">
          <ul class="list-inline next_btn_div">
              <li><a href="#" class="default-btn next-step skip_btn" v-on:click="nextStep">Skip for now and create my e-commerce store</a></li>
          </ul>
      </div>
    </div>

    <el-dialog
      title="Shopify Import"
      :visible.sync="dialog1Visible"
      :append-to-body="true" :close-on-click-modal="false">
      <form @submit="handleShopifySubmit" method="post">
        <div class="form-group">
          <label for="exampleFormControlInput1">Your Shopify URL</label>
          <input type="url" class="form-control" v-model="shopify_url" required id="exampleFormControlInput1" placeholder="https://myshop.myshopify.com">
        </div>
        <input type="submit" style="display: none" ref="shopify"/>
      </form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialog1Visible = false">Cancel</el-button>
        <el-button type="primary" @click="shopifySave()">Save</el-button>
      </span>
    </el-dialog>

    <el-dialog
      title="Wordpress Import"
      :visible.sync="dialog2Visible"
      :append-to-body="true" :close-on-click-modal="false">
      <form @submit="handleWooCommerceSubmit">
        <div class="form-group">
          <label for="exampleFormControlInput2">Your Shop URL</label>
          <input type="url" class="form-control" v-model="woo_url" required id="exampleFormControlInput2" placeholder="https://myshop.com">
        </div>
        <input type="submit" style="display: none" ref="woo"/>
      </form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialog2visible = false">Cancel</el-button>
        <el-button type="primary" @click="wooCommerceSave()">Save</el-button>
      </span>
    </el-dialog>

    <csv-import-modal v-model="dialog3Visible" :next-step="nextStep"></csv-import-modal>
  </div>
</template>

<script>
import axios from "axios";
import CsvImportModal from "@/components/signup/CsvImportModal";

export default {
  name: "ImportData",
  components: {CsvImportModal},
  props: {
    nextStep: {
      type: Function,
      required: true
    }
  },
  data() {
    return {
      dialog1Visible: false,
      dialog2Visible: false,
      dialog3Visible: false,
      shopify_url: "",
      woo_url: "",
      selected_platform: 'shopify',
      csv_file: null,
      products: []
    }
  },
  methods: {
    showDialog() {
      if (this.selected_platform == 'shopify') {
        this.dialog1Visible = true;
      } else if (this.selected_platform == 'csv') {
        this.dialog3Visible = true;
      }
    },
    selectPlatform(platform) {
      this.selected_platform = platform;
      let that = this;
      if (platform == 'woo' || platform == "big") {
        setTimeout(() => {
          that.comingSoon()
        }, 1000)
      }
    },
    shopifySave() {
      this.$refs.shopify.click();
    },
    handleShopifySubmit(e) {
      e.preventDefault();
      let that = this;
      axios.post("/api/business/shopify-url/update/", {shop_url: this.shopify_url}).then(() => {
        that.dialog1Visible = false;
        setTimeout(() => {
          that.nextStep();
        }, 100)
      })
    },
    wooCommerceSave() {
      this.$refs.woo.click();
    },
    handleWooCommerceSubmit(e) {
      e.preventDefault();
      let that = this;
      axios.post("/api/business/woo-commerce-url/update/", {shop_url: this.woo_url}).then(() => {
        that.dialog2Visible = false;
        setTimeout(() => {
          that.nextStep();
        }, 100)
      })
    },
    comingSoon() {
      alert("Coming soon!");
    },
  }
}
</script>

<style lang="scss">
.box-import {
  .box_div.active {
    border: 2px solid green;
  }
}
</style>
