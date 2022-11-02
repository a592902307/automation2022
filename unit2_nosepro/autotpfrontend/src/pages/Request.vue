<template>
  <MainLayout :columns="columns" :tableData="tableData"></MainLayout>
</template>

<script>
  import MainLayout from '../components/common/MainLayout.vue';
  import {ref} from 'vue';
  import { getRequests } from '@/httplib';
  export default {
    components:{
      MainLayout,
    },
    setup(){
      const columns=[
        {
            title: '请求方法',
            field: 'method',
        },
        {
            title: '请求路径',
            field: 'url',
        },
        {
            title: '请求体参数',
            field: 'data',
        },
        {
            title: 'URL参数',
            field: 'params' 
        },
        {
            title: '请求头',
            field: 'headers' 
        }
      ]
      const tableData=ref([])
      // 读取后台请求
      getRequests().then(
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