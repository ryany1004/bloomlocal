<template>
  <div v-loading.fullscreen="loading" class="row shop-cards">
    <div class="col-lg-2 col-md-3 col-6 mb-5" v-for="shop in data_shops" :key="shop.id">
      <shop-card :shop="shop" :media-url="mediaUrl"></shop-card>
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
