<template>
  <section class="product-card">
    <a href="javascript:void(0)">
      <div class="card-image" :style="{backgroundImage: `url('${mediaUrl}${product.thumbnail}')`}">
      </div>
    </a>
    <article>
      <h2 :title="product.title" class="mt-2"><a href="javascript:void(0)">{{product.title}}</a></h2>
      <p>{{product.description}}</p>
    </article>
    <footer class="d-flex justify-content-between align-items-center">
      <span>Price: ${{product.price}}</span>
      <a href="javascript:void(0)" class="btn btn-primary btn-sm"><i class="fas fa-plus"></i> Add to cart</a>
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
