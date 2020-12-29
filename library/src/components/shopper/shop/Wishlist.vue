<template>
  <a v-if="isLoggedIn" href="javascript:void(0)" @click="toggleWishlist()">
      <i class="fa-heart" :class="{'fas': user.wishlist_products.indexOf(product.id) != -1,
        'far': user.wishlist_products.indexOf(product.id) == -1}" style="font-size: 10px"></i>
  </a>
</template>

<script>
import {mapState} from "vuex";
import axios from "axios";

export default {
  name: "Wishlist",
  props: {
    product: {
      required: true,
      type: Object
    }
  },
  computed: {
    ...mapState([
        'isLoggedIn', 'user'
    ]),
  },
  methods: {
    toggleWishlist() {
      let that = this;
      axios.post(`/api/user/product/${this.product.id}/wishlist/`).then((res) => {
        that.$store.dispatch('set_user', res.data);
      })
    },
  }
}
</script>

<style scoped>
.fa-heart.fas {
  color: #ED6B5E;
}
</style>
