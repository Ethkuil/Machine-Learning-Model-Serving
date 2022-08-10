<template>
  <div>
    <el-form :model="form" :ref="formRef" :rules="rules">

      <el-form-item label="服务名称" prop="name">
        <el-input v-model="form.name"></el-input>
      </el-form-item>

      <el-form-item label="预留CPU" prop="cpu">
        <el-input v-model="form.cpu"></el-input>
      </el-form-item>

      <el-form-item label="预留内存(GB)" prop="memory">
        <el-input v-model="form.memory"></el-input>
      </el-form-item>


    </el-form>
  </div>
</template>
<script>
export default {
  data() {
    return {
      formRef: "formForAddService",
      form: {
        name: '',
        cpu: 0,
        memory: 0.0,
      },
      rules: {
        name: [
          { required: true, message: '请输入服务名称', trigger: 'blur' },
          { max: 20, message: '长度在 1 到 20 个字符', trigger: 'blur' },
        ],
        cpu: [
          { type: 'number', required: true, message: '请输入预留CPU' },
        ],
        memory: [
          { type: 'number', required: true, message: '请输入预留内存' },
        ],
      },
    }
  },
  methods: {
    submitForm() {
      this.$refs[this.formRef].validate((valid) => {
        if (!valid) {
          return
        }
        // TODO 提交表单
        this.$message({
          message: '提交成功',
          type: 'success'
        })
      });
    },
  },
}
</script>
<style scoped>
</style>
