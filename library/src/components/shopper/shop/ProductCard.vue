<template>
  <section class="product-card">
    <a :href="`/product/${product.slug}/`">
      <div class="card-image" :style="{backgroundImage: `url('${mediaUrl}${product.thumbnail}')`}">
      </div>
    </a>
    <article>
      <h2 :title="product.title" class="mt-2"><a :href="`/product/${product.slug}/`">{{product.title}}</a></h2>
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

<style scoped>

</style>
