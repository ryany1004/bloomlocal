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
    cart_items: [],
    cartLoading: false,


    tags: [
      {id:1, name:'tshirts'},
      {id:2, name:'Jeans'},
      {id:3, name:'Bottoms'},
      {id:4, name:'Shoes'},
      {id:5, name:'Men'},
      {id:6, name:'Women'}
    ],
    storeType: [
      {id:1, name: 'Store 1'},
      {id:2, name: 'Store 2'}
    ],
    isSignup: true,
    isSignUpSteps: false,
    signupSteps: 1,
    forms: {
      signUpFields: {},
      storeInfo: {},
      contactDetail: {}
    }
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
    },

    getTags: state=>{
      return state.tags;
    },
    getStoreType: state =>{
      return state.storeType;
    },
    isSignupForm: state => {
      return state.isSignup;
    },
    isformSteps: state => {
      return state.isSignUpSteps
    },
    formSteps: state => {
      return state.signupSteps
    },
    signUpFormFields: state => {
      return state.forms.signUpFields;
    },
    getStoreInfo: state => {
      return state.forms.storeInfo;
    },
    getContactDetail: state => {
      return state.forms.contactDetail;
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
    },
    setCartLoading(state, loading) {
      state.cartLoading = loading
    },


    signupformSteps(state, payload) {
      if(payload == 'signup') {
        state.isSignup = true;
        state.isSignUpSteps = false
      } else if(payload == 'steps'){
        state.isSignup = false;
        state.isSignUpSteps = true;
      }
    },
    steps(state, payload) {
      state.signupSteps = payload
    },
    signupFormFields( state, payload) {
      state.forms.signUpFields = payload;
    },
    storeInfoFields( state, payload) {
      state.forms.storeInfo = payload
    },
    contactDetail( state, payload) {
      state.forms.contactDetail = payload
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
      context.commit("setCartLoading", true);
      return axios.get(`/api/order/cart/`).then((res) => {
        context.commit("setCart", res.data);
        context.commit("setCartLoading", false);
      }).catch((err) => {
        console.log(err)
      })
    },
    strip_connect() {
      return axios.post('/users/stripe/connect/')
    },

    nextStep(context, payload) {
      context.commit('signupformSteps', payload);
    },
    nextProcess( context, payload) {
      context.commit('steps', payload);
    },
    singUpFormField( context, payload) {
      context.commit('signupFormFields', payload);
    },
    storeInfoFields (context, payload) {
      context.commit('storeInfoFields', payload);
    },
    contactDetail (context, payload) {
      context.commit('contactDetail', payload);
    }
  },
  modules: {
  }
})

Vue.prototype.$store = vStore;
window.vStore = vStore;
export default vStore
