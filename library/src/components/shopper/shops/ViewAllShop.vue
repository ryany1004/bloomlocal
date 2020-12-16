<template>
  <div v-loading.fullscreen="loading" class="row shop-cards">
    <div class="col-lg-2 col-md-3 col-6 mb-5" v-for="shop in data_shops" :key="shop.id">
      <section class="shop-card">
        <a href="javascript:void(0)">
          <div class="card-image" :style="{backgroundImage: `url('${mediaUrl}${shop.logo}')`}">
          </div>
        </a>
        <article class="px-2 mt-2">
          <div class="d-flex">
            <h2 :title="shop.name" class="shop-name flex-grow-1"><a href="javascript:void(0)">{{shop.name}}</a></h2>
            <following-love :shop="shop"></following-love>
          </div>

          <ul class="list-categories">
            <li v-for="category in shop.category_names" :key="category.id">{{category.name}}</li>
          </ul>
        </article>
        <footer class="px-2 pb-2">
          <ul class="shop-feature">
            <li>Free Delivery</li>
            <li>Christmas Sale</li>
            <li>Custom offers</li>
          </ul>
        </footer>
      </section>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import _ from "lodash";

export default {
  name: "ViewAllShop",
  data: function () {
    return {
      shops: [],
      loading: false
    }
  },
  props: {
    orderBy: {
      type: String
    },
    mediaUrl: {
      type: String,
      default: ""
    },
  },
  computed: {
    data_shops() {
      if (this.orderBy == 'name') {
        return _.orderBy(this.shops, this.orderBy)
      } else {
        return this.shops
      }
    }
  },
  created() {
    let that = this;
    that.loading = true
    axios.get("/api/shops/?view=all").then((res) => {
      that.loading = false;
      that.shops = res.data;
    })
  },
  methods: {

  }
}
</script>

<style scoped>

</style>
