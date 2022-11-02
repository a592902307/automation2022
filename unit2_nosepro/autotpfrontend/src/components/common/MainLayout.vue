<!-- 主页面布局 面包屑+表格+分页 -->
<template>
    <el-row justify="center">
        <el-col :span="24"> <BreadCrumb> </BreadCrumb></el-col>
    </el-row>
    <el-row>
        <el-col :span="24"> <Tables :columns="columns" :tableData="tableData"></Tables> </el-col>
        <el-col> <PagInator></PagInator> </el-col>
    </el-row>
    <!-- <el-row>
        <el-col :span="12"><div class="grid-content ep-bg-purple" /></el-col>
        <el-col :span="12"><div class="grid-content ep-bg-purple-light" /></el-col>
    </el-row> -->
</template>

<script>
    import BreadCrumb from './BreadCrumb.vue';
    import Tables from './Tables.vue'; 
    import PagInator from './PagInator.vue';
    export default {
        name:'MainLayout',
        components:{
            BreadCrumb,
            Tables,
            PagInator
        },
        props:{
            columns:Array,
            tableData:Object
        }
    }
</script>

<style lang="scss">
    .el-row {
        margin-bottom: 20px;
    }
    .el-row:last-child {
        margin-bottom: 0;
    }
    .el-col {
        border-radius: 4px;
    }
    .ep-bg-purple-dark {
        background: #99a9bf;
    }
    .ep-bg-purple {
        background: #d3dce6;
    }
    .ep-bg-purple-light {
        background: #e5e9f2;
    }
    .grid-content {
        border-radius: 4px;
        min-height: 36px;
    }
    .row-bg {
        padding: 10px 0;
        background-color: #f9fafc;
    }
</style>