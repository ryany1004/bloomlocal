<template>
  <div class="dashboard">
    <div class="row">
      <div class="col-8 mb-4">
        <welcome></welcome>
      </div>
      <div class="col-4 mb-4">
        <earning></earning>
      </div>
    </div>
    <div class="row">
      <div class="col-3 mb-4">
        <store-visit></store-visit>
      </div>
      <div class="col-3 mb-4">
        <product-views></product-views>
      </div>
      <div class="col-3 mb-4">
        <orders></orders>
      </div>
      <div class="col-3 mb-4">
        <revenue></revenue>
      </div>
    </div>
    <div class="row mb-4">
      <div class="col-md-6 col-sm-12">
        <popular-product-view-sale :media-url="mediaUrl"></popular-product-view-sale>
      </div>
      <div class="col-md-6 col-sm-12">
        <top-products-add-to-cart :media-url="mediaUrl"></top-products-add-to-cart>
      </div>
    </div>
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

    <div class="row widget-list mb-4">
      <div class="col-md-6 col-sm-12">
        <div class="charts">
          <order-by-day></order-by-day>
        </div>
      </div>
      <div class="col-md-6 col-sm-12">
        <div class="charts">
          <revenue-by-day></revenue-by-day>
        </div>
      </div>

      <div class="col-md-6 col-sm-12">
        <div class="charts">
          <products-added-to-cart-by-day></products-added-to-cart-by-day>
        </div>
      </div>
      <div class="col-md-6 col-sm-12">
        <div class="charts">
          <products-view-by-day></products-view-by-day>
        </div>
      </div>
      <div class="col-md-6 col-sm-12">
        <div class="charts">
          <storefront-view-by-day></storefront-view-by-day>
        </div>
      </div>

      <div class="col-md-6 col-sm-12">
        <div class="charts">
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
import Earning from "@/components/business/dashboard/Earning";
import Welcome from "@/components/business/dashboard/Welcome";
import StoreVisit from "@/components/business/dashboard/StoreVisit";
import ProductViews from "@/components/business/dashboard/ProductViews";
import Orders from "@/components/business/dashboard/Orders";
import Revenue from "@/components/business/dashboard/Revenue";
import TopProductsAddToCart from "@/components/business/dashboard/TopProductsAddToCart";

export default {
  name: "Dashboard",
  components: {
    TopProductsAddToCart,
    Revenue,
    Orders,
    ProductViews,
    StoreVisit,
    Welcome,
    Earning,
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

<style lang="scss">
.dashboard {
  .wbox {
    background: #FFFFFF;
    box-shadow: 0px 9px 35px rgba(0, 0, 0, 0.03);
    border-radius: 24px;
  }
  .sm-box {
    padding: 24px 15px;
    .d-filter-opts {
      font-size: 14px;
      a {
        font-size: 14px;
        color: #919EAB;
        text-decoration: none;
      }
      strong {
        font-size: 18px;
      }
    }
    .summary-st {
      .a-icon {
        width: 62px;
        height: 62px;
        display: inline-block;
      }
      .a-store {
        background: url("../../../assets/icons/icon-d-store.png");
      }
      .a-product {
        background: url("../../../assets/icons/icon-d-product.png");
      }
      .a-orders {
        background: url("../../../assets/icons/icon-d-order.png");
      }
      .a-revenue {
        background: url("../../../assets/icons/icon-d-revenue.png");
      }
      span {
        font-weight: 900;
        font-size: 32px;
        margin-left: 16px;
      }
    }
  }
  .welcome {
    padding: 32px;
    .welcome-text {
      margin-top: 30px;
      font-style: normal;
      font-weight: normal;
      font-size: 22px;
      color: #637381;
    }
    .m-icon {
      width: 36px;
      height: 36px;
      display: inline-block;
    }
    .manage {
      margin-bottom: 16px;
    }
    .btn-manage {
      display: flex;
      margin-left: 20px;
      padding: 9px 0;
      text-decoration: none;
      .m-btn-text {
        display: flex;
        flex-direction: column;
        margin-left: 1rem;
        .m-text {
          font-size: 16px;
          color: #212B36;
          line-height: 18px;
        }
        .m-sub-text {
          color: #919EAB;
          font-size: 14px
        }
      }
      .m-orders {
        background: url("../../../assets/icons/manage-order.png");
      }
      .m-products {
        background: url("../../../assets/icons/manage-product.png");
      }
      .m-store {
        background: url("../../../assets/icons/manage-store.png");
      }
      .m-notification {
        background: url("../../../assets/icons/manage-notification.png");
      }
    }
  }
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
