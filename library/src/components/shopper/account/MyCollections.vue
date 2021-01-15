<template>
  <div v-loading.fullscreen="loading">
    <div class="product-category" v-loading.fullscreen="loading" v-if="collections.length > 0">
      <div class="mb-4" v-for="collection in collections" :key="collection.id">
        <h3 class="category-title">{{collection.collection_name}}</h3>
        <vue-horizontal-list v-if="collection.products.length > 0"
          :items="collection.items"
          :options="{
            responsive: [
              { end: 576, size: 2 },
              { start: 576, end: 768, size: 3 },
              { size: 5 },
            ],
          }">
          <template v-slot:default="{item}">
            <div class="item">
              <product-card :product="item" :media-url="mediaUrl"></product-card>
            </div>
          </template>
        </vue-horizontal-list>
        <p v-else class="mt-3 font-12 mb-5">No products</p>
      </div>
    </div>
    <div v-else>
      <p>No collections</p>
    </div>
  </div>
</template>

<script>
import VueHorizontalList from "vue-horizontal-list";
import axios from "axios";

export default {
  name: "MyCollections",
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
      collections: [],
      loading: false,
    }
  },
  computed: {

  },
  created() {
    let that = this;
    that.loading = true;
    axios.get(`/api/user/collections/`).then(function (res) {
      that.collections = res.data
      that.loading = false
    }).catch(function () {
      that.loading = false
    })
  },
  methods: {

  }
}
</script>

<style lang="scss">
.category-title {
  font-size: 20px;
  margin-bottom: 0px;
}
</style>
