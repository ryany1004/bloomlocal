import Vue from 'vue'
import HelloWorld from "@/components/HelloWorld";
import PasswordMeter from "@/components/PasswordMeter";
import {PlaceAutocompleteField} from 'vue-place-autocomplete';


// import App from './App.vue'
// import store from './store'

Vue.config.productionTip = false

const Components = {
    HelloWorld,
    PasswordMeter,
    PlaceAutocompleteField
}
Object.keys(Components).forEach(name => {
    console.warn('name: '+ name);
    Vue.component(name,Components[name])
})

export default Components

// new Vue({
//   store,
//   render: h => h(App)
// }).$mount('#app')
