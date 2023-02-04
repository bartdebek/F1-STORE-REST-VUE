import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios'

axios.defaults.baseURL = 'https://f1-store.herokuapp.com/api/v1/'

createApp(App).use(store).use(router).mount('#app')
