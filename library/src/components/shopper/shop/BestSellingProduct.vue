<template>
  <div>
    No data
  </div>
</template>

<script>
export default {
  name: "BestSellingProduct",
  props: {
    shopId: {
      type: Number,
      required: true
    },
    orderBy: {
      type: String
    },
    mediaUrl: {
      type: String,
      default: ""
    }
  },
  data: function () {
    return {

    }
  },
  computed: {

  },
  created() {
  },
  methods: {

  }
}
</script>

<style scoped>

</style>
