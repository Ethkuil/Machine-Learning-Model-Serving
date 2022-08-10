<template>
  <div>
    <TheTabs />
    <el-main class="main">
      <el-row :gutter="20">
        <el-col :span="12">
          <el-card>
            <h2>「Web前端技术实训课程」与「程序设计实践」联合大作业</h2>
            <p>仿照 DaaS 平台，提供模型部署上线一站式解决方案。</p>
          </el-card>
        </el-col>
        <el-col :span="12">
          <ConnectCard />
        </el-col>
      </el-row>
    </el-main>
  </div>
</template>

<script>
import ConnectCard from '../components/ConnectCard.vue'
import TheTabs from '../components/TheTabs.vue'
export default {
  data() {
    return {};
  },
  components: { ConnectCard, TheTabs }
}
</script>

<style scoped>
.main {
  background-color: #f1f2f6;
  height: calc(100vh - 186px);
}
</style>