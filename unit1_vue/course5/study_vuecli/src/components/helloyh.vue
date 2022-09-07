<template>
    <!-- 模板里面引用ref，可以使脚本获取dom元素对象，变量名和模板ref属性值相同 -->
    <div ref="root">
        <button @click="chilema">吃饭/消化</button>
        <h3>{{person.name}}</h3>
        <h3 v-if="ate">吃饱了</h3>
    </div>

</template>

<script>
    // 选项式API
    // export default {
    //     name:'App',
    //     data(){
    //         let ate=false;
    //         return{
    //             ate  // 这里默认转化成响应式数据了
    //         }
    //     },
    //     methods:{
    //         chilema(){
    //             this.ate=!this.ate
    //         }
    //     }
    // }
    // 组合式API
    import {ref,reactive,onMounted} from 'vue'
    export default {
        name: 'HelloYh',
        // eslint-disable-next-line no-unused-vars
        setup(props) {
            // 组件引用
            const root=ref(null);
            onMounted(() => {
                console.log(root.value)  // 获取元素对象
                console.log(root.value.tagName) // 加载之后才能看到数据
                console.log(root.value.innerText)
            })
            
            // 将简单数据类型转成响应式数据，需要ref，数据内容访问、设置需要通过value访问
            // 复杂数据（对象类型的数据），需要使用reactive函数，不需要通过value访问
            let ate= ref(false) // 响应式数据需要通过ref包裹
            console.log(ate.value) // false
            const person = reactive({
                name:'yh',
                age:18
            })

            function chilema(){
                ate.value=!ate.value   // 设置数据类型需要通过value，组合式api中没有this
            }
            // 模板中引用的变量和方法统统都要return出去
            return{
                ate,
                chilema,
                person,
                root
            }
        }
    }

</script>