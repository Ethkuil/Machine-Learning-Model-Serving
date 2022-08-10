<template>
  <div>
    <el-page-header @back="goBack" title="返回" class="page-header" />

    <el-header class="row-bg">
      <el-row type="flex">
        <el-col>
          <h3>{{ model.name }}</h3>
          <p class="description">{{ model.description }}</p>
        </el-col>
        <el-row class="info" type="flex" justify="space-between">
          <el-col class="tab">
            <el-row class="label">修改时间</el-row>
            <el-row class="content-time">{{ model.update_time }}</el-row>
          </el-col>
          <el-col class="tab">
            <el-row class="label">类型</el-row>
            <el-row class="content">{{ model.type }}</el-row>
          </el-col>
          <el-col class="tab">
            <el-row class="label">算法</el-row>
            <el-row class="content">{{ model.algorithm }}</el-row>
          </el-col>
          <el-col class="tab">
            <el-row class="label">引擎</el-row>
            <el-row class="content">{{ model.engine }}</el-row>
          </el-col>
        </el-row>
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
        inputVariablesData: [
          /*
          {
            field: 'sepal length(cm)',
            type: 'double',
            measure: 'continuous',
            value: ''
          },

          */
        ],
        targetVariablesData: [
          /*
          {
            field: 'Species',
            type: 'integer',
            measure: 'nominal',
            value: '0,1,2'
          }
          */
        ],
        deploys: [
          {
            id: 1,
            name: '部署1',
            type: 'PMML',
            start_time: '2017-01-15 16:01',
            state: '运行中'
          },
          {
            id: 3,
            name: '部署3',
            type: 'PMML',
            start_time: '2019-06-01 19:01',
            state: '运行中'
          },
        ],
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
    getData () {
      console.log('enter getData')
        const path = 'http://localhost:5000/getModelDetail'
        const payload = {   // TO DO: 从前端读取文件路径或者直接读取文件
          'filePath': '/Users/janet/Desktop/bigHomework/xgb-iris.pmml'
          //'mnist-8.onnx'#'rf_iris.onnx'#'.\demo.pmml'#'xgb-iris.pmml'# 'models/randomForest.pmml'
        }
        axios.post(path, payload).then((response) => {
          /*
          console.log('filePath:', response.data.filePath);
          console.log('xNames:', response.data.xNames);
          console.log('xDTS:', response.data.xDataTypes);
          console.log('xOTS:', response.data.xOpTypes);
          console.log('yNames:', response.data.yNames);
          console.log('yDTS:', response.data.yDataTypes);
          console.log('yOTS:', response.data.yOpTypes);
          */
          this.model.inputVariablesData = []
          for (let i = 0; i < response.data.xNames.length; i++) {
            var tmp = {
              field: response.data.xNames[i],
              type: response.data.xDataTypes[i],
              measure: response.data.xOpTypes[i],
              value: '',
            }
            if(response.data.xValues[i]) {
              console.log('enter loop')
              var li = response.data.xValues[i]
              for (let j = 0; j < li.length; j++) {
                tmp.value += (li[j] + ',')
              }
            }
            this.model.inputVariablesData.push(tmp)
          }
          this.model.targetVariablesData = []
          for (let i = 0; i < response.data.yNames.length; i++) {
            var tmp = {
              field: response.data.yNames[i],
              type: response.data.yDataTypes[i],
              measure: response.data.yOpTypes[i],
              value: '',
            }
            if(response.data.yValues[i]) {
              // console.log('enter loop')
              var li = response.data.yValues[i]
              for (let j = 0; j < li.length; j++) {
                tmp.value += (li[j] + ',')
              }
              tmp.value = tmp.value.slice(0, (tmp.value.length - 1))   //删除最后一个逗号
            }
            this.model.targetVariablesData.push(tmp)
          }
        })
    },
    },
  created () {
    this.getData()
  },
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

.tab{
  width: 80px;
}

.label {
  color: #999;
  font-size: 14px;
}

.content {
  font-size: 15px;
  word-wrap: break-word;
}

.content-time {
  color: #666;
  font-size: 12px;
}
</style>