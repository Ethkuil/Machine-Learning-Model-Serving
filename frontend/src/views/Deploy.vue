<template>
  <div>
    <TheTabs />
    <el-main class="main">
      <el-card>
        <el-row slot="header" type="flex" justify="space-between" align="middle">
          <h3 class="title">{{ title }}</h3>
          <el-row type="flex">
            <el-button icon="el-icon-plus" @click="dialogAddServiceFormVisible = true">
              添加服务
            </el-button>
            <el-button icon="el-icon-plus" @click="dialogAddTaskFormVisible = true" style="margin-left: 20px;">
              添加任务
            </el-button>
            </el-input>
          </el-row>
        </el-row>

        <el-table :data="tableData" :default-sort="{ prop: 'date', order: 'descending' }" empty-text="没有任何部署">
          <el-table-column prop="name" label="名称" sortable></el-table-column>
          <el-table-column prop="type" label="类型" sortable></el-table-column>
          <el-table-column prop="date" label="开始时间" sortable></el-table-column>
          <el-table-column prop="state" label="状态" sortable></el-table-column>
          <el-table-column label="操作" align="center">
            <template slot-scope="scope">
              <el-button type="text" size="small" @click="handleDetail(scope.row)">详情</el-button>
              <el-button type="text" size="small" @click="handleDelete(scope.row)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </el-main>
  </div>
</template>
<script>
import TheTabs from '../components/TheTabs.vue';
export default {
  components: { TheTabs },
  data() {
    return {
      title: this.$route.meta.title,
      tableData: [
        {
          name: '部署1',
          type: 'PMML',
          date: '2018-01-15',
          state: '运行中'
        },
        {
          name: '部署2',
          type: 'ONNX',
          date: '2018-01-03',
          state: '运行中'
        },
        {
          name: '部署3',
          type: 'PMML',
          date: '2019-06-01',
          state: '运行中'
        },
      ]
    };
  }
}
</script>
<style scoped>
.main {
  background-color: #f1f2f6;
}
</style>