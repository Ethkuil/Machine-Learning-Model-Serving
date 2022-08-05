<template>
  <div>
    <TheTabs />
    <el-main class="main">
      <el-card>
        <el-row slot="header" type="flex" justify="space-between" align="middle">
          <h3 class="title">{{ title }}</h3>
          <el-row type="flex">
            <el-button icon="el-icon-plus" @click="dialogImportModelFormVisible = true">导入模型</el-button>
            <el-input v-model="search" placeholder="搜索模型名" suffix-icon="el-icon-search" style="margin-left: 20px">
            </el-input>
          </el-row>
        </el-row>

        <ModelTable :data="models.filter(data => data.name.includes(search))" />
      </el-card>
    </el-main>

    <el-dialog title="导入模型" :visible.sync="dialogImportModelFormVisible">
      <ImportModelForm :ref="formRef" />
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogImportModelFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="submitForm()">导 入</el-button>
      </div>
    </el-dialog>
  </div>
</template>
<script>
import TheTabs from '../components/TheTabs.vue'
import ImportModelForm from '../components/forms/ImportModelForm.vue'
import ModelTable from '../components/tables/ModelTable.vue'
export default {
  components: { TheTabs, ImportModelForm, ModelTable },
  data() {
    return {
      title: this.$route.meta && this.$route.meta.title,
      search: '',
      models: [
        {
          id: 1,
          name: '模型1',
          type: 'PMML',
          date: '2018-01-15 16:01',
        },
        {
          id: 2,
          name: '模型2',
          type: 'ONNX',
          date: '2018-01-03 16:45',
        },
        {
          id: 3,
          name: '模型3',
          type: 'PMML',
          date: '2019-06-01 12:01',
        },
      ],
      dialogImportModelFormVisible: false,
      formRef: 'importModelFormWithSubmit',
    }
  },
  methods: {
    submitForm() {
      this.$refs[this.formRef].submitForm()
    },
  }
}
</script>
<style scoped>
.main {
  background-color: #f1f2f6
}
</style>