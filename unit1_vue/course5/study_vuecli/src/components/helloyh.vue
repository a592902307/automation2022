<template>
    <div>
        <button @click="chilema">吃饭/消化</button>
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
    //             ate
    //         }
    //     },
    //     methods:{
    //         chilema(){
    //             this.ate=!this.ate
    //         }
    //     }
    // }
    // 组合式API
    import {ref} from 'vue'
    export default {
        name: 'HelloYh',
        // eslint-disable-next-line no-unused-vars
        setup(props) {
            let ate= ref(false) // 响应式数据需要通过ref包裹
            console.log(ate.value) // false
            function chilema(){
                ate.value=!ate.value   // 数据类型需要通过value，组合式api中没有this
            }
            // 模板中引用的变量和方法统统都要return出去
            return{
                ate,
                chilema
            }
        }
    }

</script>