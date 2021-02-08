<template>
  <section class="import-product-card">
    <input type="checkbox" v-model="product.checked" :checked="product.checked" class="select-product"/>
    <a href="javascript:void(0)" @click="clickProduct(product)" style="z-index: 0">
      <div class="card-image" :style="{backgroundImage: `url('${product_image}')`}">
      </div>
    </a>
    <article>
      <h2 :title="product.title" class="mt-2"><a href="javascript:void(0)">{{product.title}}</a></h2>
<!--      <p>{{product.description}}</p>-->
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
  .import-product-card {
    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.12);
    border-radius: 10px;
    padding: 6px;
    background-color: #fff;
    position: relative;
    z-index: 0;
    .select-product {
      position: absolute;
      top: 15px;
      right: 15px;
      z-index: 1;
    }

    .card-image {
      height: 153px;
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
      height: 43px;
      line-height: 14px;
      overflow: hidden;
      display: -webkit-box;
      -webkit-line-clamp: 3;
      -webkit-box-orient: vertical;
      white-space: normal;
      font-size: 12px;
      font-weight: bolder;
      a {
        font-size: 12px;
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
      font-size: 14px;
      font-weight: bolder;
      a {
        font-size: 14px;
      }
    }
  }
</style>
