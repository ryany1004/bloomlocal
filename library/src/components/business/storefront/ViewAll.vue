<template>
  <div v-loading.fullscreen="loading" class="row product-cards">
    <div class="col-lg-2 col-md-3 col-6 mb-5" v-for="product in data_products" :key="product.id">
      <section class="product-card">
        <a :href="`/business/product/${product.uuid}/update/`">
          <div class="card-image" :style="{backgroundImage: `url('${mediaUrl}${product.thumbnail}')`}">
          </div>
        </a>
        <article>
          <h2 :title="product.title" class="mt-2"><a :href="`/business/product/${product.uuid}/update/`">{{product.title}}</a></h2>
          <p>{{product.description}}</p>
        </article>
        <footer class="d-flex justify-content-between align-items-center">
          <span>Price: ${{product.price}}</span>
          <a href="javascript:void(0)" class="btn btn-primary btn-sm"><i class="fas fa-plus"></i> Add to cart</a>
        </footer>
      </section>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import _ from "lodash";

export default {
  name: "ViewAll",
  props: {
    orderBy: {
      type: String
    },
    mediaUrl: {
      type: String,
      default: ""
    },
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
    data_products() {
      if (this.orderBy == 'title') {
        return _.orderBy(this.products, this.orderBy)
      } else if (this.orderBy == 'price') {
        return _.orderBy(this.products, this.orderBy);
      } else {
        return this.products
      }
    }
  },
  methods: {

  }
}
</script>

<style scoped>

</style>
