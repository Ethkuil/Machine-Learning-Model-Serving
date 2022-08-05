<template>
  <div>
    <TheTabs />
    <el-main class="main">
      <el-card>
        <el-row slot="header" type="flex" justify="space-between" align="middle">
          <h3 class="title">{{ title }}</h3>
          <el-row type="flex">
            <el-button icon="el-icon-plus" @click="dialogAddDatasetFormVisible = true">添加数据集</el-button>
            <el-input v-model="search" placeholder="搜索数据集名" suffix-icon="el-icon-search" style="margin-left: 20px">
            </el-input>
          </el-row>
        </el-row>

        <DatasetTable :data="datasets.filter(data => data.name.includes(search))" />
      </el-card>
    </el-main>
    <el-dialog title="添加数据集" :visible.sync="dialogAddDatasetFormVisible">
      <AddDatasetForm :ref="formRef" />
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogAddDatasetFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="submitForm()">添 加</el-button>
      </div>
    </el-dialog>
  </div>
</template>
<script>
import TheTabs from '../components/TheTabs.vue'
import DatasetTable from '../components/tables/DatasetTable.vue'
import AddDatasetForm from '../components/forms/AddDatasetForm.vue'
export default {
  components: { TheTabs, DatasetTable, AddDatasetForm },
  data() {
    return {
      title: this.$route.meta && this.$route.meta.title,
      search: '',
      datasets: [
        {
          id: 1,
          name: '数据集1',
          type: 'CSV',
          size: '2.71KB',
          update_time: '2018-01-15 16:01',
        },
        {
          id: 2,
          name: '数据集2',
          type: 'ZIP',
          size: '1.52MB',
          update_time: '2018-01-03 16:45',
        },
        {
          id: 3,
          name: '数据集3',
          type: 'CSV',
          size: '12.17KB',
          update_time: '2019-06-01 12:01',
        },
      ],
      dialogAddDatasetFormVisible: false,
      formRef: 'addDatasetFormWithSubmit',
    }
  },
  methods: {
    submitForm() {
      this.$refs[this.formRef].submitForm()
    },
  },
}
</script>
<style scoped>
.main {
  background-color: #f1f2f6
}
</style>