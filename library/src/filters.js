import Vue from "vue";
import numeral from "numeral";

Vue.filter('numFormat', (val, format = '0,0') => numeral(val).format(format));
