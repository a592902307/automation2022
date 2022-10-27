<!-- eslint-disable vue/valid-v-for -->
<template>
  <el-breadcrumb separator="/">
    <el-breadcrumb-item v-for="route in currentRouteList" :to="{ path: route.path }">{{route.meta.title}}</el-breadcrumb-item>
    <!-- <el-breadcrumb-item> <a href="/">promotion management</a> </el-breadcrumb-item> -->
    <!-- <el-breadcrumb-item>promotion list</el-breadcrumb-item>
    <el-breadcrumb-item>promotion detail</el-breadcrumb-item> -->
  </el-breadcrumb>
</template>

<script>
    import { useRoute } from 'vue-router';
    export default{
        setup(){
            // 获取当前路由信息
            const route = useRoute();
            console.log(route.matched);
            const currentRouteList = route.matched; // 当前路由列表(包括所有上级路由)
            return{
                currentRouteList
            }
        }
    }
</script>