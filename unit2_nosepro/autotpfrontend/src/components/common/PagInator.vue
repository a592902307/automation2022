<!-- pagination分页组件 -->
<template>
    <!-- total总数据条数 page_size当前显示条数 -->
    <el-pagination 
        blackground 
        layout="prev, pager, next, sizes" 
        :total="total" 
        :page-size="page_size"
        :page-sizes="[5,10,20]"
        v-model:currentPage="page_index"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
    >
    </el-pagination>
</template>

<script>
    import { ref } from '@vue/reactivity';
    import { inject } from '@vue/runtime-core';
    export default{
        name:'PagInator',
        setup(){
            const page_size=ref(5); // 当前页显示条数 
            const page_index=ref(1); // 当前页码
            const total=inject('total');
            const sync_data=inject('sync_data');
            
            // 处理页面条数更改
            function handleSizeChange(size){
                console.log('page_size',size)
                page_size.value=size
                sync_data(page_size.value,page_index.value)
            }
            // 处理页码更新
            function handleCurrentChange(index){
                console.log('page_index',index)
                page_index.value=index
                sync_data(page_size.value,page_index.value)
            }
            return {
                total,page_size,page_index,
                handleSizeChange,handleCurrentChange
            }
        }
    }
</script>