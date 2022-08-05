<template>
  <div>
    <el-main class="main">
      <el-row :gutter="20">
        <el-col :span="12">
          <el-card>
            <div slot="header">
              <el-row type="flex" justify="space-between" align="middle">
                <h2 class="card-title">输入</h2>
                <el-button type="text" @click="dialogInputJsonVisible = true">JSON</el-button>
              </el-row>
            </div>
            <el-form>
              <template v-for="(inputVariable, index) in inputVariablesData">
                <el-form-item prop="inputVariable.value">
                  <template slot="label">
                    <span class="label">{{ inputVariable.field }}</span>
                  </template>
                  <el-input v-model="inputVariable.value" :placeholder="inputVariable.type">
                  </el-input>
                </el-form-item>
              </template>
            </el-form>
            <el-row type="flex" justify="end">
              <el-button @click="clearInputVariables">清 除</el-button>
              <el-button type="primary" @click="submit">提 交</el-button>
            </el-row>
          </el-card>
        </el-col>

        <el-dialog title="输入JSON" :visible.sync="dialogInputJsonVisible">
          <el-input type="textarea" v-model="inputJson" :rows="15" :placeholder="'请输入JSON'"></el-input>
          <div slot="footer" class="dialog-footer">
            <el-button @click="dialogInputJsonVisible = false">取 消</el-button>
            <el-button type="primary" @click="submitJsonStr()">提 交</el-button>
          </div>
        </el-dialog>

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
  props: {
    inputVariablesData: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      dialogInputJsonVisible: false,
      inputJson: null,
      outputJson: {
        "result": [
          {
            "predicted_Species": "0",
            "probability_0": "0.5",
            "probability_1": "0.3",
            "probability_2": "0.2"
          }
        ],
        "stderr": [],
        "stdout": []
      },
    }
  },
  methods: {
    clearInputVariables() {
      this.inputVariablesData.forEach(inputVariable => {
        inputVariable.value = '';
      });
    },
    submitJson() {
      // TODO: 提交inputJson
      // 从后端获取输出的JSON
      this.$message({
        message: '提交成功！',
        type: 'success'
      });
    },
    submitJsonStr() {
      this.dialogInputJsonVisible = false;
      // TODO: 可能需要从字符串转换为json对象
      this.submitJson();
    },
    submit() {
      // TODO: 提交由inputVariablesData部分内容得到的JSON
      this.submitJson();
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

.label {
  font-family: "Roboto", sans-serif;
}
</style>