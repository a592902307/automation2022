<template>
    <el-table :data="tableData" style="width: 100%">
        <!-- 多选框 -->
        <!-- <el-table-column type="selection" width="180"></el-table-column>  -->

        <!-- v-bind:key 用的v-for的时候的固定写法  (item,index)也是固定写法 -->
        <el-table-column v-for="(item,index) in columns" v-bind:key="index" :label="item.title" width="180">
            <!-- #default="scope" 设置一个默认的定义域插槽并定义一个对象scope来绑定数据 -->
            <template #default="scope">
                <div style="display: flex; align-items: center">
                    <!-- 使用 component 标签来实现动态图标 -->
                    <component :is="item.icon" style="width: 20px; height:20px;"/>
                    <!-- scope.row表示当前行的数据对象 -->
                    <span style="margin-left: 10px">{{ field_value(scope.row,item.field) }}</span>
                </div>
            </template>
        </el-table-column>

        <el-table-column label="Operations">
            <template #default="scope">
                <el-button size="small" @click="handleEdit(scope.$index, scope.row)">Edit</el-button>
                <el-button size="small" type="danger" @click="handleDelete(scope.$index, scope.row)">Delete</el-button>
            </template>
        </el-table-column>
    </el-table>
</template>

<script>

import {inject} from '@vue/runtime-core'
export default {
    // 改用provide、inject传输数据方式
    // props:{
    //     columns:Array,
    //     tableData:Object
    // },
    setup() {
        const columns=inject('columns')
        const tableData = inject('tableData')

        const handleEdit = (index, row) => {
            console.log(index, row)
        }
        const handleDelete = (index, row) => {
            console.log(index, row)
        }
        function field_value(obj,fields) {
            // 传入一个对象，一个多级字段，例如：config.project.name
            let temp_obj=obj
            for(const item of fields.split('.')){
                // 通过反射来重复获取字段，temp_obj=temp_obj['config'] temp_obj=temp_obj['project'] temp_obj['name']
                temp_obj=Reflect.get(temp_obj,item)
            }
            return temp_obj
        }

        return{
            handleEdit,
            handleDelete,
            field_value,
            columns,
            tableData
        }
    }
}

</script>
