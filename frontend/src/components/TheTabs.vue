<template>
  <el-header style="height: 40px;">
    <!-- height的值使得横线紧贴边缘 -->
    <el-tabs v-model="activeName" @tab-click="handleClick">
      <el-tab-pane label="主页" name="home"></el-tab-pane>
      <el-tab-pane label="部署" name="deploys"></el-tab-pane>
      <el-tab-pane label="模型" name="models"></el-tab-pane>
      <el-tab-pane label="脚本" name="scripts"></el-tab-pane>
      <el-tab-pane label="数据集" name="datasets"></el-tab-pane>
    </el-tabs>
  </el-header>
</template>
<script>
export default {
  data() {
    return {
      activeName: this.$route.name
    }
  },
  methods: {
    handleClick(tab) {
      if (tab.name !== this.$route.name) {
        this.$router.push({ name: tab.name });
      }
    }
  }
}
</script>
<style scoped>
</style>