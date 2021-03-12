<template>
  <div class="business products" v-loading="loading">
<!--    <product-inventory v-if="view_mode == 'inventory'" :view-mode="view_mode" :media-url="mediaUrl" @changeViewMode="changeViewMode"></product-inventory>-->
<!--    <my-storefront v-if="view_mode == 'storefront'" :view-mode="view_mode" :media-url="mediaUrl" @changeViewMode="changeViewMode"></my-storefront>-->
    <h3 class="business-title">Store Products</h3>

    <div class="d-flex justify-content-between align-items-center">
      <div class="form-row align-items-center my-3 ml-2">
        <div class="col-auto my-1">
          <div class="form-check form-check-inline mr-0">
            <input class="form-check-input" type="checkbox" id="inlineCheckbox1" value="option1">
          </div>
        </div>
        <div class="col-auto my-1">
          <select class="custom-select mr-sm-2" id="inlineFormCustomSelect">
            <option disabled selected>Manage Products</option>
          </select>
        </div>
        <div class="col-auto my-1">
          <div class="btn-group btn-group-toggle btn-group-sm" data-toggle="buttons" style="height: 31px">
            <label class="btn btn-light" :class="{active: view_mode == 'cards'}" @click="changeViewMode('cards')">
              <input type="radio" name="options" id="option1" value="cards"> <i class="fas fa-grip-horizontal"></i>
            </label>
            <label class="btn btn-light" :class="{active: view_mode == 'table'}" @click="changeViewMode('table')">
              <input type="radio" name="options" id="option2" value="table"> <i class="fas fa-list-alt"></i>
            </label>
          </div>
        </div>
      </div>

      <div>
        <a href="/business/product/upload/" class="btn btn-primary white"><i class="fas fa-plus-circle"></i> Add New Product</a>
      </div>
    </div>

    <card-products v-if="view_mode == 'cards'" :media-url="mediaUrl" :products="products"></card-products>
    <table-products v-if="view_mode == 'table'" :media-url="mediaUrl" :products="products"></table-products>
  </div>
</template>

<script>
import CardProducts from "@/components/business/products/CardProducts";
import axios from "axios";
import TableProducts from "@/components/business/products/TableProducts";


export default {
  name: "Products",
  components: {TableProducts, CardProducts},
  props: {
    mediaUrl: {
      type: String,
      default: ""
    },
  },
  data: function () {
    return {
      view_mode: 'table',
      products: [],
      loading: false
    }
  },
  created() {
    let view_mode = localStorage.getItem('view_mode');
    if (['table', 'cards'].indexOf(view_mode) != -1) {
      this.view_mode = view_mode;
    } else {
      this.view_mode = 'table';
    }
    this.get_products();
  },
  methods: {
    changeViewMode(mode) {
      this.view_mode = mode;
      localStorage.setItem('view_mode', mode);
    },
    get_products() {
      let that = this;
      that.loading = true;
      axios.get('/api/shop/products/').then(function (res) {
        that.products = res.data
        that.loading = false
        that.total = res.data.length;
      }).catch(function () {
        that.loading = false
      })
    }
  }
}
</script>

<style lang="scss">
</style>
