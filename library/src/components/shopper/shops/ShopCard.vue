<template>
  <section class="shop-card">
    <a :href="`/shop/${shop.slug}/`">
      <div class="card-image" :style="{backgroundImage: `url('${mediaUrl}${shop.logo}')`}">
      </div>
    </a>
    <article class="px-2 mt-2">
      <div class="d-flex">
        <h2 :title="shop.name" class="shop-name flex-grow-1"><a :href="`/shop/${shop.slug}/`">{{shop.name}}</a></h2>
        <following-love :shop="shop"></following-love>
      </div>

      <ul class="list-categories">
        <li v-for="category in shop.category_names" :key="category.id">{{category.name}}</li>
      </ul>
    </article>
    <footer class="px-2 pb-2">
      <ul class="shop-feature">
        <li>Free Delivery</li>
        <li>Christmas Sale</li>
        <li>Custom offers</li>
      </ul>
    </footer>
  </section>
</template>

<script>
export default {
  name: "ShopCard",
  props: {
    shop: {
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
