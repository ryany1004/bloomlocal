<template>
  <div class="products">
    <product-inventory v-if="view_mode == 'inventory'" :view-mode="view_mode" :media-url="mediaUrl" @changeViewMode="changeViewMode"></product-inventory>
    <my-storefront v-if="view_mode == 'storefront'" :view-mode="view_mode" :media-url="mediaUrl" @changeViewMode="changeViewMode"></my-storefront>
  </div>
</template>

<script>
export default {
  name: "Products",
  props: {
    mediaUrl: {
      type: String,
      default: ""
    },
  },
  data: function () {
    return {
      view_mode: 'storefront'
    }
  },
  created() {
    let view_mode = localStorage.getItem('view_mode');
    if (['storefront', 'inventory'].indexOf(view_mode) != -1) {
      this.view_mode = view_mode;
    } else {
      this.view_mode = 'storefront';
    }
  },
  methods: {
    changeViewMode(mode) {
      this.view_mode = mode;
      localStorage.setItem('view_mode', mode);
    }
  }
}
</script>

<style lang="scss">
</style>
