<template>
  <div class="my-storefront">
    <div class="d-flex justify-content-center">
      <ul class="storefront-filter">
        <li :class="{active: filter.value == active_top_filter}" v-for="filter in top_filters" :key="filter.value">
          <a href="javascript:void(0)" @click="active_top_filter = filter.value">{{ filter.text }}</a>
        </li>
      </ul>
    </div>
    <div class="row mb-4">
      <div class="col-lg-6 col-md-6 col-12">
        <h4>My Storefront</h4>
      </div>
      <div class="col-lg-6 col-md-6 col-12">
        <div class="d-flex align-items-center justify-content-end">
          <a href="/business/product/upload/"><i class="fas fa-plus fa-1x"></i></a>
          <a href="/business/google-merchant/upload/" class="ml-3" title="Upload your products to Google Merchant"><i class="fas fa-upload"></i></a>
          <div class="dropdown">
            <button class="btn btn-primary dropdown-toggle btn-sm white ml-3" type="button" id="dropdownImportButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
              Import
            </button>
            <div class="dropdown-menu" aria-labelledby="dropdownImportButton">
              <a class="dropdown-item font-14" href="/business/products/shopify/import/">Shopify</a>
              <a class="dropdown-item font-14" href="/business/products/file/import/">CSV or Google Spreadsheet</a>
              <a class="dropdown-item font-14" href="/business/products/wordpress/import/">Wordpress</a>
            </div>
          </div>
          <div class="dropdown mx-4">
            <button class="btn btn-light btn-sm dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
              View by {{sort_by_text}}
            </button>
            <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
              <a class="dropdown-item" href="javascript:void(0)" @click="order_by='all'">View all</a>
              <a class="dropdown-item" href="javascript:void(0)" @click="order_by='title'">Name</a>
              <a class="dropdown-item" href="javascript:void(0)" @click="order_by='price'">Price</a>
            </div>
          </div>
          <div class="btn-group btn-group-toggle btn-group-sm" data-toggle="buttons" style="height: 31px">
            <label class="btn btn-primary" :class="{active: view_mode == 'storefront'}" @click="changeViewMode('storefront')">
              <input type="radio" name="options" id="option1" value="storefront"> <i class="fas fa-grip-horizontal"></i>
            </label>
            <label class="btn btn-primary" :class="{active: view_mode == 'inventory'}" @click="changeViewMode('inventory')">
              <input type="radio" name="options" id="option2" value="inventory"> <i class="fas fa-list-alt"></i>
            </label>
          </div>
        </div>
      </div>
    </div>

    <best-selling v-if="active_top_filter == 'best_selling'" :media-url="mediaUrl" :order-by="order_by"></best-selling>
    <recent-added v-else-if="active_top_filter == 'recent_added'" :media-url="mediaUrl" :order-by="order_by"></recent-added>
    <storefront-category v-else-if="active_top_filter == 'category'" :media-url="mediaUrl" :order-by="order_by"></storefront-category>
    <view-all v-else-if="active_top_filter == 'view_all'" :media-url="mediaUrl" :order-by="order_by"></view-all>
  </div>
</template>

<script>
export default {
  name: "MyStorefront",
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
      products: [],
      loading: false,
      view_mode: this.viewMode,
      active_top_filter: 'recent_added',
      top_filters: [
        {value: 'best_selling', text: "Best Selling"},
        {value: 'recent_added', text: "Recent Added"},
        {value: 'category', text: "Category"},
        {value: 'view_all', text: "View All"},
      ],
      order_by: 'all',

    }
  },
  computed: {
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
  created() {
    let that = this;
    that.view_mode = this.viewMode;
    that.$store.dispatch('get_categories')
  },
  methods: {
    changeViewMode(mode) {
      this.$emit("changeViewMode", mode);
    }
  }
}
</script>

<style lang="scss">
  .my-storefront {
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
    .storefront-filter {
      list-style: none;
      li {
        display: inline-block;
        padding: 5px 15px;
        font-size: 18px;
        a {
          color: #4F4F4F;
        }
      }
      li.active {
        font-size: 26px;
      }
    }
  }
  .product-cards {
    @media (min-width: 992px) {
      .col-lg-2 {
         max-width: 20%;
        flex: 0 0 20%;
      }
    }
  }
</style>
