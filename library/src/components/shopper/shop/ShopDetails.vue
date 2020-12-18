<template>
  <div class="shop-details">
    <div class="d-flex justify-content-center">
      <ul class="product-filter">
        <li :class="{active: filter.value == active_filter}" v-for="filter in top_filters" :key="filter.value">
          <a href="javascript:void(0)" @click="active_filter = filter.value">{{ filter.text }}</a>
        </li>
      </ul>
    </div>
    <div class="d-flex justify-content-between mb-4">
      <div class="d-flex align-items-center">
        <span class="btn btn-primary btm-sm font14 mr-3 white">{{ shopName }}</span>
        <a href="javascript:void(0)" v-if="isLoggedIn" class="btn btn-light btn-sm" @click="toggleLove(shopId)"><i class="fa-heart color-red" :class="{fas: user.love_shops.indexOf(shopId) != -1, far: user.love_shops.indexOf(shopId) == -1}"></i></a>
      </div>
      <div class="dropdown">
        <button class="btn btn-light btn-sm dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
          View by {{sort_by_text}}
        </button>
        <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
          <a class="dropdown-item" href="javascript:void(0)" @click="order_by='all'">All</a>
          <a class="dropdown-item" href="javascript:void(0)" @click="order_by='title'">Name</a>
          <a class="dropdown-item" href="javascript:void(0)" @click="order_by='price'">Price</a>
        </div>
      </div>
    </div>

    <best-selling-product v-if="active_filter == 'best_selling'" :shop-id="shopId"
                          :media-url="mediaUrl" :order-by="order_by"></best-selling-product>
    <recent-added-product v-else-if="active_filter == 'recent_added'" :shop-id="shopId"
                          :media-url="mediaUrl" :order-by="order_by"></recent-added-product>
    <category-product v-else-if="active_filter == 'category'" :shop-id="shopId"
                      :media-url="mediaUrl" :order-by="order_by"></category-product>
    <view-all-product v-else-if="active_filter == 'view_all'" :shop-id="shopId"
                      :media-url="mediaUrl" :order-by="order_by"></view-all-product>
  </div>
</template>

<script>
import {mapState} from "vuex";
import axios from "axios";

export default {
  name: "ShopDetails",
  props: {
    mediaUrl: {
      type: String,
      default: ""
    },
    shopId: {
      type: Number,
      required: true
    },
    shopName: {
      type: String
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
      heart: false,
    }
  },
  computed: {
    ...mapState([
        "isLoggedIn",
        "user"
    ]),
    sort_by_text() {
      let text = "All";
      if (this.order_by == "name") {
        text = "Name"
      }
      return text
    },
  },
  created() {
    this.$store.dispatch('get_categories');
    this.$store.dispatch("get_user");
    this.$store.dispatch("get_sizes");
    this.$store.dispatch("get_colors");
  },
  methods: {
    toggleLove(shopId) {
      let that = this;
      axios.post(`/api/user/shop/${shopId}/love/`).then((res) => {
        that.$store.dispatch('set_user', res.data);
      })
    }
  }
}
</script>

<style lang="scss">
.shop-details {
  .font14 {
    font-size: 14px;
  }
  .color-red {
    color: #ED6B5E;
  }
  .product-filter {
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
  .product-cards {
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

    .product-card {
      box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.12);
      border-radius: 10px;
      padding: 6px;
      background-color: #fff;

      .card-image {
        height: 153px;
        width: 100%;
        background-size: contain;
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

        a {
          font-size: 14px;
          color: #0C242E;
        }
      }

      p {
        font-size: 11px;
        height: 43px;
        line-height: 14px;
        overflow: hidden;
        display: -webkit-box;
        -webkit-line-clamp: 3;
        -webkit-box-orient: vertical;
        margin-bottom: 0.5rem;
      }

      footer {
        font-size: 11px;

        a {
          font-size: 11px;
        }
      }
    }
  }
}
</style>
