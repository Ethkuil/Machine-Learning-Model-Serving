// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
Vue.config.productionTip = false

import router from './router'

import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
Vue.use(ElementUI)

import axios from 'axios'
axios.defaults.baseURL = 'http://localhost:8000/'; // Flask API URL
Vue.prototype.$axios = axios // 将axios挂载到Vue的原型上，这样所有组件都可以使用this.$axios访问axios

import JSONView from 'vue-json-viewer'
Vue.use(JSONView)

import App from './App'
/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
