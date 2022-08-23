<template>
  <div>
    <el-page-header @back="goBack" title="返回" class="page-header" />

    <el-header class="row-bg" style="height:max-content">
      <el-row type="flex" align="middle" justify="space-between">
        <div>
          <h3>{{ model.name }}</h3>
          <p class="description">{{ model.description }}</p>
        </div>
        <div>
          <el-row class="info" type="flex">
            <el-col>
              <el-row class="label">修改时间</el-row>
              <el-row class="content-time">{{ model.update_time }}</el-row>
            </el-col>
            <el-col>
              <el-row class="label">类型</el-row>
              <el-row class="content">{{ model.type }}</el-row>
            </el-col>
          </el-row>
        </div>
      </el-row>
    </el-header>

    <el-header style="height: 40px;">
      <!-- height的值使得横线紧贴边缘 -->
      <el-tabs v-model="activeName">
        <el-tab-pane label="概述" name="overview"></el-tab-pane>
        <el-tab-pane label="部署" name="deploys"></el-tab-pane>
        <el-tab-pane label="测试" name="tests"></el-tab-pane>
      </el-tabs>
    </el-header>

    <OverviewTab v-if="activeName == 'overview'" :input_variables="model.input_variables"
      :target_variables="model.target_variables" />
    <DeployTab v-if="activeName == 'deploys'" :id="id" :services="model.services" :jobs="model.jobs"
      @refresh="getModelDetail" />
    <TestTab v-if="activeName == 'tests'" :input_variables="model.input_variables" />


  </div>
</template>
<script>
import OverviewTab from "../components/modelDetail/OverviewTab.vue";
import DeployTab from "../components/modelDetail/DeployTab.vue";
import TestTab from "../components/modelDetail/TestTab.vue";

export default {
  components: { OverviewTab, DeployTab, TestTab },
  data() {
    return {
      // id是integer类型
      id: parseInt(this.$route.params.id),
      activeName: 'overview',
      model: {
        name: "example-model",
        description: "这是一个示例模型",
        update_time: "2020-01-01 16:01",
        type: "PMML",
        input_variables: [],
        target_variables: [],
        services: [],
        jobs: []
      }
    };
  },
  created() {
    this.getModelDetail();
  },
  methods: {
    goBack() {
      this.$router.go(-1);
    },
    getModelDetail() {
      this.$axios.get(`/models/${this.$route.params.id}`)
        .then(res => {
          this.model = res.data.data;
        })
        .catch(err => {
          this.$message.error(err.response.data.error);
        });
    }
  },
}
</script>
<style scoped>
.page-header {
  padding: 10px;
}

.row-bg {
  background-color: #f5f5f5;
}

.description {
  color: #999;
  font-size: 14px;
}

.info * {
  width: max-content;
  padding-left: 16px;
}

.label {
  color: #999;
  font-size: 14px;
  padding-bottom: 5px;
}

.content {
  font-size: 20px;
}

.content-time {
  color: #666;
  font-size: 12px;
}
</style>