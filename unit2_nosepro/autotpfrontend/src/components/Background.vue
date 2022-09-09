<template>
    <div ref="bg" class="bg"></div>
</template>

<script>
    import {onBeforeUnmount, onMounted, ref,getCurrentInstance} from 'vue';
    import CanvasNest from "canvas-nest.js";
    export default ({
        setup() {
            const config = {
                color: "18,156,255",
                opacity: 0.7,
                zIndex: -1,
                count: 150,
                pointColor: "255,0,0"
            };
            const bg = ref(null);
            onMounted(() => {
                getCurrentInstance().cn = new CanvasNest(bg.value, config);
            });
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