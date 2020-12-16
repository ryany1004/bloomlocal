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
    isLoggedIn: false
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
    }
  },
  actions: {
    get_colors(context) {
      axios.get('/api/product/attribute/color/').then((res) => {
        context.commit('setColors', res.data);
      })
    },
    get_sizes(context) {
      axios.get('/api/product/attribute/size/').then((res) => {
        context.commit('setSizes', res.data);
      })
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
      axios.get('/api/users/me/').then((res) => {
        context.commit('setUser', res.data);
      }).catch((err) => {
        console.log(err)
        context.commit('setUser', {});
      })
    },
    set_user(context, user) {
      context.commit("setUser", user);
    }
  },
  modules: {
  }
})

Vue.prototype.$store = vStore;
window.vStore = vStore;
export default vStore
