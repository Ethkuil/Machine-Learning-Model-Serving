<template>
  <div>
    <TheTabs />
    <el-main class="main">
      <el-card>
        <el-row slot="header" type="flex" justify="space-between" align="middle">
          <h3 class="title">{{ title }}</h3>
          <el-row type="flex">
            <el-button icon="el-icon-plus" @click="addService">添加部署</el-button>
            <el-input v-model="search" placeholder="搜索部署名" suffix-icon="el-icon-search" style="margin-left: 20px">
            </el-input>
          </el-row>
        </el-row>

        <ServiceTable :data="tableData.filter(data => data.name.includes(search))" @refresh="refresh"></ServiceTable>
      </el-card>
    </el-main>
  </div>
</template>
<script>
import TheTabs from '../components/TheTabs.vue'
import ServiceTable from '../components/tables/ServiceTable.vue';
export default {
  components: { TheTabs, ServiceTable },
  data() {
    return {
      title: this.$route.meta && this.$route.meta.title,
      search: '',
      tableData: [
        {
          id: 1,
          name: '部署1',
          start_time: '2017-01-15',
          state: '运行中'
        },
        {
          id: 2,
          name: '部署2',
          start_time: '2018-01-03',
          state: '运行中'
        },
        {
          id: 3,
          name: '部署3',
          start_time: '2019-06-01',
          state: '运行中'
        },
      ]
    }
  },
  created() {
    this.getData();
  },
  methods: {
    getData() {
      this.$axios.get('/services').then(res => {
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