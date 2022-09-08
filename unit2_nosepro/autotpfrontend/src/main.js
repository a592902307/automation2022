import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import ElementPlus from 'element-plus'  // 引入element plus组件库
import 'element-plus/dist/index.css'    // 引入element plus样式表

const app=createApp(App);
app.use(store).use(router)
app.use(ElementPlus)
app.mount('#app')
