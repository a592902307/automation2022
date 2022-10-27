import { createRouter, createWebHashHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import Login from '../views/Login.vue'

const routes = [
  {
    path: '/', //一级路由
    name: 'home',
    component: HomeView,
    meta:{
      title:'首页'
    },
    children:[ //子路由，这里的路由组件会显示到当前父组件的router-view中，开头不需要加/
      {
        path:'cases',
        component: ()=>import("../pages/Cases.vue"),
        meta:{ //存放自定义数据
          title:'测试用例',
          icon:'Location'
        }
      },
      {
        path:'requests',
        component: ()=>import("../pages/Request.vue"),
        meta:{
          title:'web接口',
          icon:'Clock'
        }
      },
      {
        path:'plans',
        component: ()=>import("../pages/Plans.vue"),
        meta:{
          title:'测试计划',
          icon:'Document'
        }
      },
      {
        path:'reports',
        component: ()=>import("../pages/Reports.vue"),
        meta:{
          title:'测试报告',
          icon:'Notebook'
        }
      }
    ]
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  },
  {
    path:'/login',
    name:'login',
    component: Login
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

// 全局前置路由守卫
router.beforeEach((to,from,next)=>{
  // 控制要访问的路由，如果访问的不是login且没有登录，就重定向到login
  if (to.name !== 'login' && localStorage.getItem('islogin') !== 'yes'){
    console.log('未登录')
    // return '/about' // 重定向到'/about'，跳到about页面会再次触发路由守卫
    next({name:'login'})
  }
  else{
    if(to.name != 'login'){
      console.log('已登录')
    }else{
      console.log('未登录')
    }
    // next() 表示放行，会继续访问to指向的路径，但是仍然会触发全局守卫
    next()
  }
})

export default router