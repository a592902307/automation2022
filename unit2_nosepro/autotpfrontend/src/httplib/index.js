import axios from "axios";
import router from '../router';
import { ElMessage } from 'element-plus'; // ElMessage消息框

axios.defaults.validateStatus=(status)=>{
    return status>=200 && status<400  // 返回状态为200-400的请求才是正常请求
};
axios.defaults.baseURL='http://120.27.146.185:8076'; // 设置baseURL

// 登录请求
function login(username,password){
    axios({
        method:'post',
        url:'/api/login/',
        data:{
            username,
            password
        }
    }).then(
        function(response){
            console.log("登录成功");
            console.log(response.data);
            // 账号密码正确-响应成功-跳转首页
            ElMessage.success(response.data.msg);
            router.push('/');
            localStorage.setItem('islogin','yes') // 设置登录状态
        }
    ).catch(
        // 处理异常响应，根据状态码，默认非2开头的响应码会在这里处理
        function(error){
            console.log("登录失败");
            console.log(error.response.data);
            ElMessage.error(error.response.data.error);
        }
    )
}

// 退出请求
function logout(){
    axios.get(
        '/api/logout/'
    ).then(()=>{
        // 返回到登录
        router.push('/login')
        ElMessage.info("退出登录")
        localStorage.setItem('islogin','no') // 设置登录状态
    }      
    )
}

// 获取用例数据请求
function getCases(page_size,page_index){
    return axios({
      method: 'get',
      url: 'api/cases/',
      params: {
        page_size,
        page_index,
      }
    })
 }
   



// export：导出  export default就相当于把导出内容设置一个default别名 其实导出的是default 好处是导入是不需要写{}、
// 当有多个内容需要导出时，此时应该不写default，导入时需要加上{}
// export default login
export {login,logout,getCases}