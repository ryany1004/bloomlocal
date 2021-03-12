<template>
  <div class="table-products">
    <el-table
      :data="pagingTableData"
      stripe
      class="product-list"
      style="width: 100%">
      <el-table-column
        type="selection"
        width="43">
      </el-table-column>
      <el-table-column
        width="70">
        <template slot-scope="scope">
          <div class="product-thumbnail" :style="{backgroundImage: `url('${mediaUrl}${scope.row.thumbnail}')`}"></div>
        </template>
      </el-table-column>
      <el-table-column
        prop="title"
        label="PRODUCT">
      </el-table-column>
      <el-table-column
        prop="price"
        width="100"
        label="PRICE">

      </el-table-column>
      <el-table-column
        label="QTY SOLD"
        width="80">
        <template slot-scope="scope">
          {{scope.row.price * 0}}
        </template>
      </el-table-column>
      <el-table-column
        prop="stock"
        width="80"
        label="STOCK">
      </el-table-column>
<!--      <el-table-column-->
<!--        label="Date Added">-->
<!--        <template slot-scope="scope">-->
<!--          {{scope.row.created_at | moment('MM/DD/YYYY') }}-->
<!--        </template>-->
<!--      </el-table-column>-->
      <el-table-column
        label="STATUS"
        width="90">
        <template slot-scope="scope">
          {{scope.row.status == 0 ? 'Active': "Disabled"}}
        </template>
      </el-table-column>
      <el-table-column
        label="CATEGORY" width="150">
        <template slot-scope="scope">
          {{scope.row.category_names.join(", ")}}
        </template>
      </el-table-column>
      <el-table-column
        class-name="text-center"
        width="120">
        <template>
          <a href="javascript:void(0)" class="btn bloom-btn-light btn-sm font-14">
            Manage
          </a>
        </template>
      </el-table-column>
    </el-table>
    <div class="d-flex my-3">
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
import _ from "lodash";

export default {
  name: "TableProducts",
  props: {
    mediaUrl: {
      type: String,
      default: ""
    },
    products: {
      type: Object,
      default: () => []
    }
  },
  data() {
    return {
      order_by: "",
      page_size: 20,
      current_page: 1,
      total: 0
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
  },
  methods: {
    change_page(page) {
       this.current_page = page;
    }
  }
}
</script>

<style lang="scss">
.table-products {
  .el-table {
    .product-thumbnail {
      width: 50px;
      height: 50px;
      background-position: center;
      background-size: contain;
    }
  }
}
</style>
