<template>
  <div v-loading.fullscreen="loading" class="my-orders container">
    <el-table
      :data="pagingTableData"
      class="orders-table"
      style="width: 100%">
      <el-table-column
        prop="product_title"
        label="Product">
      </el-table-column>
      <el-table-column
        prop="quantity"
        label="Quantity"
        class-name="text-center"
        width="80">
      </el-table-column>
      <el-table-column
        width="100"
        label="Order Number">
        <template slot-scope="scope">
          #{{ scope.row.order_no }}
        </template>
      </el-table-column>
      <el-table-column
          width="80"
          class-name="text-center"
          label="Purchase Price">
        <template slot-scope="scope">
          ${{ scope.row.price }}
        </template>
      </el-table-column>
      <el-table-column
          class-name="text-center"
        label="Total Price">
        <template slot-scope="scope">
          ${{ scope.row.price *  scope.row.quantity }}
        </template>
      </el-table-column>
      <el-table-column
          width="100"
          class-name="text-center"
        label="Commission Rate">
        <template slot-scope="scope">
          {{ scope.row.commission_rate }}%
        </template>
      </el-table-column>
      <el-table-column
          class-name="text-center"
        label="Total Commission Fee">
        <template slot-scope="scope">
          ${{ (scope.row.commission_rate * scope.row.price *  scope.row.quantity / 100).toFixed(1) }}
        </template>
      </el-table-column>
      <el-table-column
          width="100"
          class-name="text-center"
        label="Shopper Information">
        <template slot-scope="scope">
          <a href="javascript:void(0)" @click="showShopperDialog(scope.row)"><img src="../../../assets/contact-book.svg"></a>
        </template>
      </el-table-column>
      <el-table-column
        label="Receipt"
        class-name="text-center"
        width="100">
        <template slot-scope="scope">
          <a href="javascript:void(0)" @click="showReceiptDialog(scope.row)" class="btn btn-primary btn-sm font-12 white">
            Receipt <svg width="7" height="9" viewBox="0 0 7 9" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M6.67097 2.52084C6.6499 2.46934 6.61873 2.42259 6.5793 2.38334L4.65013 0.454171C4.57206 0.376567 4.46646 0.333008 4.35638 0.333008C4.2463 0.333008 4.1407 0.376567 4.06263 0.454171C4.02358 0.492906 3.99258 0.53899 3.97143 0.589765C3.95027 0.640539 3.93938 0.695 3.93938 0.750005C3.93938 0.80501 3.95027 0.85947 3.97143 0.910245C3.99258 0.96102 4.02358 1.0071 4.06263 1.04584L5.2793 2.2625H1.94596C1.50394 2.2625 1.08001 2.4381 0.767452 2.75066C0.454892 3.06322 0.279297 3.48714 0.279297 3.92917V8.25C0.279297 8.36051 0.323196 8.46649 0.401336 8.54463C0.479476 8.62277 0.585457 8.66667 0.695964 8.66667C0.806471 8.66667 0.912451 8.62277 0.990591 8.54463C1.06873 8.46649 1.11263 8.36051 1.11263 8.25V3.92917C1.11263 3.70816 1.20043 3.4962 1.35671 3.33992C1.51299 3.18364 1.72495 3.09584 1.94596 3.09584H5.2793L4.06263 4.3125C4.00387 4.37078 3.96379 4.44524 3.94751 4.52639C3.93124 4.60753 3.93949 4.69169 3.97123 4.76812C4.00296 4.84456 4.05674 4.90981 4.12571 4.95556C4.19468 5.00131 4.2757 5.02549 4.35847 5.025C4.46837 5.02344 4.5732 4.97851 4.65013 4.9L6.5793 2.975C6.61772 2.93337 6.64873 2.88545 6.67097 2.83334C6.71151 2.73312 6.71151 2.62106 6.67097 2.52084Z" fill="#FEFEFE"/>
            </svg>
          </a>
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

    <el-dialog title="Shopper Information" :visible.sync="dialogShopperVisible" width="70%">
      <shopper-info :uuid="uuid" v-if="uuid"></shopper-info>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogShopperVisible = false">Close</el-button>
      </span>
    </el-dialog>
    <el-dialog title="Receipt" :visible.sync="dialogReceiptVisible" width="70%">
      <receipt :uuid="uuid" v-if="uuid"></receipt>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogReceiptVisible = false">Close</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "MyOrders",
  props: {
    mediaUrl: {
      type: String,
      default: ""
    }
  },
  data: function () {
    return {
      loading: false,
      page_size: 7,
      current_page: 1,
      total: 0,
      orders: [],
      dialogReceiptVisible: false,
      dialogShopperVisible: false,
      uuid: null
    }
  },
  computed: {
    pagingTableData() {
      let orders = [];
      let size_start = (this.current_page - 1) * this.page_size;
      orders = this.orders.slice(size_start, size_start + this.page_size);
      return orders
    }
  },
  created() {
    this.loading = true;
    this.get_orders('/api/business/my-orders/')
  },
  methods: {
    change_page(page) {
       this.current_page = page;
    },
    get_orders(url) {
      let that = this;
      axios.get(url).then((res) => {
        that.orders = that.orders.concat(res.data.results);
        that.total = res.data.count;
        if (res.data.next) {
          this.get_orders(res.data.next);
        }
        that.loading = false;
      })
    },
    showShopperDialog(item) {
      this.uuid = item.order_uuid;
      this.dialogShopperVisible = true;
    },
    showReceiptDialog(item) {
      this.uuid = item.order_uuid;
      this.dialogReceiptVisible = true;
    }
  }
}
</script>

<style lang="scss">
.my-orders {
  .el-table {
    font-size: 12px;
    .cell {
      word-break: break-word;
    }
  }
  .el-table thead tr th {
    background-color: #ecf5fc !important;
  }
  .orders-table {

  }
}
</style>
