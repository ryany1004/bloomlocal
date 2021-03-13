<template>
  <div class="row">
    <div class="col-3 my-5" v-for="product in products" :key="product.id">
      <store-product-card :product="product" :media-url="mediaUrl"></store-product-card>
    </div>
  </div>
</template>

<script>
import StoreProductCard from "@/components/business/products/StoreProductCard";


export default {
  name: "CardProducts",
  components: {StoreProductCard},
  props: {
    mediaUrl: {
      type: String,
      default: ""
    },
    products: {
      type: Object,
      default: () => []
    }
  },
}
</script>

<style scoped>

</style>
