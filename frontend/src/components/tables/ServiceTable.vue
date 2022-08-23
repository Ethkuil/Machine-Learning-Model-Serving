<template>
  <el-table :data="data" :default-sort="{ prop: 'start_time', order: 'descending' }" empty-text="没有任何服务">
    <!-- id列，提交请求时用 -->
    <el-table-column prop="id" label="id" sortable></el-table-column>
    <el-table-column prop="name" label="名称" sortable></el-table-column>
    <el-table-column prop="start_time" label="开始时间" sortable></el-table-column>
    <el-table-column prop="state" label="状态" sortable></el-table-column>
    <el-table-column label="操作" align="center">
      <template slot-scope="scope">
        <el-button type="text" size="small" @click="handleDetail(scope.row)">详情</el-button>
        <el-button type="text" size="small" @click="handleDelete(scope.row)">删除</el-button>
        <el-button type="text" size="small" @click="handleStart(scope.row)">启动</el-button>
        <el-button type="text" size="small" @click="handlePause(scope.row)">暂停</el-button>
      </template>
    </el-table-column>
  </el-table>
</template>
<script>
export default {
  props: {
    data: {
      type: Array,
      default: [],
    },
  },
  methods: {
    handleDetail(row) {
      this.$router.push({
        name: 'serviceDetail',
        params: { id: row.id },
      })
    },
    handleDelete(row) {
      this.$confirm('确定删除该部署吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$axios.delete(`/services/${row.id}`)
          .then(() => {
            this.$message({
              type: 'success',
              message: '删除成功!'
            })
            // 令父组件重新请求数据
            this.$emit('refresh')
          })
          .catch(() => {
            this.$message({
              type: 'info',
              message: '删除失败!'
            })
          })
      })
        .catch(() => {
          this.$message({
            type: 'info',
            message: '已取消删除'
          })
        })
    },
    handleStart(row) { // TODO 测试
      this.$message({
        type: 'info',
        message: '启动中...',
      })
      this.$axios.post(`/services/${row.id}/start`)
      this.$emit('refresh')
      this.$message({
        type: 'success',
        message: '启动成功!',
      })
    },
    handlePause(row) { // TODO 测试
      this.$message({
        type: 'info',
        message: '暂停中...',
      })
      this.$axios.post(`/services/${row.id}/pause`)
      this.$emit('refresh')
      this.$message({
        type: 'success',
        message: '暂停成功!',
      })
    },
  }
}
</script>
<style scoped>
</style>