<template>
  <div>
    <el-form :model="form" :ref="formRef" :rules="rules">

      <el-form-item label="名称" prop="name">
        <el-input v-model="form.name"></el-input>
      </el-form-item>

      <el-form-item label="描述" prop="description">
        <el-input type="textarea" v-model="form.description" placeholder="用简洁的文字描述模型"></el-input>
      </el-form-item>

      <el-form-item label="类型" prop="type">
        <el-select v-model="form.type" placeholder="请选择类型">
          <el-option label="PMML" value="PMML"></el-option>
          <el-option label="ONNX" value="ONNX"></el-option>
        </el-select>
      </el-form-item>

      <el-form-item label="文件" prop="file">
        <el-upload ref="upload" action="nothing" :auto-upload="false" :limit="1" :on-change="handleChange">
          <el-button type="primary">点击添加</el-button>
          <div class="el-upload__tip" slot="tip">1. 添加的模型文件应与所选类型匹配；2. 只允许添加一个文件</div>
        </el-upload>
      </el-form-item>

    </el-form>
  </div>
</template>
<script>
export default {
  data() {
    return {
      formRef: "importModelForm",
      form: {
        name: '',
        description: '',
        type: '',
        file: null,
      },
      rules: {
        name: [
          { required: true, message: '请输入模型名称', trigger: 'blur' },
          { min: 1, max: 20, message: '长度在 1 到 20 个字符', trigger: 'blur' },
        ],
        description: [
          { required: true, message: '请输入模型描述', trigger: 'blur' },
          { min: 1, max: 200, message: '长度在 1 到 200 个字符', trigger: 'blur' },
        ],
        type: [
          { required: true, message: '请选择模型类型', trigger: 'change' },
        ],
        file: [
          { required: true, message: '请上传模型文件', trigger: 'change' },
        ],
      },
    }
  },
  methods: {
    handleChange(file) {
      if (!this.form.type) {
        this.$message.error('请选择文件类型')
        this.$refs.upload.clearFiles();
        return false
      }
      const fileName = file.name
      const fileType = fileName.substring(fileName.lastIndexOf('.') + 1).toUpperCase()
      if (fileType !== this.form.type) {
        this.$message.error('文件类型不符合')
        this.$refs.upload.clearFiles();
        return false
      }
      this.form.file = file.raw
    },
    submitForm() {
      this.$refs[this.formRef].validate((valid) => {
        if (!valid) {
          return false
        }
        // 整理数据，提交到后台
        let formData = new FormData()
        formData.append('name', this.form.name)
        formData.append('description', this.form.description)
        formData.append('type', this.form.type)
        formData.append('file', this.form.file)
        let config = {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        };
        this.$axios.post('/models', formData, config)
          .then(response => {
            this.$message({
              message: '模型添加成功',
              type: 'success'
            })
            // 清空表单
            this.$refs[this.formRef].resetFields()
            this.$refs.upload.clearFiles();
          })
          .catch(error => {
            this.$message.error(`模型添加失败${error.response.data.error}`)
          })
        return true
      })
    }
  },
}
</script>
<style scoped>
</style>