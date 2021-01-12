<template>
  <section class="product-card">
    <input type="checkbox" v-model="product.checked" :checked="product.checked" class="select-product"/>
    <a href="javascript:void(0)" @click="clickProduct(product)" style="z-index: 0">
      <div class="card-image" :style="{backgroundImage: `url('${product_image}')`}">
      </div>
    </a>
    <article>
      <h2 :title="product.title" class="mt-2"><a href="javascript:void(0)">{{product.title}}</a></h2>
      <p>{{product.description}}</p>
    </article>
    <footer class="d-flex">
      <span>Price: ${{product.price}}</span>
    </footer>
  </section>
</template>

<script>
export default {
  name: "ShopifyProductCard",
  props: {
    product: {
      type: Object,
      required: true
    },
    handleClick: {
      type: Function,
      required: true
    }
  },
  computed: {
    product_image() {
      if (this.product.thumbnail) {
        return this.product.thumbnail;
      }
      return require("../../assets/sample-image.jpg");
    }
  },
  methods: {
    clickProduct(product) {
      this.handleClick(product);
    }
  }
}
</script>

<style scoped lang="scss">
  .product-card {
    position: relative;
    z-index: 0;
    .select-product {
      position: absolute;
      top: 15px;
      right: 15px;
      z-index: 1;
    }
  }
</style>
