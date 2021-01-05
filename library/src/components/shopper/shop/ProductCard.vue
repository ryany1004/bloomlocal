<template>
  <section class="product-card">
    <a :href="product.url">
      <div class="card-image" :style="{backgroundImage: `url('${mediaUrl}${product.thumbnail}')`}">
      </div>
    </a>
    <article class="position-relative">
      <h2 :title="product.title" class="mt-2 pr-4"><a :href="product.url">{{product.title}}</a></h2>
      <wishlist :product="product" class="wishlist"></wishlist>
      <p>{{product.description}}</p>
    </article>
    <footer class="d-flex justify-content-between align-items-center">
      <span>Price: ${{product.price}}</span>
      <btn-add-to-cart :product="product"></btn-add-to-cart>
    </footer>
  </section>
</template>

<script>
export default {
  name: "ProductCard",
  props: {
    product: {
      type: Object,
      required: true
    },
    mediaUrl: {
      type: String,
      default: ""
    },
  }
}
</script>

<style lang="scss">
.product-card {
  .wishlist {
    position: absolute;
    right: 5px;
    top: 10px;
  }
}
</style>
