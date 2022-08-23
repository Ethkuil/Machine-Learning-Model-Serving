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

        <ModelTable :data="models.filter(data => data.name.includes(search))" @refresh="getData" />
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
      models: [],
      dialogImportModelFormVisible: false,
      formRef: 'importModelFormWithSubmit',
    }
  },
  created() {
    this.getData()
  },
  methods: {
    getData() {
      this.$axios.get('/models').then(response => {
        this.models = response.data.data
      })
    },
    submitForm() {
      if (this.$refs[this.formRef].submitForm()) {
        this.dialogImportModelFormVisible = false
        this.getData()
      }
    },

  },
}
</script>
<style scoped>
.main {
  background-color: #f1f2f6;
  height: calc(100vh - 186px);
}
</style>