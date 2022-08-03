<template>
  <div>
    <TheTabs />
    <el-main class="main">
      <el-card>
        <el-row slot="header" type="flex" justify="space-between" align="middle">
          <h3 class="title">{{ title }}</h3>
          <el-row type="flex">
            <el-button icon="el-icon-plus" @click="dialogImportModelFormVisible = true">导入模型</el-button>
            <el-input v-model="search" placeholder="搜索模型名" suffix-icon="el-icon-search" style="margin-left: 20px;">
            </el-input>
          </el-row>
        </el-row>

        <el-table :data="tableData.filter(data => data.name.includes(search))"
          :default-sort="{ prop: 'date', order: 'descending' }" empty-text="没有任何模型">
          <el-table-column prop="name" label="名称" sortable></el-table-column>
          <el-table-column prop="type" label="类型" sortable></el-table-column>
          <el-table-column prop="date" label="更新时间" sortable></el-table-column>
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
      search: '',
      tableData: [
        {
          name: '模型1',
          type: 'PMML',
          date: '2018-01-15'
        },
        {
          name: '模型2',
          type: 'ONNX',
          date: '2018-01-03'
        },
        {
          name: '模型3',
          type: 'PMML',
          date: '2019-06-01'
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