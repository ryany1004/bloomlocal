<template>
  <div v-loading.fullscreen="loading" class="business my-orders">
    <h3 class="business-title">Store Orders</h3>

    <div class="form-row align-items-center my-3 ml-2">
      <div class="col-auto my-1">
        <div class="form-check form-check-inline mr-0">
          <input class="form-check-input" type="checkbox" id="inlineCheckbox1" value="option1">
        </div>
      </div>
      <div class="col-auto my-1">
        <select class="custom-select mr-sm-2" id="inlineFormCustomSelect">
          <option disabled selected>Manage Orders</option>
        </select>
      </div>
      <div class="col-auto my-1">
        <select class="custom-select mr-sm-2" id="inlineFormCustomSelect2">
          <option disabled selected>Filter Orders</option>
        </select>
      </div>
    </div>

    <el-table
      :data="pagingTableData"
      stripe
      class="orders-table"
      style="width: 100%">
      <el-table-column
      type="selection"
      width="43">
      </el-table-column>
      <el-table-column width="40">
        <template slot-scope="scope">
          <img :src="`${mediaUrl}${scope.row.product.thumbnail}`" class="product-thumb">
        </template>
      </el-table-column>
      <el-table-column
        label="PRODUCT">
        <template slot-scope="scope">
          {{ scope.row.product.title }}
        </template>
      </el-table-column>
      <el-table-column
        width="100"
        label="ORDER #">
        <template slot-scope="scope">
          #{{ scope.row.order_no }}
        </template>
      </el-table-column>
      <el-table-column
          width="80"
          class-name="text-center"
          label="PRICE">
        <template slot-scope="scope">
          ${{ scope.row.price }}
        </template>
      </el-table-column>
      <el-table-column
          class-name="text-center"
        label="TOTAL PRICE">
        <template slot-scope="scope">
          ${{ scope.row.price *  scope.row.quantity | numFormat("0.00") }}
        </template>
      </el-table-column>
      <el-table-column
        prop="quantity"
        label="QTY SOLD"
        class-name="text-center"
        width="80">
      </el-table-column>
      <el-table-column
          width="100"
          class-name="text-center"
        label="RATE">
        <template slot-scope="scope">
          {{ scope.row.commission_rate }}%
        </template>
      </el-table-column>
      <el-table-column
        class-name="text-center"
        width="100"
        label="FEE">
        <template slot-scope="scope">
          ${{ (scope.row.commission_rate * scope.row.price *  scope.row.quantity / 100) | numFormat("0.00") }}
        </template>
      </el-table-column>
      <el-table-column
        width="100"
        prop="order_status"
        class-name="text-center"
        label="STATUS">
      </el-table-column>
<!--      <el-table-column-->
<!--          width="100"-->
<!--          class-name="text-center"-->
<!--        label="Shopper Information">-->
<!--        <template slot-scope="scope">-->
<!--          <a href="javascript:void(0)" @click="showShopperDialog(scope.row)"><img src="../../../assets/contact-book.svg"></a>-->
<!--        </template>-->
<!--      </el-table-column>-->
      <el-table-column
        class-name="text-center"
        width="120">
        <template slot-scope="scope">
          <a href="javascript:void(0)" @click="showReceiptDialog(scope.row)" class="btn bloom-btn-light btn-sm font-14">
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

</style>
