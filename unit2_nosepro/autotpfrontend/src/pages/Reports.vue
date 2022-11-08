<template>
  <MainLayout :columns="columns" :tableData="tableData"></MainLayout>
</template>

<script>
  import MainLayout from '../components/common/MainLayout.vue';
  import { ref,onMounted,provide } from 'vue';
  import { getReports } from '@/httplib';
  export default {
    components:{
      MainLayout,
    },
    setup(){
      const columns=[
        {
            title: '测试计划',
            field: 'plan.name',
        },
        {
            title: '测试人员',
            field: 'trigger.username',
        },
        {
            title: '开始时间',
            field: 'create_time',
        },
        {
            title: '结束时间',
            field: 'update_time' 
        },
        {
            title: '报告详情',
            field: 'desc' 
        }
      ]
      const tableData=ref([])
      const total=ref(0)
      // 读取后台请求
      // getReports().then(
      //   function(resp){
      //     tableData.value=resp.data.retlist // 拿到后台返回的retlist
      //   }
      // )
      // return{
      //     columns,
      //     tableData
      // }
      function sync_data(page_size, page_index) {
        getReports(page_size, page_index).then(function (resp) {
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