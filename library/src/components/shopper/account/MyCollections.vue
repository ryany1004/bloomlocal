<template>
  <div v-loading.fullscreen="loading">
    <div class="product-category" v-loading.fullscreen="loading" v-if="products.length > 0">
      <div class="mb-4" v-for="(objs, category_id) in groupedCategory" :key="category_id">
        <h3 class="category-title">{{objectCategories[category_id]}}</h3>
        <vue-horizontal-list
          :items="objs"
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
      </div>
    </div>
    <div v-else>
      <p>No any products here</p>
    </div>
  </div>
</template>

<script>
import VueHorizontalList from "vue-horizontal-list";
import {mapState} from "vuex";
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
      products: [],
      loading: false,
    }
  },
  computed: {
    ...mapState([
        'categories',
    ]),
    objectCategories() {
      let obj = {};
      this.categories.forEach((c) => {
        obj[c.id] = c.name;
      })
      return obj;
    },
    groupedCategory() {
      let groups = {}, that = this;
      that.products.forEach((p) => {
        p.categories.forEach((c) => {
          if (groups[c] == undefined) {
            groups[c] = [p];
          } else {
            groups[c].push(p);
          }
        })
      })
      return groups
    },
  },
  created() {
    let that = this;
    that.loading = true;
    axios.get(`/api/user/wishlist-products/`).then(function (res) {
      that.products = res.data
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
