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
        <el-upload drag :limit="1" :action="action" :before-upload="beforeUpload" :on-success="handleUploadSuccess"
          :on-error="handleUploadError">
          <i class="el-icon-upload"></i>
          <div class="el-upload__text">将模型文件拖至此处，或<em>点击上传</em></div>
          <div class="el-upload__tip" slot="tip">上传的模型文件应与所选类型匹配</div>
        </el-upload>
      </el-form-item>

    </el-form>
  </div>
</template>
<script>
export default {
  data() {
    return {
      action: '', // 上传的地址
      formRef: "importModelForm",
      form: {
        name: '',
        description: '',
        type: '',
        file: '',
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
    beforeUpload(file) {
      if (!this.form.type) {
        this.$message.error('请选择文件类型')
        return false
      }
      const fileName = file.name
      const fileType = fileName.substring(fileName.lastIndexOf('.') + 1).toUpperCase()
      if (fileType !== this.form.type) {
        this.$message.error('文件类型不符合')
        return false
      }
    },
    handleUploadError(error) {
      this.$message.error("上传失败")
    },
    // TODO
    handleUploadSuccess(response, file) {
      this.form.file = response.data.url
    },
    submitForm() {
      this.$refs[this.formRef].validate((valid) => {
        if (!valid) {
          return
        }
        // TODO 整理数据，提交到后台
      })
    }
  },
}
</script>
<style scoped>
</style>