<template>
  <div class="dashboard">
    <div class="row">
      <div class="col-4">
        <div class="pie-chart">
          <sale-pie-chart></sale-pie-chart>
        </div>
      </div>
      <div class="col-8">
        <div class="row">
          <div class="col-6">
            <div class="order-received font-14" v-loading="loading">
              <p>Orders Received</p>
              <div class="d-flex justify-content-between align-items-center mt-5">
                <div>{{ percent_order_increase.toFixed(0) }}%</div>
                <div>
                  This month
                  <div class="d-flex justify-content-between align-items-center mt-2">
                    <i :title="order_increase" class="fas"
                       :class="{
                        'fa-arrow-up': order_increase > 0,
                        'fa-arrow-down': order_increase < 0,
                        'fa-horizontal-rule': order_increase == 0,
                        'color-1': order_increase >= 0,
                        'color-red': order_increase < 0,}"></i>
                    <span>{{ total_order }}</span>
                  </div>
                </div>
              </div>
              <div class="progress mt-2" style="height: 20px;border-radius: 15px;">
                <div class="progress-bar" role="progressbar" :style="{width: `${progress_order}%`}" aria-valuenow="25" aria-valuemin="0" aria-valuemax="100"></div>
              </div>
            </div>
          </div>
          <div class="col-6">
            <div class="revenue" v-loading="loading">
              <p>Revenue</p>
              <div class="d-flex justify-content-between align-items-center mt-5">
                <div>{{ percent_revenue_increase.toFixed(0) }}%</div>
                <div>
                  This month
                  <div class="d-flex justify-content-between align-items-center mt-2">
                    <i :title="`${revenue_increase | numFormat}$`" class="fas"
                       :class="{
                        'fa-arrow-up': revenue_increase > 0,
                        'fa-arrow-down': revenue_increase < 0,
                        'fa-horizontal-rule': revenue_increase == 0,
                        'color-1': revenue_increase >= 0,
                        'color-red': revenue_increase < 0,}"></i>
                    <span>${{ total_revenue | numFormat }}</span>
                  </div>
                </div>
              </div>
              <div class="progress mt-2" style="height: 20px;border-radius: 15px;">
                <div class="progress-bar bg-success" role="progressbar" :style="{width: `${progress_revenue}%`}" aria-valuenow="25" aria-valuemin="0" aria-valuemax="100"></div>
              </div>
            </div>
          </div>
        </div>

        <div class="product-sale-chart mt-4">
          <product-sales-chart></product-sales-chart>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import SalePieChart from "@/components/business/dashboard/SalePieChart";
import ProductSalesChart from "@/components/business/dashboard/ProductSalesChart";
import axios from "axios";

export default {
  name: "Dashboard",
  components: {
    SalePieChart,
    ProductSalesChart,
  },
  data: function () {
    return {
      loading: false,
      order_data: []
    }
  },
  created() {
    this.get_order_revenue();
  },
  computed: {
    total_order() {
      if (this.order_data.this_month) {
        return this.order_data.this_month.total_orders
      }
      return "N/A"
    },
    progress_revenue() {
      if (this.percent_revenue_increase > 0) {
        return this.percent_revenue_increase <= 100 ? this.percent_revenue_increase : 100
      }
      return 0
    },
    progress_order() {
       if (this.percent_order_increase > 0) {
        return this.percent_order_increase <= 100 ? this.percent_order_increase : 100
      }
      return 0
    },
    total_revenue() {
      if (this.order_data.this_month) {
        return this.order_data.this_month.revenue;
      }
      return "N/A"
    },
    order_increase() {
      let data = this.order_data
      if (data.this_month) {
        return data.this_month.total_orders - data.previous_month.total_orders;
      }
      return 0;
    },
    percent_order_increase() {
      if (this.order_data.previous_month) {
        let data = this.order_data.previous_month;
        return data.total_orders > 0 ? (this.order_increase / data.total_orders * 100) : 100;
      }
      return 0;
    },
    revenue_increase() {
      let data = this.order_data
      if (data.this_month) {
        return data.this_month.revenue - data.previous_month.revenue;
      }
      return 0;
    },
    percent_revenue_increase() {
      if (this.order_data.previous_month) {
        let data = this.order_data.previous_month
        return data.revenue > 0 ? (this.revenue_increase / data.revenue * 100) : 100;
      }
      return 0;
    }
  },
  methods: {
    get_order_revenue() {
      let that = this;
      that.loading = true
      axios.get('/api/statistic/order-revenue/by-month/').then(res => {
        that.order_data = res.data;
        that.loading = false;
      }).catch(() => {
        that.loading = false;
      })
    }
  }
}
</script>

<style scoped lang="scss">
.dashboard {
  margin-bottom: 20px;
  .pie-chart {
    min-height: 50px;
    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.12);
    border-radius: 10px;
  }
  .order-received, .revenue {
    padding: 20px;
    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.12);
    border-radius: 10px;
    font-size: 12px;
  }
  .product-sale-chart {
    min-height: 50px;
    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.12);
    border-radius: 10px;
  }
  .color-red {
    color: red;
  }
}
</style>
