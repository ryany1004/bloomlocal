<template>
  <div class="multi-shops">
    <div class="d-flex justify-content-center">
      <ul class="shop-filter">
        <li :class="{active: filter.value == active_filter}" v-for="filter in top_filters" :key="filter.value">
          <a href="javascript:void(0)" @click="active_filter = filter.value">{{ filter.text }}</a>
        </li>
      </ul>
    </div>
    <div class="d-flex justify-content-end mb-4">
      <div class="dropdown mx-4">
        <button class="btn btn-light btn-sm dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
          View by {{sort_by_text}}
        </button>
        <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
          <a class="dropdown-item" href="javascript:void(0)" @click="order_by='all'">All</a>
          <a class="dropdown-item" href="javascript:void(0)" @click="order_by='name'">Name</a>
        </div>
      </div>
    </div>

    <best-selling-shop v-if="active_filter == 'best_selling'" :media-url="mediaUrl" :order-by="order_by"></best-selling-shop>
    <recent-added-shop v-else-if="active_filter == 'recent_added'" :media-url="mediaUrl" :order-by="order_by"></recent-added-shop>
    <category-shop v-else-if="active_filter == 'category'" :media-url="mediaUrl" :order-by="order_by"></category-shop>
    <view-all-shop v-else-if="active_filter == 'view_all'" :media-url="mediaUrl" :order-by="order_by"></view-all-shop>
  </div>
</template>

<script>
export default {
  name: "MultiShops",
  props: {
    mediaUrl: {
      type: String,
      default: ""
    }
  },
  data: function () {
    return {
      active_filter: 'recent_added',
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
      let text = "All";
      if (this.order_by == "name") {
        text = "Name"
      }
      return text
    },
  },
  created() {
    this.$store.dispatch('get_shop_categories');
  },
  methods: {

  }
}
</script>

<style lang="scss">
.font-8 {
  font-size: 8px;
}
.multi-shops {
  .shop-filter {
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
  .btn-light {
    border-color: #bdbdbd;
  }
}
.shop-cards {
  @media (min-width: 992px) {
    .col-lg-2 {
       max-width: 20%;
      flex: 0 0 20%;
    }
  }
  .category-title {
    font-size: 20px;
    margin-bottom: 0px;
  }
  .shop-card {
    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.12);
    border-radius: 10px;
    background-color: #fff;

    .card-image {
      height: 153px;
      width: 100%;
      background-size: cover;
      background-position: center;
      background-repeat: no-repeat;
      border: 1px solid #f8f8f8;
      border-top-right-radius: 10px;
      border-top-left-radius: 10px;
    }
    h2 {
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      font-size: 18px;
      margin-bottom: 0;
      a {
        font-size: 14px;
        color: #4F4F4F;
      }
    }
    .list-categories {
      margin-bottom: 0;
      padding-left: 0;
      height: 24px;
      li {
        display: inline-block;
        margin-right: 8px;
        font-size: 8px;
        color: #0C242E;
      }
      li + li::before {
        content: "•";
        padding-right: 8px;
      }
    }
    footer {
      .shop-feature {
        margin-bottom: 0;
        padding-left: 0;
        li {
          display: inline-block;
          margin-right: 3px;
          font-size: 8px;
          color: #828282;
        }
        li:last-child {
          margin-right: 0px;
        }
      }
    }
  }
}
</style>
