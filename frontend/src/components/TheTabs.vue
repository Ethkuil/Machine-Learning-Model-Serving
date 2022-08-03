<template>
  <el-header style="height: 40px;">
    <!-- height的值使得横线紧贴边缘 -->
    <el-tabs v-model="activeName" @tab-click="handleClick">
      <el-tab-pane label="主页" name="home"></el-tab-pane>
      <el-tab-pane label="部署" name="deploy"></el-tab-pane>
      <el-tab-pane label="模型" name="model"></el-tab-pane>
      <el-tab-pane label="脚本[暂无计划]" name="script"></el-tab-pane>
      <el-tab-pane label="数据集[暂无计划]" name="dataset"></el-tab-pane>
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