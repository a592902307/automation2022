<!-- eslint-disable vue/valid-v-for -->
<template>
    <el-menu-item v-bind:index="item.path" :key="index" v-for="(item,index) in routes">
        <!-- <el-icon>{{item.meta.icon}}</el-icon> -->
        <el-icon>
            <SvgIcon :icon="item.meta.icon" />
        </el-icon>
        <span>{{item.meta.title}}</span>
    </el-menu-item>
</template>

<script>
    export default {
        name:'SidebarItem',
        props:{
            routes:Array // 接收父组件的传参，指定为Array类型
        }
    }
</script>
