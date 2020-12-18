import Vue from 'vue'
import Vuex from 'vuex'
import axios from "axios"

Vue.use(Vuex)

const vStore = new Vuex.Store({
  state: {
    colors: [],
    sizes: [],
    categories: [],
    product: {},
    shop_categories: [],
    user: {},
    isLoggedIn: false,
    cart_items: []
  },
  getters: {
    colors: state => {
      return state.colors
    },
    sizes:state => {
      return state.sizes
    },
    shopCategories: state => {
      return state.shop_categories;
    }
  },
  mutations: {
    setColors(state, colors) {
      state.colors = colors
    },
    setSizes(state, sizes) {
      state.sizes = sizes
    },
    setCategories(state, categories) {
      state.categories = categories;
    },
    setShopCategories(state, categories) {
      state.shop_categories = categories;
    },
    setProduct(state, product) {
      state.product = product;
    },
    setUser(state, user) {
      state.user = user;
      if (user.id) {
        state.isLoggedIn = true;
      }
    },
    setCart(state, products) {
      state.cart_items = products;
    }
  },
  actions: {
    get_colors(context) {
      if (context.state.colors.length == 0) {
        axios.get('/api/product/attribute/color/').then((res) => {
          context.commit('setColors', res.data);
        })
      }
    },
    get_sizes(context) {
      if (context.state.sizes.length == 0) {
        axios.get('/api/product/attribute/size/').then((res) => {
          context.commit('setSizes', res.data);
        })
      }
    },
    get_categories(context) {
      axios.get('/api/product/categories/').then((res) => {
        context.commit('setCategories', res.data);
      })
    },
    get_shop_categories(context) {
      axios.get('/api/shop/categories/').then((res) => {
        context.commit('setShopCategories', res.data);
      })
    },
    get_product(context, uuid) {
      return axios.get(`/api/shop/product/${uuid}/`).then((res) => {
        context.commit('setProduct', res.data);
      })
    },
    get_user(context) {
      return axios.get('/api/users/me/').then((res) => {
        context.commit('setUser', res.data);
      }).catch((err) => {
        console.log(err)
        context.commit('setUser', {});
      })
    },
    set_user(context, user) {
      context.commit("setUser", user);
    },
    add_recent_viewed_shop(context, shop_id) {
      axios.post(`/api/user/shop/${shop_id}/recent-viewed/`).then(() => {
      }).catch((err) => {
        console.log(err)
      })
    },
    add_to_cart(context, data) {
      return axios.post(`/api/order/cart/item/add/`, data).then((res) => {
        context.commit("setCart", res.data);
      }).catch((err) => {
        alert("Unable add to cart! Please try again.");
        console.log(err)
      })
    },
    remove_item_cart(context, data) {
      return axios.post(`/api/order/cart/item/remove/`, data).then((res) => {
        context.commit("setCart", res.data);
      }).catch((err) => {
        alert("Unable remove to cart! Please try again.");
        console.log(err)
      })
    },
    get_cart(context) {
      return axios.get(`/api/order/cart/`).then((res) => {
        context.commit("setCart", res.data);
      }).catch((err) => {
        console.log(err)
      })
    }
  },
  modules: {
  }
})

Vue.prototype.$store = vStore;
window.vStore = vStore;
export default vStore
