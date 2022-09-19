<template>
  <div class="home">
    <!-- <img alt="Vue logo" src="../assets/logo.png">
    <HelloWorld msg="Welcome to Your Vue.js App"/> -->
    <button @click="quit">点我退出</button>
  </div>
</template>

<script>
// @ is an alias to /src
// import HelloWorld from '@/components/HelloWorld.vue'
import {logout} from '@/httplib';

export default {
  name: 'HomeView',
  components: {
    // HelloWorld
  },
  setup(){
    function quit(){
      logout()
    }
    return{
      quit
    }
  }
}
</script>


