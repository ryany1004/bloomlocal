<template>
  <section class="product-card">
    <a :href="product.url" style="z-index: 0">
      <div class="card-image position-relative" :style="{backgroundImage: `url('${mediaUrl}${product.thumbnail}')`}">
        <wishlist :product="product" class="wishlist"></wishlist>
      </div>
    </a>
    <article>
      <h2 :title="product.title" class="mt-2"><a :href="product.url">{{product.title}}</a></h2>

<!--      <p v-if="!hideDescription">{{product.description}}</p>-->
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
    hideDescription: {
      type: Boolean,
      default: false
    }
  }
}
</script>

<style lang="scss">
.product-card {
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.12);
  border-radius: 10px;
  padding: 15px;
  background-color: #fff;

  .wishlist {
    position: absolute;
    right: 5px;
    top: 10px;
    z-index: 10;
  }

  .card-image {
    height: 230px;
    width: 100%;
    background-size: contain;
    background-position: center;
    background-repeat: no-repeat;
    border: 1px solid #f8f8f8;
    border-top-right-radius: 10px;
    border-top-left-radius: 10px;
    position: relative;
    .select-product {
      position: absolute;
      right: 10px;
      top: 10px;
    }
  }
  h2 {
    height: 56px;
    overflow: hidden;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    white-space: normal;
    font-size: 16px;
    font-weight: bolder;
    a {
      font-size: 14px;
      color: #0C242E;
    }
  }
  p {
    font-size: 11px;
    height: 43px;
    overflow: hidden;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    margin-bottom: 0.5rem;
  }
  footer {
    font-size: 14px;
    font-weight: bolder;
    a {
      font-size: 14px;
    }
  }
}
</style>
