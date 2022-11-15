<template>
  <MainLayout :columns="columns" :tableData="tableData" v-if="$route.path==='/plans'"></MainLayout>
  <router-view v-else></router-view>
</template>

<script>
  import MainLayout from '../components/common/MainLayout.vue';
  import { ref,onMounted,provide } from 'vue';
  import { getPlans } from '@/httplib';
  export default {
    components:{
      MainLayout,
    },
    setup(){
      const columns=[
        {
            title: '计划名称',
            field: 'name',
        },
        {
            title: '项目',
            field: 'environment.project.name',
        },
        {
            title: '测试人员',
            field: 'executor.username',
        },
        {
            title: '测试环境',
            field: 'environment.desc' 
        },
        {
            title: '状态',
            field: 'status' 
        },
        {
            title: '执行次数',
            field: 'exec_counts' 
        },
        {
            title: '描述',
            field: 'desc'
        }
      ]
      const tableData=ref([])
      const total=ref(0)
      // 读取后台请求
      // getPlans().then(
      //   function(resp){
      //     tableData.value=resp.data.retlist // 拿到后台返回的retlist
      //   }
      // )
      function sync_data(page_size, page_index) {
        getPlans(page_size, page_index).then(function (resp) {
          tableData.value = resp.data.retlist
          total.value = resp.data.total
        });
      }
      // 组件加载后自动更新一次数据
      onMounted(() => {
        sync_data(5,1);
      });
      // provide为子组件、后代组件提供数据
      provide("total", total);
      provide("sync_data", sync_data);
      provide("columns", columns);
      provide("tableData", tableData);
    }
  }
</script>