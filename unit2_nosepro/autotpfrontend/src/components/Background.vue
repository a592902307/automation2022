<template>
    <div ref="bg" class="bg"></div>
</template>

<script>
    import {onBeforeUnmount, onMounted, ref,getCurrentInstance} from 'vue';
    import CanvasNest from "canvas-nest.js"; // 导入粒子canvas-nest包
    export default ({
        setup() {
            const config = {
                color: "18,156,255", // R,G,B 数字范围是0-255
                opacity: 0.7, // 不透明度
                zIndex: -1, // 背景的z-index属性，css属性用于控制所在层的位置
                count: 150, // 线条总数量，默认150
                pointColor: "255,0,0" // 焦点颜色R,G,B
            };
            const bg = ref(null);
            // 等组件加载完在画粒子效果
            onMounted(() => {
                // 获取当前组件的实例对象getCurrentInstance()
                // 初始化粒子效果new CanvasNest(背景元素引用 配置项)
                getCurrentInstance().cn = new CanvasNest(bg.value, config);
            });
            // 在组件销毁之前回收粒子效果
            onBeforeUnmount(()=>{
                getCurrentInstance().cn.destroy() //销毁实例
            })
            return {
                bg,
            };
        },
    });

</script>

<style scoped>
    .bg{
      width: 100vw;   
      height: 100vh;
    }
</style>