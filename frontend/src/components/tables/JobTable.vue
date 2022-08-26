<template>
  <el-table :data="data" :default-sort="{ prop: 'start_time', order: 'descending' }" empty-text="没有任何任务">
    <!-- id列，提交请求时用 -->
    <el-table-column prop="id" label="id" sortable></el-table-column>
    <el-table-column prop="name" label="名称" sortable></el-table-column>
    <el-table-column prop="start_time" label="开始时间" sortable></el-table-column>
    <el-table-column prop="state" label="状态" sortable></el-table-column>
    <el-table-column label="操作" align="center">
      <template slot-scope="scope">
        <el-button v-if="scope.row.state == '成功'" type="text" size="small" @click="handleDownload(scope.row)">下载结果
        </el-button>
        <el-button type="text" size="small" @click="handleDelete(scope.row)">删除</el-button>
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
    handleDownload(row) {
      this.$axios.get(`/jobs/${row.id}/download`)
        .then(response => {
          const blob = new Blob([response.data], { type: 'application/octet-stream' });
          const link = document.createElement('a');
          link.href = window.URL.createObjectURL(blob);
          // 从header中获取文件名
          let contentDisposition = response.headers['content-disposition'];
          const fileName = contentDisposition && contentDisposition.split('filename=')[1];
          link.download = fileName;
          link.click();
        })
    },
    handleDelete(row) {
      this.$confirm('确定删除该任务吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$axios.delete(`/jobs/${row.id}`)
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
  }
}
</script>
<style scoped>
</style>