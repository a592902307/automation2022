<template>
    <el-container>
        <!-- 页面布局组件留出并定义具名插槽 -->
        <el-header> <slot name="header"></slot> </el-header>
        <el-container>
            <el-aside width="150px"> <slot name="aside"></slot> </el-aside>
            <el-main> <slot name="main"></slot> </el-main>
        </el-container>
    </el-container>
</template>

<script>
    // 页面布局组件
    export default {
        name: 'Layout'
    }
</script>


<style>
    body {
        margin: 0px !important;
    }
    .el-header {
        padding:0px !important;
    }
    .el-header ,
    .el-footer {
      background-color: #b3c0d1;
      color: var(--el-text-color-primary);
      text-align: center;
      line-height: 60px;
    }
    .el-aside {
      background-color: #e9eef3;
      color: var(--el-text-color-primary);
      text-align: center;
      line-height: 200px;
    }
    .el-main {
      background-color: #e9eef3;
      color: var(--el-text-color-primary);
      text-align: center;
      line-height: 160px;
    }
    body > .el-container {
      margin-bottom: 40px;
    }
</style>