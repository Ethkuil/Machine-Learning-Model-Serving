<template>
  <el-table :data="data" :default-sort="{ prop: 'update_time', order: 'descending' }" empty-text="没有任何数据集">
    <!-- id列，提交请求时用 -->
    <el-table-column prop="id" label="id" sortable></el-table-column>
    <el-table-column prop="name" label="名称" sortable></el-table-column>
    <el-table-column prop="type" label="类型" sortable></el-table-column>
    <el-table-column prop="size" label="大小" sortable></el-table-column>
    <el-table-column prop="update_time" label="更新时间" sortable></el-table-column>
    <el-table-column label="操作" align="center">
      <template slot-scope="scope">
        <el-button type="text" size="small" @click="handleDownload(scope.row)">下载</el-button>
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
      // TODO: 下载数据集
    },
    handleDelete(row) {
      this.$confirm('确定删除该数据集吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        // TODO: 删除数据集
        this.$message({
          type: 'success',
          message: '删除成功!'
        })
      }).catch(() => {
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