<template>
  <div v-loading.fullscreen="loading" class="my-storefront">
    <div class="d-flex justify-content-between mb-4">
      <div>
        <h4>Inventory</h4>
      </div>
      <div class="d-flex align-items-center">
        <a href="/business/product/upload/"><i class="fas fa-plus fa-1x"></i></a>
        <div class="dropdown mx-4">
          <button class="btn btn-secondary btn-sm dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
            Sort by View All
          </button>
          <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
            <a class="dropdown-item" href="#">View all</a>
            <a class="dropdown-item" href="#">Name</a>
            <a class="dropdown-item" href="#">Price</a>
          </div>
        </div>
        <div class="btn-group btn-group-toggle btn-group-sm" data-toggle="buttons" style="height: 31px">
          <label class="btn btn-secondary" :class="{active: view_mode == 'grid'}" @click="view_mode = 'grid'">
            <input type="radio" name="options" id="option1" value="grid" v-model="view_mode"> <i class="fas fa-grip-horizontal"></i>
          </label>
          <label class="btn btn-secondary" :class="{active: view_mode == 'list'}" @click="view_mode = 'list'">
            <input type="radio" name="options" id="option2" value="list" v-model="view_mode"> <i class="fas fa-list-alt"></i>
          </label>
        </div>
      </div>
    </div>
    <el-table v-if="view_mode == 'list'"
      :data="tableData"
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
        width="70"
        label="Price">
        <template slot-scope="scope">
          ${{scope.row.price}}
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
          {{scope.row.stock}}
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
        width="80">
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
            <a :href="`/business/product/${scope.row.uuid}/update/`" target="_blank"><i class="fas fa-edit"></i></a>
            <a href="javascript:void(0)" target="_blank"><i class="fas fa-eye-slash"></i></a>
            <a href="javascript:void(0)" target="_blank"><i class="fas fa-archive"></i></a>
          </div>
        </template>
      </el-table-column>
    </el-table>
    <div v-else>

    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Storefront",
  props: {
    mediaUrl: {
      type: String,
      default: ""
    },
  },
  data: function () {
    return {
      products: [],
      loading: false,
      view_mode: 'list'
    }
  },
  created() {
    let that = this;
    that.loading = true;
    axios.get('/api/shop/products/').then(function (res) {
      that.products = res.data
      that.loading = false
    }).catch(function () {
      that.loading = false
    })
  },
  computed: {
    tableData() {
      return this.products;
    }
  },
  methods: {

  }
}
</script>

<style lang="scss">
.my-storefront {
  .product-thumbnail {
    width: 30px;
    height: 30px;
    background-position: center;
    background-size: cover;
    border-radius: 5px;
  }
}
</style>
