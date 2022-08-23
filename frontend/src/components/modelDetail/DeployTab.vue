<template>
  <div>
    <el-main class="main">
      <el-card>

        <el-row slot="header" type="flex" justify="space-between" align="middle">
          <h3>{{ title }}</h3>
          <el-row type="flex">
            <el-button icon="el-icon-plus" @click="dialogAddServiceFormVisible = true">添加服务</el-button>
            <el-button icon="el-icon-plus" @click="dialogAddJobFormVisible = true" style="margin-left: 20px">添加任务
            </el-button>
            <el-input v-model="search" placeholder="搜索部署名" suffix-icon="el-icon-search" style="margin-left: 20px">
            </el-input>
          </el-row>
        </el-row>

        <h4>服务</h4>
        <ServiceTable :data="services.filter(data => data.name.includes(search))" @refresh="refresh"></ServiceTable>
        <h4>任务</h4>
        <JobTable :data="jobs.filter(data => data.name.includes(search))" @refresh="refresh"></JobTable>

      </el-card>
    </el-main>

    <el-dialog title="添加服务" :visible.sync="dialogAddServiceFormVisible">
      <AddServiceForm ref="addServiceFormRef" :id="id" />
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogAddServiceFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="submitAddServiceForm()">添 加</el-button>
      </div>
    </el-dialog>

    <el-dialog title="添加任务" :visible.sync="dialogAddJobFormVisible">
      <AddJobForm ref="addJobFormRef" :id="id" @submit-success="submitSuccess" />
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogAddJobFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="submitAddJobForm()">添 加</el-button>
      </div>
    </el-dialog>

  </div>
</template>
<script>
import ServiceTable from '../tables/ServiceTable.vue';
import JobTable from '../tables/JobTable.vue';
import AddServiceForm from '../forms/AddServiceForm.vue';
import AddJobForm from '../forms/AddJobForm.vue';
export default {
  props: {
    id: {
      type: Number,
    },
    services: {
      type: Array,
      default: () => []
    },
    jobs: {
      type: Array,
      default: () => []
    },
  },
  components: { ServiceTable, JobTable, AddServiceForm, AddJobForm },
  data() {
    return {
      title: '部署',
      search: '',
      dialogAddServiceFormVisible: false,
      dialogAddJobFormVisible: false,
    };
  },
  methods: {
    submitAddServiceForm() {
      this.$refs.addServiceFormRef.submitForm();
    },
    submitAddJobForm() {
      this.$refs.addJobFormRef.submitForm();
    },
    refresh() {
      this.$emit('refresh');
    },
    submitSuccess() {
      this.dialogAddServiceFormVisible = false;
      this.dialogAddJobFormVisible = false;
      this.refresh();
    },
  },
}
</script>
<style scoped>
.main {
  background-color: #f1f2f6;
}
</style>
