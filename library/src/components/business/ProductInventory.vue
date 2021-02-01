<template>
  <div v-loading.fullscreen="loading" class="product-list">
    <div class="d-flex justify-content-between mb-4">
      <div>
        <h4>Inventory</h4>
      </div>
      <div class="d-flex align-items-center">
        <a href="/business/product/upload/"><i class="fas fa-plus fa-1x"></i></a>
        <a href="/business/google-merchant/upload/" class="ml-3" title="Upload your products to Google Merchant"><i class="fas fa-upload"></i></a>
        <div class="dropdown">
          <button class="btn btn-primary dropdown-toggle btn-sm white ml-3" type="button" id="dropdownImportButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
            Import
          </button>
          <div class="dropdown-menu" aria-labelledby="dropdownImportButton">
            <a class="dropdown-item font-14" href="/business/products/shopify/import/">Shopify</a>
            <a class="dropdown-item font-14" href="/business/products/file/import/">CSV or Google Spreadsheet</a>
          </div>
        </div>
        <div class="dropdown mx-4">
          <button class="btn btn-light btn-sm dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
            Sort by {{ sort_by_text }}
          </button>
          <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
            <a class="dropdown-item" href="javascript:void(0)" @click="order_by='all'">View all</a>
            <a class="dropdown-item" href="javascript:void(0)" @click="order_by='title'">Name</a>
            <a class="dropdown-item" href="javascript:void(0)" @click="order_by='price'">Price</a>
          </div>
        </div>
        <div class="btn-group btn-group-toggle btn-group-sm" data-toggle="buttons" style="height: 31px">
          <label class="btn btn-primary" :class="{active: view_mode == 'storefronnt'}" @click="changeViewMode('storefront')">
            <input type="radio" name="options" id="option1" value="storefront"> <i class="fas fa-grip-horizontal"></i>
          </label>
          <label class="btn btn-primary" :class="{active: view_mode == 'inventory'}" @click="changeViewMode('inventory')">
            <input type="radio" name="options" id="option2" value="inventory"> <i class="fas fa-list-alt"></i>
          </label>
        </div>
      </div>
    </div>

    <el-table
      :data="pagingTableData"
      class="product-list"
      style="width: 100%">
      <el-table-column
        prop="title"
        label="My Products"
        width="180">
      </el-table-column>
      <el-table-column
        prop="thumbnail"
        label="Image"
        width="70">
        <template slot-scope="scope">
          <div class="product-thumbnail" :style="{backgroundImage: `url('${mediaUrl}${scope.row.thumbnail}')`}"></div>
        </template>
      </el-table-column>
      <el-table-column
        prop="price"
        width="100"
        label="Price">
        <template slot-scope="scope">
          <div>
            ${{scope.row.price}}
            <el-popover
              placement="bottom"
              title="Edit price"
              width="200"
              trigger="manual"
              v-model="scope.row.price_visible">
              <div>
                <ValidationProvider rules="positive" v-slot="{ errors }">
                <input type="number" min="0" v-model="scope.row.edit_price" class="form-control" :class="{'is-invalid': errors.length > 0 || (errs[scope.row.id] && errs[scope.row.id].price)}"/>
                </ValidationProvider>
                <div class="mt-3" style="text-align: right;">
                  <el-button size="mini" type="text" @click="scope.row.price_visible = false">cancel</el-button>
                  <el-button type="primary" size="mini" @click="saveAttribute(scope.row, 'price')">confirm</el-button>
                </div>
              </div>
              <a slot="reference" class="icon-edit" href="javascript:void(0)" @click="scope.row.price_visible=true;scope.row.edit_price=scope.row.price"><i class="fas fa-pencil-alt"></i></a>
            </el-popover>
          </div>
        </template>
      </el-table-column>
      <el-table-column
        label="Quantity Sold">
        <template slot-scope="scope">
          {{scope.row.price * 0}}
        </template>
      </el-table-column>
      <el-table-column
        label="Stock">
        <template slot-scope="scope">
          <div>
            {{scope.row.stock}}

            <el-popover
              placement="bottom"
              title="Edit stock"
              width="200"
              trigger="manual"
              v-model="scope.row.stock_visible">
              <div>
                <ValidationProvider rules="positive" v-slot="{ errors }">
                <input type="number" min="0" v-model="scope.row.edit_stock" class="form-control" :class="{'is-invalid': errors.length > 0 || (errs[scope.row.id] && errs[scope.row.id].stock)}"/>
                </ValidationProvider>
                <div class="mt-3" style="text-align: right;">
                  <el-button size="mini" type="text" @click="scope.row.stock_visible = false">cancel</el-button>
                  <el-button type="primary" size="mini" @click="saveAttribute(scope.row, 'stock')">confirm</el-button>
                </div>
              </div>
              <a slot="reference" class="icon-edit" href="javascript:void(0)" @click="scope.row.stock_visible=true;scope.row.edit_stock=scope.row.stock"><i class="fas fa-pencil-alt"></i></a>
            </el-popover>
          </div>
        </template>
      </el-table-column>
      <el-table-column
        label="Date Added">
        <template slot-scope="scope">
          {{scope.row.created_at | moment('MM/DD/YYYY') }}
        </template>
      </el-table-column>
      <el-table-column
        label="Status"
        width="90">
        <template slot-scope="scope">
          {{scope.row.status == 0 ? 'Active': "Disabled"}}
        </template>
      </el-table-column>
      <el-table-column
        label="Category">
        <template slot-scope="scope">
          {{scope.row.category_names.join(", ")}}
        </template>
      </el-table-column>
      <el-table-column
        label="Action"
        width="80">
        <template slot-scope="scope">
          <div class="d-flex justify-content-around">
            <a :href="`/business/product/${scope.row.uuid}/update/`"><i class="fas fa-pencil-alt"></i></a>
            <a href="javascript:void(0)" @click="toggleActive(scope.row)"><i class="fas" :class="{'fa-eye': scope.row.status == 1, 'fa-eye-slash': scope.row.status == 0}"></i></a>
            <a href="javascript:void(0)" @click="archiveProduct(scope.row)"><i class="fas fa-archive"></i></a>
          </div>
        </template>
      </el-table-column>
    </el-table>
    <div class="d-flex justify-content-center my-3">
      <el-pagination
        background
        layout="prev, pager, next"
        :current-page="current_page"
        :page-size="page_size"
        :total="total"
        @current-change="change_page">
      </el-pagination>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import _ from "lodash";
