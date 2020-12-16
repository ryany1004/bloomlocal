<template>
  <div class="product-category" v-loading.fullscreen="loading">
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
            <section class="product-card">
              <a :href="`/business/product/${item.uuid}/update/`">
                <div class="card-image" :style="{backgroundImage: `url('${mediaUrl}${item.thumbnail}')`}">
                </div>
              </a>
              <article>
                <h2 :title="item.title" class="mt-2"><a :href="`/business/product/${item.uuid}/update/`">{{item.title}}</a></h2>
                <p>{{item.description}}</p>
              </article>
              <footer class="d-flex justify-content-between align-items-center">
                <span>Price: ${{item.price}}</span>
                <a href="javascript:void(0)" class="btn btn-primary btn-sm"><i class="fas fa-plus"></i> Add to cart</a>
              </footer>
            </section>
          </div>
        </template>
      </vue-horizontal-list>
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
    }
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
    .product-card {
      box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.12);
      border-radius: 10px;
      padding: 6px;
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
</style>
