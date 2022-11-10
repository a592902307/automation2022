<!-- 测试用例详情页组件 -->
<template>
    <el-row justify="center">
        <el-col :span="24">
            <BreadCrumb> </BreadCrumb>
        </el-col>
    </el-row>
    <el-row>
        <el-col :span="24">
            <el-form status-icon label-width="80px" label-position="left" :model="caseForm">
                <!-- 公共区域 -->
                <el-form-item>
                    <div class="title"><strong>Common</strong></div>
                </el-form-item>
                <el-form-item label="file_path">
                    <el-input v-model="caseForm.file_path"></el-input>
                </el-form-item>
                <el-form-item label="desc">
                    <el-input v-model="caseForm.desc"></el-input>
                </el-form-item>
                <el-form-item label="project">
                    <el-select v-model="caseForm.selected" placeholder="Select" size="large">
                        <el-option v-for="item in caseForm.options" :key="item.value" :label="item.label"
                            :value="item.value">
                        </el-option>
                    </el-select>
                </el-form-item>
                <!-- Config部分 -->
                <el-form-item>
                    <div class="title"><strong>Config</strong></div>
                </el-form-item>
                <el-form-item label="name">
                    <el-input></el-input>
                </el-form-item>
                <el-form-item label="base_url">
                    <el-input></el-input>
                </el-form-item>
                <el-form-item label="variables">
                    <el-input type="textarea"></el-input>
                </el-form-item>
                <el-form-item label="parameters">
                    <el-input type="textarea"></el-input>
                </el-form-item>
                <el-form-item label="verify">
                    <el-switch v-model="caseForm.verify"></el-switch>
                </el-form-item>
                <el-form-item label="export">
                    <el-input type="textarea"></el-input>
                </el-form-item>
                <!-- Config部分 -->
                <el-form-item>
                    <div class="title"><strong>TestSteps</strong></div>
                    <button class="newLine">添加一行</button>
                </el-form-item>
                <el-form-item v-for="(item, index) in caseForm.teststeps" :key="index" :label="item.no">
                    <el-input type="textarea" v-model="item.content" :value="item.content"></el-input>
                </el-form-item>

                <el-form-item>
                    <el-button type="primary" @click="submitForm('ruleForm')">Submit</el-button>
                    <el-button @click="resetForm('ruleForm')">Reset</el-button>
                </el-form-item>
            </el-form>
        </el-col>
    </el-row>
</template>

<script>
import BreadCrumb from '@/components/common/BreadCrumb.vue';
import { reactive } from '@vue/reactivity';
import { caseDetail } from '@/httplib';
import { useRoute } from 'vue-router';
export default {
    name: 'CaseView',
    components: {
        BreadCrumb,
    },
    setup() {
        const options = [
            {
                label: "demo1",
                value: "demo1value",
            },
            {
                label: "demo2",
                value: "demo2value",
            }
        ];
        const selected = options[0].value;
        // 表单数据
        const caseForm = reactive({
            file_path: 'abc/path/',
            desc: 'desc',
            options,
            selected,
            verify: false,
            teststeps: [
                {
                    no: "1",
                    content: "step123",
                },
                {
                    no: "2",
                    content: "step666",
                },
            ],
        });
        function submitForm() {
            console.log('submitForm');
        }
        function resetForm() {
            console.log('resetForm');
        }

        const route = useRoute()
        // 载入用例详情
        const case_id = route.path.split('/').pop() //取路径末尾的ID
        console.log(case_id)
        caseDetail(case_id).then((resp) => {
            console.log(resp.data);
            const case_detail = resp.data.retlist[0]
            //更新表单值
            caseForm.file_path = case_detail.file_path
            caseForm.desc = case_detail.desc
            caseForm.teststeps = case_detail.teststeps
        })
        return {
            caseForm, submitForm, resetForm
        }
    }
}
</script>

<style lang="scss">
.el-row {
    margin-bottom: 20px;
}

.el-row:last-child {
    margin-bottom: 0;
}

.el-col {
    border-radius: 4px;
}

.grid-content {
    border-radius: 4px;
    min-height: 36px;
}

.row-bg {
    padding: 10px 0;
    background-color: #f9fafc;
}

.title {
    text-align: left;
    width: 120px;
}

.newLine {
    float: right;
}
</style>