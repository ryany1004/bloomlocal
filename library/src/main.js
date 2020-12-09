import Vue from 'vue'
import HelloWorld from "@/components/HelloWorld";
import PasswordMeter from "@/components/PasswordMeter";
import {PlaceAutocompleteField} from 'vue-place-autocomplete';
import VuePhoneNumberInput from 'vue-phone-number-input';
import 'vue-phone-number-input/dist/vue-phone-number-input.css';
import Avatar from 'vue-avatar';
import Switches from 'vue-switches';
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import VueCookies from 'vue-cookies'
import axios from "axios";
import VueAxios from "vue-axios";

axios.defaults.headers.common['X-CSRFToken'] = document.querySelector('[name=csrfmiddlewaretoken]').value;
Vue.use(VueCookies)
Vue.use(ElementUI);
Vue.use(VueAxios, axios)
// import App from './App.vue'
import './store';
import ProductAdd from "./components/business/ProductAdd";
import Storefront from "./components/business/Storefront";
import ProductCofirmUpload from "./components/business/ProductCofirmUpload";

Vue.config.productionTip = false

const Components = {
    HelloWorld,
    PasswordMeter,
    PlaceAutocompleteField,
    VuePhoneNumberInput,
    Avatar,
    Switches,
    ProductAdd,
    Storefront,
    ProductCofirmUpload
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
