<template>
  <MainLayout :columns="columns" :tableData="tableData"></MainLayout>
</template>

<script>
  import MainLayout from '../components/common/MainLayout.vue';
  import {ref} from 'vue';
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
      // 读取后台请求
      getReports().then(
        function(resp){
          tableData.value=resp.data.retlist // 拿到后台返回的retlist
        }
      )
      return{
          columns,
          tableData
      }
    }
  }
</script>