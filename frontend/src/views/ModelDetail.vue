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
            <el-col>
              <el-row class="label">算法</el-row>
              <el-row class="content">{{ model.algorithm }}</el-row>
            </el-col>
            <el-col>
              <el-row class="label">引擎</el-row>
              <el-row class="content">{{ model.engine }}</el-row>
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
        <el-tab-pane label="实时预测（快速返回）" name="predictions"></el-tab-pane>
        <el-tab-pane label="批量预测（等待返回）" name="batchPredictions"></el-tab-pane>
        <el-tab-pane label="关联脚本" name="scripts"></el-tab-pane>
      </el-tabs>
    </el-header>

    <OverviewTab v-if="activeName == 'overview'" :inputVariablesData="model.inputVariablesData"
      :targetVariablesData="model.targetVariablesData" />
    <DeployTab v-if="activeName == 'deploys'" :deploys="model.deploys" />
    <TestTab v-if="activeName == 'tests'" :inputVariablesData="model.inputVariablesData" />


  </div>
</template>
<script>
import OverviewTab from "../components/modelDetail/OverviewTab.vue";
import DeployTab from "../components/modelDetail/DeployTab.vue";
import TestTab from "../components/modelDetail/TestTab.vue";
import axios from 'axios';

export default {
  data() {
    return {
      activeName: 'overview',
      model: {
        name: "example-model",
        description: "这是一个示例模型",
        update_time: "2020-01-01 16:01",
        type: "PMML",
        algorithm: "MiningModel(classification)",
        engine: "PyPMML",
        inputVariablesData: [],
        deploys: [],
        tests: [],
        predictions: [],
        batchPredictions: [],
        scripts: [],
      }
    };
  },
  methods: {
    goBack() {
      this.$router.go(-1);
    },
  }
  components: { OverviewTab, DeployTab, TestTab }
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