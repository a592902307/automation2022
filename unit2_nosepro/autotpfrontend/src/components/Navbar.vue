<template>
    <div class="logo">
      <el-icon><ChromeFilled /></el-icon>
      TESTSQ
    </div>
    <!-- :ellipsis="false" 解决tab栏中出现省略号的问题 -->
    <el-menu
      class="navbar"
      mode="horizontal"
      background-color="#545c64"
      text-color="#fff"
      active-text-color="#ffd04b"
      :ellipsis="false" 
    >
      <!-- <el-menu-item index="1">Processing Center</el-menu-item>
      <el-sub-menu index="2">
        <template #title>Workspace</template>
        <el-menu-item index="2-1">item one</el-menu-item>
        <el-menu-item index="2-2">item two</el-menu-item>
        <el-menu-item index="2-3">item three</el-menu-item>
        <el-sub-menu index="2-4">
          <template #title>item four</template>
          <el-menu-item index="2-4-1">item one</el-menu-item>
          <el-menu-item index="2-4-2">item two</el-menu-item>
          <el-menu-item index="2-4-3">item three</el-menu-item>
        </el-sub-menu>
      </el-sub-menu>
      <el-menu-item index="3" disabled>Info</el-menu-item>
      <el-menu-item index="4" >Orders</el-menu-item>
      <div class="flex-grow" /> -->
      
      <!-- <el-sub-menu id="avatar" index="5">
        <template #title>
          <el-avatar :size="size" :src="circleUrl"></el-avatar>
        </template>
        <el-menu-item index="2-1"> <el-icon><Setting /></el-icon> 设置</el-menu-item>
        <el-menu-item index="2-2" @click="quit"> <el-icon><Edit /></el-icon> 退出</el-menu-item>
      </el-sub-menu> -->

      <!-- 设置一个div元素并设置它的flex-grow属性 来弹性占用父元素的剩余空间（按比列自适应） -->
      <div class="flex-grow" />
      <el-menu-item id="avatar2">
        <el-dropdown>
          <span class="el-dropdown-link">
            <el-avatar :size="size" :src="circleUrl"></el-avatar>
            <el-icon class="el-icon--right">
              <arrow-down />
            </el-icon>
          </span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item > <el-icon><Setting /></el-icon> 设置</el-dropdown-item>
              <el-dropdown-item @click="quit"> <el-icon><Edit /></el-icon> 退出</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>  
      </el-menu-item>

    </el-menu>
</template>
  
<script>
  import {logout} from '@/httplib';
  export default {
      setup(){
        function quit(){
          logout()
        }
        return {
            size:32,
            circleUrl:'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png',
            quit
        }
      }
  }
</script>

<style>
  .navbar{
    text-align: center;
  }
  .logo{
    width: 150px;
    background-color: rgb(255, 208, 75);
    /* 浮动 */
    float: left; 
  }
  .flex-grow{
    flex-grow: 1;
  }
  #avatar2{
    width: 96px;
    height: 60px;
    text-align: center;
  }
  .el-dropdown-link{
    cursor: pointer;
    color: var(--el-color-primary);
    display: flex;
    align-items: center;
  }
</style>