<template>
  <div>
    <el-page-header @back="goBack" title="返回" class="page-header" />

    <el-header class="row-bg">
      <el-row type="flex" align="middle" justify="space-between">
        <div>
          <h3>{{ service.name }}</h3>
        </div>
        <div>
          <el-row class="info" type="flex">
            <el-col>
              <el-row class="label">模型</el-row>
              <el-row class="content">{{ service.model.name }}</el-row>
            </el-col>
            <el-col>
              <el-row class="label">服务状态</el-row>
              <el-row class="content">{{ service.state }}</el-row>
            </el-col>
            <el-col>
              <el-row class="label">开始时间</el-row>
              <el-row class="content-time">{{ service.start_time }}</el-row>
            </el-col>
          </el-row>
        </div>
      </el-row>
    </el-header>

    <el-header style="height: 40px;">
      <!-- height的值使得横线紧贴边缘 -->
      <el-tabs v-model="activeName">
        <el-tab-pane label="测试" name="tests"></el-tab-pane>
      </el-tabs>
    </el-header>

    <TestTab v-if="activeName == 'tests'" />

  </div>
</template>
<script>
import TestTab from "../components/serviceDetail/TestTab.vue";
export default {
  data() {
    return {
      activeName: 'tests',
      service: {
        id: 1,
        name: '部署1',
        start_time: '2020-01-01 00:30',
        state: '运行中',
        model: {
          id: 1,
          name: '模型1',
          type: 'PMML',
          update_time: '2020-01-01 00:30'
        }
      },
    }
  },
  components: {
    TestTab,
  },
  created() {
    this.getServiceDetail();
  },
  methods: {
    getServiceDetail() {
      this.$axios.get(`/services/${this.$route.params.id}`).then(res => {
        this.service = res.data.data;
      })
    },
    goBack() {
      this.$router.go(-1);
    }
  }
}
</script>
<style scoped>
.page-header {
  padding: 10px;
}

.row-bg {
  background-color: #f5f5f5;
}


.info * {
  width: max-content;
  padding-left: 16px;
}

.info .label {
  font-size: 14px;
  color: #999;
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