<template>
    <el-table :data="tableData" style="width: 100%">
        <!-- 多选框 -->
        <!-- <el-table-column type="selection" width="180"></el-table-column>  -->

        <el-table-column v-for="(item,index) in columns" v-bind:key="index" :label="item.title" width="180">
            <template #default="scope">
                <div style="display: flex; align-items: center">
                    <!-- 使用 component 标签来实现动态图标 -->
                    <component :is="item.icon" style="width: 20px; height:20px;"/>
                    <span style="margin-left: 10px">{{ scope.row[item.field] }}</span>
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
export default {
    props:{
        columns:Array,
        tableData:Object
    },
    setup() {
        const handleEdit = (index, row) => {
            console.log(index, row)
        }
        const handleDelete = (index, row) => {
            console.log(index, row)
        }

        return{
            handleEdit,
            handleDelete
        }
    }
}

</script>
