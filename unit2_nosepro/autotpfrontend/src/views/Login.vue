<template>
    <div class="title">测试平台</div>
    <div class="login-form">
        <!-- 表单最外层用el-form来包裹 -->
        <el-form :model="form" label-width="60px" :rules="rules" validate-on-rule-change ref="loginForm">
            <!-- el-form需要嵌套el-form-item -->
            <el-form-item label="账号" prop="account">
                <el-input v-model="form.account" placeholder="请输入账号"></el-input>
            </el-form-item>
            <el-form-item label="密码" prop="psw">
                <el-input v-model="form.psw" placeholder="请输入密码" show-password></el-input>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="submit">submit</el-button>
                <el-button @click="reset">reset</el-button>
            </el-form-item>
        </el-form>
    </div>
</template>

<script>
    import {ref,reactive} from "vue"
    export default ({
        // eslint-disable-next-line vue/multi-word-component-names
        name:"Login",

        setup() {
            const loginForm=ref(null)
            // 转换成响应式对象需要reactive
            const form=reactive({
                account:"",
                psw:""
            })
            function submit(){
                // reactive包裹的对象不需要用value来调用了
                form.account=""
                form.psw=""
                console.log("点我提交");
            }
            function reset(){
                form.account=""
                form.psw=""
                loginForm.value.resetFields() // 自带的恢复初始值的方法--需要通过表单元素的引用调用该方法
                console.log("点我重置");
            }
            // 定义表单输入验证规则--要求必须输入
            const rules={
                // 对象的属性需要对应表单数据对象的元素
                // msg提示信息，trigger触发器：blur表示失去焦点的时候触发
                psw: [{required: true, msg: '请输入密码',trigger: 'blur'}],
                account : [{required: true, msg: '请输入用户名',trigger: 'blur'}]
            }

            return {
                form,submit,reset,rules,loginForm
            }
        }
    })
</script>

<style scoped>
    .text-header {
      text-align: center;
      font-size: 20px;
      color: rgb(16, 16, 16);
      margin-bottom: 50px;
    }
    .login-form {
      position: absolute;
      width: 400px;
      height: 400px;
      top: 200px;
      right: 300px;
      border-radius: 10px;
      box-shadow: 1px 1px 5px #333;
      display: flex;
      justify-content: center;
      align-items: center;
    }
    .title {
      position: absolute;
      width: 400px;
      height: 80px;
      top: 50px;
      right: 300px;
      display: flex;
      justify-content: center;
      align-items: center;
      font-size: 60px;
      font-family: "Microsoft Yahei";
      color: rgb(13, 104, 139);
    }
    .el-form-item {
      color: black;
    }
</style>