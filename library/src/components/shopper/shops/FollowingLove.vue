<template>
  <div v-if="isLoggedIn" style="width: 80px" class="d-flex justify-content-end align-items-baseline shop-following">
    <a href="javascript:void(0)" class="font-8 mr-1" @click="toggleFollowing(shop)"
       :class="{'followed': user.following_shops.indexOf(shop.id) != -1}">{{ user.following_shops.indexOf(shop.id) != -1 ? "Following" : "Follow" }}</a>
    <a href="javascript:void(0)" @click="toggleLove(shop)">
      <i class="fa-heart" :class="{'fas': user.love_shops.indexOf(shop.id) != -1,
        'far': user.love_shops.indexOf(shop.id) == -1}" style="font-size: 10px"></i>
    </a>
  </div>
</template>

<script>
import {mapState} from "vuex";
import axios from "axios";

export default {
  name: "FollowingLove",
  props: {
    shop: {
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
    toggleFollowing(shop) {
      let that = this;
      axios.post(`/api/user/shop/${shop.id}/following/`).then((res) => {
        that.$store.dispatch('set_user', res.data);
      })
    },
    toggleLove(shop) {
      let that = this;
      axios.post(`/api/user/shop/${shop.id}/love/`).then((res) => {
        that.$store.dispatch('set_user', res.data);
      })
    }
  }
}
</script>

<style lang="scss">
.shop-following {
  a {
    color: #828282;
    text-decoration: none;
  }
  .followed {
    background: #ED6B5E;
    border-radius: 3px;
    padding: 2px 4px;
    color: #F2F2F2;
  }
}
</style>
