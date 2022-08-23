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
      // TODO. 尚未测试
      this.$axios.get(`/jobs/${row.id}/download`, { responseType: 'blob' })
        .then(response => {
          const blob = new Blob([response.data], { type: 'application/octet-stream' });
          const link = document.createElement('a');
          link.href = window.URL.createObjectURL(blob);
          // 从header中获取文件名
          let contentDisposition = response.headers['content-disposition'];
          const fileName = contentDisposition && contentDisposition.split('filename=')[1];
          link.download = fileName || 'result.csv';
          link.click();
        })
    },
  }
}
</script>
<style scoped>
</style>