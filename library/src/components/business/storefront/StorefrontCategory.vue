<template>
  <div class="product-category" v-loading.fullscreen="loading">
    <div class="mb-4" v-for="(objs, category_id) in filterGroupedCategory" :key="category_id">
      <h3 class="category-title">{{objectCategories[category_id]}}</h3>
      <vue-horizontal-list
        :items="objs"
        :options="{
          responsive: [
            { end: 576, size: 1 },
            { start: 576, end: 768, size: 2 },
            { size: 4 },
          ],
        }">
        <template v-slot:default="{item}">
          <div class="item">
            <business-product-card :product="item" :media-url="mediaUrl"></business-product-card>
          </div>
        </template>
      </vue-horizontal-list>
    </div>
    <div v-if="products.length == 0">
      {{ loading ? "Loading...": "No data" }}
    </div>
  </div>
</template>

<script>
import axios from "axios";
import {mapState} from "vuex";
import VueHorizontalList from "vue-horizontal-list";
import _ from "lodash";

export default {
  name: "StorefrontCategory",
  props: {
    orderBy: {
      type: String
    },
    mediaUrl: {
      type: String,
      default: ""
    },
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
  created() {
    let that = this;
    that.loading = true;
    axios.get('/api/shop/products/?view=all').then(function (res) {
      that.products = res.data
      that.loading = false
    }).catch(function () {
      that.loading = false
    })
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
    filterGroupedCategory() {
      let that = this, sortedGroup = {};
      if (this.orderBy == 'title') {
        Object.keys(this.groupedCategory).forEach((category) => {
          sortedGroup[category] = _.orderBy(that.groupedCategory[category], 'title')
        })
        return sortedGroup;
      } else if (this.orderBy == 'price') {
        Object.keys(this.groupedCategory).forEach((category) => {
          sortedGroup[category] = _.orderBy(that.groupedCategory[category], 'price')
        })
        return sortedGroup;
      } else {
        return this.groupedCategory
      }
    },

  },
  methods: {
  }
}
</script>

<style lang="scss">
  .product-category {
    .category-title {
      font-size: 20px;
      margin-bottom: 0px;
    }

  }
</style>
