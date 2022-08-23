<template>
  <div>
    <TheTabs />
    <el-main class="main">
      <el-card>
        <el-row slot="header" type="flex" justify="space-between" align="middle">
          <h3 class="title">{{ title }}</h3>
          <el-row type="flex">
            <el-button icon="el-icon-plus" @click="addService">添加部署</el-button>
            <el-input v-model="search" placeholder="搜索任务名" suffix-icon="el-icon-search" style="margin-left: 20px">
            </el-input>
          </el-row>
        </el-row>

        <JobTable :data="tableData.filter(data => data.name.includes(search))" @refresh="refresh"></JobTable>
      </el-card>
    </el-main>
  </div>
</template>
<script>
import TheTabs from '../components/TheTabs.vue'
import JobTable from '../components/tables/JobTable.vue';
export default {
  components: { TheTabs, JobTable },
  data() {
    return {
      title: this.$route.meta && this.$route.meta.title,
      search: '',
      tableData: []
    }
  },
  created() {
    this.getData();
  },
  methods: {
    getData() {
      this.$axios.get('/jobs').then(res => {
        this.tableData = res.data.data;
      })
    },
    refresh() {
      this.getData();
    },
    addService() {
      this.$message({
        message: '请选择所需模型',
        type: 'info'
      })
      this.$router.push({
        name: 'models'
      })
    }
  }
}
</script>
<style scoped>
.main {
  background-color: #f1f2f6;
  height: calc(100vh - 186px);
}
</style>