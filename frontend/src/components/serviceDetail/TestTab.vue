<template>
  <div>
    <el-main class="main">
      <el-row :gutter="20">
        <el-col :span="12">
          <el-card>
            <div slot="header">
              <el-row type="flex" justify="space-between" align="middle">
                <h2 class="card-title">实时预测（快速返回）</h2>
              </el-row>
            </div>

            <el-input type="textarea" v-model="inputJson" :rows="15" :placeholder="'请输入JSON'"></el-input>

            <el-row type="flex" justify="end">
              <el-button type="primary" @click="submit">提 交</el-button>
            </el-row>

          </el-card>
        </el-col>

        <el-col :span="12">
          <el-card>
            <div slot="header">
              <h2 class="card-title">输出</h2>
            </div>
            <json-viewer :value="outputJson" :expand-depth="5" copyable sort />
          </el-card>
        </el-col>
      </el-row>
    </el-main>
  </div>
</template>
<script>
export default {
  data() {
    return {
      inputJson: '',
      outputJson: {
        "result": [
          {
            "predicted_Species": "0",
            "probability_0": "0.5",
            "probability_1": "0.3",
            "probability_2": "0.2"
          }
        ],
      },
    }
  },
  methods: {
    submit() { // TODO 测试
      this.$axios.post(`/services/${this.$route.params.id}/predict`, this.inputJson).then(response => {
        this.outputJson = response.data.data;
        this.$message({
          message: '提交成功',
          type: 'success'
        })
      }).catch(error => {
        this.$message.error(error.response.data.error);
      });
    }
  }
}
</script>
<style scoped>
.main {
  background-color: #f1f2f6
}

.card-title {
  font-size: 18px;
  margin: 0
}

.label {
  font-family: "Roboto", sans-serif
}
</style>