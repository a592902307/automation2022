<template>
  <div class="home">
    <img alt="Vue logo" src="../assets/logo.png">
    <HelloWorld msg="Welcome to Your Vue.js App"/>
    <HelloYh></HelloYh>
  </div>
</template>

<script>
// @ is an alias to /src
import HelloWorld from '@/components/HelloWorld.vue'
import HelloYh from '../components/helloyh.vue'

export default {
  name: 'HomeView',
  components: {
    HelloWorld,HelloYh
  }
}
</script>
