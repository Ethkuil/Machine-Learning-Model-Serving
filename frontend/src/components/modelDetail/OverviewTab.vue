<template>
  <div>
    <el-main class="main">
      <el-row :gutter="20">
        <el-col :span="12">
          <el-card>
            <div slot="header">
              <h2 class="card-title">输入变量</h2>
            </div>
            <el-table :data="input_variables" border stripe empty-text="没有任何输入变量">
              <el-table-column label="字段" prop="field"></el-table-column>
              <el-table-column label="类型" prop="data_type"></el-table-column>
              <el-table-column label="测量" prop="op_type"></el-table-column>
              <el-table-column label="维数" prop="shape"></el-table-column>
              <el-table-column label="取值" prop="value"></el-table-column>
            </el-table>
          </el-card>
        </el-col>

        <el-col :span="12">
          <el-card>
            <div slot="header">
              <h2 class="card-title">目标变量</h2>
            </div>
            <el-table :data="target_variables" border stripe empty-text="没有任何目标变量">
              <el-table-column label="字段" prop="field"></el-table-column>
              <el-table-column label="类型" prop="data_type"></el-table-column>
              <el-table-column label="测量" prop="op_type"></el-table-column>
              <el-table-column label="维数" prop="shape"></el-table-column>
              <el-table-column label="取值" prop="value"></el-table-column>
            </el-table>
          </el-card>
        </el-col>

      </el-row>
    </el-main>
  </div>
</template>
<script>
export default {
  props: {
    input_variables: {
      type: Array,
      default: () => []
    },
    target_variables: {
      type: Array,
      default: () => []
    }
  }
}
</script>

<style scoped>
.main {
  background-color: #f1f2f6;
}

.card-title {
  font-size: 18px;
  margin: 0;
}
</style>