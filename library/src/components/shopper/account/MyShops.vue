<template>
  <div class="my-shops" v-loading.fullscreen="loading">
    <section class="mb-5">
      <h3 class="section-title">Following</h3>
      <div class="shop-cards" v-if="followed_shops.length > 0">
        <vue-horizontal-list
          :items="followed_shops"
          :options="{
            responsive: [
              { end: 576, size: 2 },
              { start: 576, end: 768, size: 3 },
              { size: 5 },
            ],
          }">
          <template v-slot:default="{item}">
            <div class="item">
              <shop-card :shop="item" :media-url="mediaUrl"></shop-card>
            </div>
          </template>
        </vue-horizontal-list>
      </div>
      <div v-else class="font-14 mt-3">
        No followed shops
      </div>
    </section>

    <section class="mb-5">
      <h3 class="section-title">Recently Viewed</h3>
      <div class="shop-cards" v-if="recent_viewed_shops.length > 0">
        <vue-horizontal-list
          :items="recent_viewed_shops"
          :options="{
            responsive: [
              { end: 576, size: 2 },
              { start: 576, end: 768, size: 3 },
              { size: 5 },
            ],
          }">
          <template v-slot:default="{item}">
            <div class="item">
              <shop-card :shop="item.shop" :media-url="mediaUrl"></shop-card>
            </div>
          </template>
        </vue-horizontal-list>
      </div>
      <div v-else class="font-14 mt-3">
        No recent viewed shops
      </div>
    </section>

    <section class="mb-5">
      <h3 class="section-title">Similar Shops</h3>
      <div class="shop-cards" v-if="similar_shops.length > 0">
        <vue-horizontal-list
          :items="similar_shops"
          :options="{
            responsive: [
              { end: 576, size: 2 },
              { start: 576, end: 768, size: 3 },
              { size: 5 },
            ],
          }">
          <template v-slot:default="{item}">
            <div class="item">
              <shop-card :shop="item" :media-url="mediaUrl"></shop-card>
            </div>
          </template>
        </vue-horizontal-list>
      </div>
      <div v-else class="font-14 mt-3">
        No similar shops
      </div>
    </section>
  </div>
</template>

<script>
import VueHorizontalList from "vue-horizontal-list";
import axios from "axios";

export default {
  name: "MyShops",
  props: {
    mediaUrl: {
      type: String,
      default: ""
    }
  },
  components: {
      VueHorizontalList
  },
  data: function () {
    return {
      followed_shops: [],
      recent_viewed_shops: [],
      similar_shops: [],
      loading: false
    }
  },
  computed: {
    shop_empty() {
      return this.followed_shops.length == 0 && this.recent_viewed_shops.length == 0 && this.similar_shops.length == 0;
    }
  },
  created() {
    this.get_followed_shops();
    this.get_recent_viewed_shops();
    this.get_similar_shops();
  },
  methods: {
    get_followed_shops() {
      let that = this;
      that.loading = true;
      axios.get("/api/user/followed-shops/").then(res => {
        that.followed_shops = res.data;
        that.loading = false;
      }).catch(() => {
        that.loading = false;
      })
    },
    get_recent_viewed_shops() {
      let that = this;
      that.loading = true;
      axios.get("/api/user/recent-viewed-shops/").then(res => {
        that.recent_viewed_shops = res.data;
        that.loading = false;
      }).catch(() => {
        that.loading = false;
      })
    },
    get_similar_shops() {
      let that = this;
      that.loading = true;
      axios.get("/api/user/similar-shops/").then(res => {
        that.similar_shops = res.data;
        that.loading = false;
      }).catch(() => {
        that.loading = false;
      })
    },
  }
}
</script>

<style lang="scss">
.my-shops {
  .section-title {
    font-size: 18px;
    margin-bottom: 0px;
  }
}
</style>
