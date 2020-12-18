<template>
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
      <a href="javascript:void(0)" @click="toggleActive(product)"><i class="fas" :class="{'fa-eye': product.status == 1, 'fa-eye-slash': product.status == 0}"></i></a>
    </footer>
  </section>
</template>

<script>
import axios from "axios";

export default {
  name: "BusinessProductCard",
  props: {
    product: {
      type: Object,
      required: true
    },
    mediaUrl: {
      type: String,
      default: ""
    },
  },
  methods: {
    toggleActive(product) {
      let msg = `Do you want to ${product.status == 0 ? "disable" : "enable"} this product`;
      if (confirm(msg)) {
        let data = {
          status: product.status == 0 ? 1 : 0
        }
        axios.patch(`/api/shop/product/${product.uuid}/`, data).then(function (res) {
          product.status = res.data.status;
        }).catch(function (err) {
          console.log(err);
        })
      }
    },
  }
}
</script>

<style scoped>

</style>
