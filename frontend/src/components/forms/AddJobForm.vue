<template>
  <div>
    <el-form :model="form" :ref="formRef" :rules="rules">

      <el-form-item label="服务名称" prop="name">
        <el-input v-model="form.name"></el-input>
      </el-form-item>

      <el-form-item label="数据集文件" prop="input">
        <el-upload action="nothing" :auto-upload="false" :limit="1" :on-change="handleChange">
          <el-button type="primary">点击添加</el-button>
        </el-upload>
      </el-form-item>

    </el-form>
  </div>
</template>
<script>
export default {
  props: {
    id: {
      type: Number,
    },
  },
  data() {
    return {
      formRef: "formForAddJob",
      form: {
        name: '',
        input: null,
      },
      rules: {
        name: [
          { required: true, message: '请输入服务名称', trigger: 'blur' },
          { max: 20, message: '长度在 1 到 20 个字符', trigger: 'blur' },
        ],
        input: [
          { required: true, message: '请上传一个文件', trigger: 'change' },
        ],
      },
    }
  },
  methods: {
    handleChange(file) {
      this.form.input = file.raw;
    },
    submitForm() {
      this.$refs[this.formRef].validate((valid) => {
        if (!valid) {
          return false
        }
        const params = {
          name: this.form.name,
          model_id: this.id,
          input: this.form.input,
        };
        this.$axios.post(`/jobs`, params, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        })
          .then(res => {
            this.$message({
              type: 'success',
              message: '提交成功!',
            });
            this.$emit('submit-success');
          })
          .catch(() => {
            this.$message({
              type: 'info',
              message: '提交失败!',
            })
          })
      });
    },
  },
}
</script>
<style scoped>
</style>
