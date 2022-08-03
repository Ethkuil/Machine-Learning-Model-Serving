<template>
  <div id="app">
    <el-header id="header">
      <h1>{{ title }}</h1>
    </el-header>
    <router-view />
    <el-footer id="footer">
      <FooterCopyright />
    </el-footer>
  </div>
</template>

<script>
import FooterCopyright from './components/FooterCopyright.vue'
export default {
  name: 'App',
  components: {
    FooterCopyright
  },
  data() {
    return {
      title: '机器学习模型服务',
    }
  },
}
</script>

<style>
#header {
  background-color: #00152a;
  display: flex;
  align-items: center;
  color: #B2C7CF;
}

#footer {
  padding-left: 0;
  padding-right: 0;
}
</style>
