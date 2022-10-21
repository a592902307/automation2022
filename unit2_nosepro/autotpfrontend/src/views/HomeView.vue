<template>
  <Layout>
    <!-- 具名插槽：往指定的插槽塞入指定的组件 v-slot:插槽名称 简写：#插槽名称 -->
    <template v-slot:header>
      <Navbar></Navbar>
    </template>
    <template v-slot:aside>
      <Sidebar></Sidebar>
    </template>
    <template v-slot:main>
      <router-view></router-view>
    </template>
  </Layout>
</template>

<script>
// @ is an alias to /src
// import HelloWorld from '@/components/HelloWorld.vue'
import {logout} from '@/httplib';
import Layout from '../components/Layout.vue';
import Navbar from '../components/Navbar.vue';
import Sidebar from '../components/Sidebar.vue';

export default {
  name: 'HomeView',
  components: {
    // HelloWorld
    Layout,
    Navbar,
    Sidebar
},
  setup(){
    function quit(){
      logout()
    }
    return{
      quit
    }
  }
}
</script>


