import Vue from 'vue'
import HelloWorld from "@/components/HelloWorld";
import PasswordMeter from "@/components/PasswordMeter";
import {PlaceAutocompleteField} from 'vue-place-autocomplete';
import VuePhoneNumberInput from 'vue-phone-number-input';
import 'vue-phone-number-input/dist/vue-phone-number-input.css';
import Avatar from 'vue-avatar';
import Switches from 'vue-switches';
import ElementUI from 'element-ui';
import locale from 'element-ui/lib/locale/lang/en';
import 'element-ui/lib/theme-chalk/index.css';
import VueCookies from 'vue-cookies'
import axios from "axios";
import VueAxios from "vue-axios";
import moment from "vue-moment";

axios.defaults.headers.common['X-CSRFToken'] = document.querySelector('[name=csrfmiddlewaretoken]').value;

Vue.use(VueCookies);
Vue.use(ElementUI, {locale});
Vue.use(VueAxios, axios);
Vue.use(moment);

// import App from './App.vue'
import './store';
import ProductAdd from "./components/business/ProductAdd";
import Products from "./components/business/Products";
import ProductConfirmUpload from "./components/business/ProductConfirmUpload";
import ProductUpdate from "./components/business/ProductUpdate";
import ProductInventory from "./components/business/ProductInventory";
import MyStorefront from "./components/business/MyStorefront";
import RecentAdded from "./components/business/storefront/RecentAdded";
import BestSelling from "./components/business/storefront/BestSelling";
import ViewAll from "./components/business/storefront/ViewAll";
import StorefrontCategory from "./components/business/storefront/StorefrontCategory";
import MyShops from "./components/shopper/MyShops";
import ViewAllShop from "./components/shopper/shops/ViewAllShop";
import RecentAddedShop from "./components/shopper/shops/RecentAddedShop";
import CategoryShop from "./components/shopper/shops/CategoryShop";
import BestSellingShop from "./components/shopper/shops/BestSellingShop";
import FollowingLove from "./components/shopper/shops/FollowingLove";

Vue.config.productionTip = false

const Components = {
    HelloWorld,
    PasswordMeter,
    PlaceAutocompleteField,
    VuePhoneNumberInput,
    Avatar,
    Switches,
    ProductAdd,
    Products,
    ProductConfirmUpload,
    ProductUpdate,
    ProductInventory,
    MyStorefront,
    RecentAdded,
    BestSelling,
    ViewAll,
    StorefrontCategory,
    MyShops,
    BestSellingShop,
    CategoryShop,
    RecentAddedShop,
    ViewAllShop,
    FollowingLove
}
Object.keys(Components).forEach(name => {
    console.info('name: '+ name);
    Vue.component(name,Components[name])
})

export default Components

// new Vue({
//   store,
//   render: h => h(App)
// }).$mount('#app')
