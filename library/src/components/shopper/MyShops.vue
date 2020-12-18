<template>
  <div>
    <div v-if="shop_empty">
      You don't have any shops here
    </div>
  </div>
</template>

<script>
export default {
  name: "MyShops",
  props: {
    mediaUrl: {
      type: String,
      default: ""
    }
  },
  data: function () {
    return {
      followed_shops: [],
      recent_viewed_shops: [],
      similar_shops: []
    }
  },
  computed: {
    shop_empty() {
      return this.followed_shops.length == 0 && this.recent_viewed_shops.length == 0 && this.similar_shops.length == 0;
    }
  },
  methods: {

  }
}
</script>

<style scoped>

</style>
