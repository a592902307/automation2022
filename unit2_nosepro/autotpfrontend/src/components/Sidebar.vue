<!-- eslint-disable vue/valid-v-for -->
<template>
    <!-- :collapse水平折叠收起菜单 绑定一个状态，为true时折叠  
        :unique-opened是否只保持一个子菜单的展开 
        router:启用vue-router模式,以 index 作为 path 进行路由跳转
    -->
    <el-menu
        router
        :unique-opened="true"
        :collapse="iscollapse"
        active-text-color="#ffd04b"
        background-color="#545c64"
        class="sidebar"
        default-active="2"
        text-color="#fff"
    >
        <!-- <el-sub-menu>
            <template #title>
                <el-icon><location /></el-icon>
                <span>测试用例</span>
            </template>
            <el-menu-item-group title="Group One">
                <el-menu-item index="/cases">item one</el-menu-item>
                <el-menu-item >item two</el-menu-item>
            </el-menu-item-group>
            <el-menu-item-group title="Group Two">
                <el-menu-item >item three</el-menu-item>
            </el-menu-item-group>
            <el-sub-menu >
                <template #title>item four</template>
                <el-menu-item >item one</el-menu-item>
            </el-sub-menu>
        </el-sub-menu>
        <el-menu-item index="/requests">
            <el-icon><Clock /></el-icon>
            <span>web接口</span>
        </el-menu-item>
        <el-menu-item index="/plans" >
            <el-icon><document /></el-icon>
            <span>测试计划</span>
        </el-menu-item>
        <el-menu-item index="/reports">
            <el-icon><Notebook /></el-icon>
            <span>测试报告</span>
        </el-menu-item> -->

        <SidebarItem v-bind:routes="route_list"></SidebarItem>

        <el-menu-item v-on:click="switch_side" class="toggle-button" index="">
            <el-icon v-if="iscollapse===false"><Expand /></el-icon>
            <el-icon v-else><Fold /></el-icon>
        </el-menu-item>
    </el-menu>
</template>

<script>
    import {ref} from 'vue';
    import { useRouter } from 'vue-router';
    import SidebarItem from './common/SidebarItem.vue';
    export default{
    // eslint-disable-next-line vue/multi-word-component-names
        name: "Sidebar",
        components:{
            SidebarItem
        },
        setup() {
            const userouter = useRouter(); // 路由器
            const route_list = userouter.options.routes[0].children; //从home获取二级路由列表
            console.log(route_list[0].meta);
            const iscollapse = ref(false); // 侧边栏状态
            function switch_side() {
                iscollapse.value = !iscollapse.value;
            }
            return {
                iscollapse,
                switch_side,
                route_list
            };
        }
    }
</script>

<style>
    .sidebar {
        /* 撑起菜单栏高度 */
        height: 100vh;
    }
</style>