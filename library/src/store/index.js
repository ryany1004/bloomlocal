import Vue from 'vue'
import Vuex from 'vuex'
import axios from "axios"

Vue.use(Vuex)

const vStore = new Vuex.Store({
  state: {
    colors: [],
    sizes: []
  },
  getters: {
    colors: state => {
      return state.colors
    },
    sizes:state => {
      return state.sizes
    }
  },
  mutations: {
    setColors(state, colors) {
      state.colors = colors
    },
    setSizes(state, sizes) {
      state.sizes = sizes
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
    }
  },
  modules: {
  }
})

Vue.prototype.$store = vStore;
window.vStore = vStore;
export default vStore