import { ValidationProvider, extend } from 'vee-validate';

extend('positive', value => {
  return value >= 0;
});

export default {
  name: "ProductInventory",
  props: {
    mediaUrl: {
      type: String,
      default: ""
    },
    viewMode: {
      type: String,
      default: 'inventory'
    }
  },
  data: function () {
    return {
      view_mode: this.viewMode,
      products: [],
      loading: false,
      order_by: 'all',
      errs: {},
      page_size: 7,
      current_page: 1,
      total: 0
    }
  },
  components: {
    ValidationProvider
  },
  created() {
    let that = this;
    that.view_mode = this.viewMode;
    that.loading = true;
    axios.get('/api/shop/products/').then(function (res) {
      that.products = res.data
      that.loading = false
      that.total = res.data.length;
    }).catch(function () {
      that.loading = false
    })
  },
  watch: {
    viewMode: function (val) {
      this.view_mode = val;
    }
  },
  computed: {
    tableData() {
      if (this.order_by == 'title') {
        return _.orderBy(this.products, this.order_by)
      } else if (this.order_by == 'price') {
        return _.orderBy(this.products, this.order_by);
      } else {
        return this.products
      }
    },
    pagingTableData() {
      let products = [];
      let size_start = (this.current_page - 1) * this.page_size;
      products = this.tableData.slice(size_start, size_start + this.page_size);
      return products
    },
    sort_by_text() {
      let text = "View All";
      if (this.order_by == "title") {
        text = "Name"
      } else if (this.order_by == 'price') {
        text = "Price"
      }
      return text
    },
  },
  methods: {
    changeViewMode(mode) {
      this.$emit("changeViewMode", mode);
    },
    saveAttribute(product, attr) {
      let data = {}, that = this;
      data[attr] = product[`edit_${attr}`];
      this.$set(this.errs, product.id, {});
      // eslint-disable-next-line no-debugger
      debugger
      axios.patch(`/api/shop/product/${product.uuid}/`, data).then(function (res) {
        product[attr] = res.data[attr];
        product[`${attr}_visible`] = false;
      }).catch(function (err) {
        that.errs[product.id] = err.response.data;
      })
    },
    toggleActive(product) {
      let msg = `Do you want to ${product.status == 0 ? "disable" : "enable"} this product`;
      if (confirm(msg)) {
        let data = {
          status: product.status == 0 ? 1 : 0
        }
        axios.patch(`/api/shop/product/${product.uuid}/`, data).then(function (res) {
          product.status = res.data.status;
        }).catch(function (err) {
          console.log(err);
        })
      }
    },
    archiveProduct(product) {
      let that = this;
      if (confirm("Do you want to archive this product?")) {
        axios.patch(`/api/shop/product/${product.uuid}/`, {archived: true}).then(function (res) {
          let index = _.findIndex(that.products, (p) => p.uuid == res.data.uuid);
          if (index != -1) {
            that.$delete(that.products, index);
            that.total = that.products.length;
          }
        })
      }
    },
    change_page(page) {
       this.current_page = page;
    }
  }
}
</script>

<style lang="scss">
  .product-list {
    .btn-light {
      border-color: #bdbdbd;
    }
    .btn-group {
      .btn-primary {
        background-color: #fffdff;
        i {
          color: #e1e1e1;
        }
      }
      .btn-primary:hover, .btn-primary.active {
        background-color: #4fc5e9;
        i {
          color: #fff;
        }
      }
    }
    .product-thumbnail {
      width: 30px;
      height: 30px;
      background-position: center;
      background-size: contain;
      border-radius: 5px;
    }
    .icon-edit {
      text-align: right;
    }
    .el-table thead tr th {
      background-color: #ecf5fc !important;
    }
  }

</style>
