<template>
  <div v-loading="loading">
    <div>
      <el-table
        :data="order.order_items"
        class="orders-table"
        style="width: 100%">
        <el-table-column
          label="Order Number">
          <template slot-scope="scope">
            #{{ scope.row.order_no }}
          </template>
        </el-table-column>
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
            width="120"
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
            ${{ scope.row.price *  scope.row.quantity | numFormat("0.00") }}
          </template>
        </el-table-column>
        <el-table-column
            width="140"
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
            ${{ (scope.row.commission_rate * scope.row.price *  scope.row.quantity / 100) | numFormat("0.00") }}
          </template>
        </el-table-column>
      </el-table>
      <div class="d-flex">
        <div class="ml-auto">
          <ul class="order-summary">
            <li>
              <div class="d-flex">
                <div class="text-right">
                  <span>Product Sub-total = </span>
                </div>
                <div class="txt-price">
                  ${{ sub_total | numFormat("0.00") }}
                </div>
              </div>
            </li>
            <li>
              <div class="d-flex justify-content-between">
                <div class="text-right">
                  <span>Service Fee = </span>
                </div>
                <div class="txt-price">
                  ${{ service_fee | numFormat("0.00") }}
                </div>
              </div>
            </li>
            <li style="border-top: 1px solid #f1f1f1">
              <div class="d-flex justify-content-between">
                <div class="text-right">
                  <span>Shop Revenue = </span>
                </div>
                <div class="txt-price">
                  ${{ purchase_total | numFormat("0.00") }}
                </div>
              </div>
            </li>
          </ul>

        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Receipt",
  props: {
    mediaUrl: {
      type: String,
      default: ""
    },
    uuid: {
      type: String,
      required: true
    }
  },
  data: function () {
    return {
      loading: false,
      order: {}
    }
  },
  watch: {
    uuid: {
      immediate: true,
      handler(val) {
        this.get_order(val);
      }
    }
  },
  computed: {
    sub_total() {
      let total = 0;
      this.order.order_items.forEach((item) => {
        total += (item.price *  item.quantity);
      })
      return total;
    },
    service_fee() {
      let total = 0;
      this.order.order_items.forEach((item) => {
        total += (item.commission_rate * item.price *  item.quantity / 100);
      })
      return total;
    },
    purchase_total() {
      return this.sub_total - this.service_fee;
    }
  },
  methods: {
    get_order(uuid) {
      let that = this;
      that.loading = true;
      axios.get(`/api/order/${uuid}/details/`).then((res) => {
        that.order = res.data;
        that.loading = false;
      }).catch(() => {
        that.loading = false;
        alert("Unable to load data");
      })
    }
  }
}
</script>

<style scoped lang="scss">
.order-summary {
  list-style: none;
  margin-top: 40px;
  li {
    padding: 5px 0;
    .text-right {
      width: 200px;
    }
    .txt-price {
      flex: 0 0 80px;
      padding-left: 10px;
      text-align: right;
    }
  }
}
</style>
