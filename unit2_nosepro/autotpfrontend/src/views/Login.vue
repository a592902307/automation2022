<template>
    <Background></Background>
    <div class="lf">
        <div class="title">测试平台</div>
        <div class="login-form">
            <!-- 表单最外层用el-form来包裹 ref绑定元素可以让后端操作dom元素 -->
            <!-- :model 绑定表单数据对象 -->
            <el-form :model="form" label-width="60px" :rules="rules" validate-on-rule-change ref="loginForm">
                <div class="text-header">登录</div>
                <!-- el-form需要嵌套el-form-item -->
                <el-form-item label="账号" prop="account">
                    <el-input v-model="form.account" placeholder="请输入账号" autocomplete="off"></el-input>
                </el-form-item>
                <el-form-item label="密码" prop="psw">
                    <el-input v-model="form.psw" placeholder="请输入密码" show-password autocomplete="off" @keyup.enter="submit"></el-input>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="submit">submit</el-button>
                    <el-button type="" @click="reset">reset</el-button>
                </el-form-item>
            </el-form>
        </div>
    </div>

</template>

<script>
    import {ref,reactive} from "vue"
    import Background from '../components/Background.vue'
    import {login} from '@/httplib'
    export default ({
        components:{
            Background
        },

        setup() {
            const loginForm=ref(null)
            // 转换成响应式对象需要reactive
            const form=reactive({
                account:"",
                psw:""
            })
            function submit(){
                console.log("点我提交");
                login(form.account,form.psw) // 调用登录
                form.account="";
                form.psw="";
            }
            function reset(){
                // reactive包裹的对象不需要用value来调用了
                // form.account=""
                // form.psw=""
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
    .lf {
        margin: 0 auto;
        width: 300px;
    }
    .text-header {
      text-align: center;
      font-size: 20px;
      color: rgb(16, 16, 16);
      margin-bottom: 30px;
      text-shadow: rgb(0, 255, 0) 10px 10px 10px;
    }
    .login-form {
      position: absolute;
      width: 300px;
      height: 300px;
      text-align: center;
      border-radius: 10px;
      box-shadow: 1px 1px 5px #333;
      display: flex;
      justify-content: center;
      align-items: center;
      top: 200px;
      /* top: 50%;
      left: 50%;
      transform: translate(-50%,-50%); */
    }
    .title {
      position: absolute;
      width: 100%;
      text-align: center;
      height: 80px;
      top: 100px;
      right: 0;
      display: flex;
      justify-content: center;
      align-items: center;
      font-size: 33px;
      font-weight:300;
      font-family: "Microsoft Yahei";
      color: rgb(13, 104, 139);
    }
    .el-form-item {
      color: black;
    }

</style>