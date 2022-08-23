<template>
  <div>
    <el-form :model="form" :ref="formRef" :rules="rules">

      <el-form-item label="服务名称" prop="name">
        <el-input v-model="form.name"></el-input>
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
      formRef: "formForAddService",
      form: {
        name: '',
      },
      rules: {
        name: [
          { required: true, message: '请输入服务名称', trigger: 'blur' },
          { max: 20, message: '长度在 1 到 20 个字符', trigger: 'blur' },
        ],
      },
    }
  },
  methods: {
    submitForm() {
      this.$refs[this.formRef].validate((valid) => {
        if (!valid) {
          return false
        }
        const params = {
          name: this.form.name,
          model_id: this.id,
        };
        this.$axios.post(`/services`, params, {
          headers: {
            'Content-Type': 'application/json',
          },
        })
          .then(res => {
            this.$message({
              type: 'success',
              message: '提交成功!',
            })
            this.$router.push({
              name: 'serviceDetail',
              params: { id: res.data.data.id },
            })
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
