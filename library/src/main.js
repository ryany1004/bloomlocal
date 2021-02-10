import Vue from 'vue'
import HelloWorld from "@/components/HelloWorld";
import PasswordMeter from "@/components/PasswordMeter";
import {PlaceAutocompleteField} from 'vue-place-autocomplete';
import VuePhoneNumberInput from 'vue-phone-number-input';
import Avatar from 'vue-avatar';
import Switches from 'vue-switches';
import ElementUI from 'element-ui';
import locale from 'element-ui/lib/locale/lang/en';
import 'element-ui/lib/theme-chalk/index.css';
import VueCookies from 'vue-cookies'
import axios from "axios";
import VueAxios from "vue-axios";
import moment from "vue-moment";
import { SidebarPlugin } from 'bootstrap-vue';
import vueCountryRegionSelect from 'vue-country-region-select';
import ReadMore from 'vue-read-more';
import ZoomOnHover from "vue-zoom-on-hover";
import VueSlimScroll from 'vue-slimscroll';


import 'vue-phone-number-input/dist/vue-phone-number-input.css';
import 'bootstrap-vue/dist/bootstrap-vue.css'

axios.defaults.headers.common['X-CSRFToken'] = document.querySelector('[name=csrfmiddlewaretoken]').value;

Vue.use(VueCookies);
Vue.use(ElementUI, {locale});
Vue.use(VueAxios, axios);
Vue.use(moment);
Vue.use(SidebarPlugin);
Vue.use(vueCountryRegionSelect)
Vue.use(ReadMore);
Vue.use(ZoomOnHover);
Vue.use(VueSlimScroll);

// import App from './App.vue'
import './store';
import "./filters";
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
import MultiShops from "./components/shopper/MultiShops";
import ViewAllShop from "./components/shopper/shops/ViewAllShop";
import RecentAddedShop from "./components/shopper/shops/RecentAddedShop";
import CategoryShop from "./components/shopper/shops/CategoryShop";
import BestSellingShop from "./components/shopper/shops/BestSellingShop";
import FollowingLove from "./components/shopper/shops/FollowingLove";
import BestSellingProduct from "./components/shopper/shop/BestSellingProduct";
import CategoryProduct from "./components/shopper/shop/CategoryProduct";
import RecentAddedProduct from "./components/shopper/shop/RecentAddedProduct";
import ViewAllProduct from "./components/shopper/shop/ViewAllProduct";
import ShopCard from "./components/shopper/shops/ShopCard";
import BusinessProductCard from "./components/business/storefront/BusinessProductCard";
import ProductCard from "./components/shopper/shop/ProductCard";
import ShopDetails from "./components/shopper/shop/ShopDetails";
import ProductDetails from "./components/shopper/shop/ProductDetails";
import CartWidget from "./components/shopper/CartWidget";
import BtnAddToCart from "./components/shopper/BtnAddToCart";
import Cart from "./components/shopper/Cart";
import OrderOverview from "./components/shopper/OrderOverview";
import OrderSuccess from "./components/shopper/OrderSuccess";
import MyShops from "./components/shopper/account/MyShops";
import MyPurchase from "./components/shopper/account/MyPurchase";
import MyCollections from "./components/shopper/account/MyCollections";
import OrderCanceled from "./components/shopper/OrderCanceled";
import Wishlist from "./components/shopper/shop/Wishlist";
import SearchBar from "./components/shopper/SearchBar";
import SearchPage from "./components/shopper/SearchPage";
import MyOrders from "./components/business/orders/MyOrders";
import ProductsImport from "./components/business/ProductsImport";
import ShopifyProductCard from "./components/business/ShopifyProductCard";
import ShopifyProductEdit from "@/components/business/ShopifyProductEdit";
import Receipt from "@/components/business/orders/Receipt";
import ShopperInfo from "@/components/business/orders/ShopperInfo";
import Dashboard from "@/components/business/dashboard/Dashboard";
import ProductsUpload from "@/components/business/ProductsUpload";
import ProductsFileImport from "@/components/business/ProductsFileImport";
import InternationalPhoneInput from "@/components/common/InternationalPhoneInput";

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
    BusinessProductCard,
    RecentAdded,
    BestSelling,
    ViewAll,
    StorefrontCategory,
    MultiShops,
    ShopCard,
    BestSellingShop,
    CategoryShop,
    RecentAddedShop,
    ViewAllShop,
    FollowingLove,
    ShopDetails,
    BestSellingProduct,
    CategoryProduct,
    RecentAddedProduct,
    ViewAllProduct,
    ProductCard,
    ProductDetails,
    CartWidget,
    BtnAddToCart,
    Cart,
    OrderOverview,
    OrderSuccess,
    OrderCanceled,
    MyShops,
    MyPurchase,
    MyCollections,
    Wishlist,
    SearchBar,
    SearchPage,
    MyOrders,
    ProductsImport,
    ShopifyProductCard,
    ShopifyProductEdit,
    Receipt,
    ShopperInfo,
    Dashboard,
    ProductsUpload,
    ProductsFileImport,
    InternationalPhoneInput
}
Object.keys(Components).forEach(name => {
    // console.info('name: '+ name);
    Vue.component(name,Components[name])
})
// Vue.config.devtools = true;
export default Components

// new Vue({
//   store,
//   render: h => h(App)
// }).$mount('#app')
