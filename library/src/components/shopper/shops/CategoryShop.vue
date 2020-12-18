<template>
  <div v-loading.fullscreen="loading" class="shop-cards">
    <div class="mb-4" v-for="(objs, category_id) in filterGroupedCategory" :key="category_id">
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
            <shop-card :shop="item" :media-url="mediaUrl"></shop-card>
          </div>
        </template>
      </vue-horizontal-list>
    </div>
  </div>
</template>

<script>
import VueHorizontalList from "vue-horizontal-list";
import axios from "axios";
import {mapState} from "vuex";
import _ from "lodash";

export default {
  name: "CategoryShop",
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
  components: {
    VueHorizontalList
  },
  computed: {
    ...mapState([
        'shop_categories'
    ]),
    objectCategories() {
      let obj = {};
      this.shop_categories.forEach((c) => {
        obj[c.id] = c.name;
      })
      return obj;
    },
    groupedCategory() {
      let groups = {}, that = this;
      that.shops.forEach((p) => {
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
      if (this.orderBy == 'name') {
        Object.keys(this.groupedCategory).forEach((category) => {
          sortedGroup[category] = _.orderBy(that.groupedCategory[category], 'name')
        })
        return sortedGroup;
      } else {
        return this.groupedCategory
      }
    }
  },
  created() {
    let that = this;
    that.loading = true;
    axios.get("/api/shops/?view=all").then((res) => {
      that.loading = false;
      that.shops = res.data;
    })
  },
  methods: {

  }
}
</script>

<style lang="scss">

</style>
