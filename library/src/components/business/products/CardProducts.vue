<template>
  <div>

  </div>
</template>

<script>
export default {
  name: "CardProducts",
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
