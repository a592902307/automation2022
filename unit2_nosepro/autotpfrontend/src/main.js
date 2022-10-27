import { createApp, createVNode } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import ElementPlus from 'element-plus'  // 引入element plus组件库
import 'element-plus/dist/index.css'    // 引入element plus样式表
import * as ElementPlusIconsVue from '@element-plus/icons-vue' // 引入element plus图标表

const app=createApp(App);
app.use(store).use(router)
app.use(ElementPlus)
// 对所有图标进行注册
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
  }
app.mount('#app')

const SvgIcon=(props) => {
  const {icon='Seting'} = props  // 解构赋值，如果传入icon="Location" 就用传入的，没传就默认用Seting
  return createVNode(ElementPlusIconsVue[icon]) // createVNode:创建dom节点  ElementPlusIconsVue[icon]通过icon获取图标组件
}
app.component('SvgIcon',SvgIcon) // 注册组件，命名