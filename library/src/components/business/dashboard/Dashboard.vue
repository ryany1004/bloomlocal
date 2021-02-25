<template>
  <div class="dashboard">
    <div class="row">
      <div class="col-md-4 col-sm-12 mb-4">
        <sale-pie-chart></sale-pie-chart>
      </div>
      <div class="col-md-8 col-sm-12">
        <div class="row widget-list">
          <div class="col-md-6 col-sm-12">
            <order-by-month></order-by-month>
          </div>
          <div class="col-md-6 col-sm-12">
            <revenue-by-month></revenue-by-month>
          </div>
          <div class="col-md-4 col-sm-12">
            <other-data-report></other-data-report>
          </div>

          <div class="col-md-4 col-sm-12">
            <products-added-to-cart-by-month></products-added-to-cart-by-month>
          </div>

          <div class="col-md-4 col-sm-12">
            <products-view-by-month></products-view-by-month>
          </div>

          <div class="col-md-6 col-sm-12">
            <storefront-view-by-month></storefront-view-by-month>
          </div>

          <div class="col-md-6 col-sm-12">
            <products-view-channels-by-month></products-view-channels-by-month>
          </div>
        </div>
      </div>
    </div>

    <div class="row widget-list mt-4">
      <div class="col-md-4 col-sm-12">
        <div class="charts">
          <p class="bolder font-14" style="margin: 0px 0 0 15px">Orders by Day</p>
          <order-by-day></order-by-day>
        </div>
      </div>
      <div class="col-md-4 col-sm-12">
        <div class="charts">
          <p class="bolder font-14" style="margin: 0px 0 0 15px">Revenue by Day</p>
          <revenue-by-day></revenue-by-day>
        </div>
      </div>
      <div class="col-md-4 col-sm-12">
        <popular-product-view-sale :media-url="mediaUrl"></popular-product-view-sale>
      </div>

      <div class="col-md-4 col-sm-12">
        <div class="charts">
          <p class="bolder font-14" style="margin: 0px 0 0 15px">Products Added To Cart</p>
          <products-added-to-cart-by-day></products-added-to-cart-by-day>
        </div>
      </div>
      <div class="col-md-4 col-sm-12">
        <div class="charts">
          <p class="bolder font-14" style="margin: 0px 0 0 15px">Product Views by Day</p>
          <products-view-by-day></products-view-by-day>
        </div>
      </div>
      <div class="col-md-4 col-sm-12">
        <div class="charts">
          <p class="bolder font-14" style="margin: 0px 0 0 15px">Storefront views</p>
          <storefront-view-by-day></storefront-view-by-day>
        </div>
      </div>

      <div class="col-md-4 col-sm-12">
        <div class="charts">
          <p class="bolder font-14" style="margin: 0px 0 0 15px">Product Views from Channels</p>
          <products-view-channels-by-day></products-view-channels-by-day>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import SalePieChart from "@/components/business/dashboard/SalePieChart";
import ProductsViewByDay from "@/components/business/dashboard/ProductsViewByDay";
import StorefrontViewByDay from "./StorefrontViewByDay";
import ProductsAddedToCartByDay from "./ProductsAddedToCartByDay";
import StorefrontViewByMonth from "./StorefrontViewByMonth";
import ProductsAddedToCartByMonth from "./ProductsAddedToCartByMonth";
import ProductsViewByMonth from "./ProductsViewByMonth";
import OrderByDay from "./OrderByDay";
import RevenueByDay from "./RevenueByDay";
import OrderByMonth from "./OrderByMonth";
import RevenueByMonth from "./RevenueByMonth";
import PopularProductViewSale from "./PopularProductViewSale";
import OtherDataReport from "./OtherDataReport";
import ProductsViewChannelsByMonth from "./ProductsViewChannelsByMonth";
import ProductsViewChannelsByDay from "./ProductsViewChannelsByDay";

export default {
  name: "Dashboard",
  components: {
    ProductsViewChannelsByDay,
    ProductsViewChannelsByMonth,
    OtherDataReport,
    PopularProductViewSale,
    RevenueByMonth,
    OrderByMonth,
    RevenueByDay,
    OrderByDay,
    ProductsViewByMonth,
    ProductsAddedToCartByMonth,
    StorefrontViewByMonth,
    ProductsAddedToCartByDay,
    StorefrontViewByDay,
    ProductsViewByDay,
    SalePieChart
  },
  props: {
    mediaUrl: {
      type: String,
      required: true
    }
  },
  data: function () {
    return {
      loading: false,
      order_data: []
    }
  },
  created() {

  },
  computed: {
  },
  methods: {

  }
}
</script>

<style scoped lang="scss">
.dashboard {
  .widget-list {
    > div {
      margin-bottom: 25px;
    }
  }
  .slide-section {
    background-color: #6C5DD3;
    height: 300px;
    width: 100%;
    border-radius: 24px;
    z-index: 1;
    .close-btn {
      right: 10px;
      top: 10px
    }
  }
  @media (max-width: 414px) {
    .slide-section {
      height: auto !important;
    }
    .c-1 {
      order: 1;
      margin: 15px 0;
    }
    .c-2 {
      order: 2;
      margin: 15px 0;
    }
  }
  .report-box2 {
    border-radius: 24px;
    padding: 5px;
    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.12);
  }

  .bg-bottom {
    position: absolute;
    left: 2%;
    right: 2%;
    top: 4.9%;
    bottom: -3.18%;
    background: #CFC8FF;
    border-radius: 24px;
    z-index: -1;
  }
  margin-bottom: 20px;
  .pie-chart {
    min-height: 50px;
    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.12);
    border-radius: 10px;
    background-color: #fff;
  }
  .order-received, .revenue, .per-order, .charts {
    padding: 20px;
    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.12);
    border-radius: 10px;
    font-size: 12px;
    background-color: #fff;
  }
  .product-sale-chart {
    min-height: 50px;
    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.12);
    border-radius: 10px;
    background-color: #fff;
  }
  .color-red {
    color: red;
  }
}
</style>
