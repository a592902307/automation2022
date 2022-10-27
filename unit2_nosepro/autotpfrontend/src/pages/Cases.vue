<template>
  <MainLayout :columns="columns" :tableData="tableData"></MainLayout>
</template>

<script>
  import MainLayout from '../components/common/MainLayout.vue';
  import {reactive} from 'vue';
  export default {
    components:{
      MainLayout,
    },
    setup(){
      const columns=[
        {
            title: '日期',
            field: 'date',
            icon: 'Timer'
        },
        {
            title: '姓名',
            field: 'name',
        },
        {
            title: '地址',
            field: 'address',
        }
      ]
      const tableData=reactive(
        [
            {
                date: '2016-05-03',
                name: '海文',
                address: 'No. 189, Grove St, Los Angeles',
            },
            {
                date: '2016-05-02',
                name: '惊韵',
                address: 'No. 189, Grove St, Los Angeles',
            },
            {
                date: '2016-05-04',
                name: '巡天',
                address: 'No. 189, Grove St, Los Angeles',
            },
            {
                date: '2016-05-01',
                name: '苏三',
                address: 'No. 189, Grove St, Los Angeles',
            },
        ],
      )
      return{
          columns,
          tableData
      }
    }
  }
</script>