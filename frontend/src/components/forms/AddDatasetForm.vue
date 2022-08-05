<template>
  <div>
    <el-form :model="form" :ref="formRef" :rules="rules">

      <el-form-item label="文件" prop="file">
        <el-upload drag :limit="1" :action="action" :before-upload="beforeUpload" :on-success="handleUploadSuccess"
          :on-error="handleUploadError">
          <i class="el-icon-upload"></i>
          <div class="el-upload__text">将数据集文件拖至此处，或<em>点击上传</em></div>
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
      formRef: "addDatasetForm",
      form: {
        file: '',
      },
      rules: {
        file: [
          { required: true, message: '请上传数据集文件', trigger: 'change' },
        ],
      },
    }
  },
  methods: {
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