<template>
  <div>
    <el-main class="main">
      <el-card>
        <el-row slot="header" type="flex" justify="space-between" align="middle">
          <h3 class="title">{{ title }}</h3>
          <el-row type="flex">
            <el-button icon="el-icon-plus" @click="dialogAddServiceFormVisible = true">添加服务</el-button>
            <el-button icon="el-icon-plus" @click="dialogAddJobFormVisible = true" style="margin-left: 20px">添加任务
            </el-button>
            <el-input v-model="search" placeholder="搜索部署名" suffix-icon="el-icon-search" style="margin-left: 20px">
            </el-input>
          </el-row>
        </el-row>

        <DeployTable :data="deploys.filter(data => data.name.includes(search))" />
      </el-card>
    </el-main>

    <el-dialog title="添加服务" :visible.sync="dialogAddServiceFormVisible">
      <AddServiceForm ref="addServiceFormRef" />
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogAddServiceFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="submitAddServiceForm()">添 加</el-button>
      </div>
    </el-dialog>

  </div>
</template>
<script>
import DeployTable from '../tables/DeployTable.vue';
import AddServiceForm from '../forms/AddServiceForm.vue';
export default {
  props: {
    deploys: {
      type: Array,
      default: () => []
    }
  },
  components: { DeployTable, AddServiceForm },
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
  },
}
</script>
<style scoped>
.main {
  background-color: #f1f2f6;
}
</style>