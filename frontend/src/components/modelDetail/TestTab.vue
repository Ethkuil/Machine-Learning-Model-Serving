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
              <template v-for="(input_variable, index) in input_variables">
                <el-form-item prop="inputVariable.value">
                  <template slot="label">
                    <span class="label">{{ input_variable.field }}</span>
                  </template>
                  <el-checkbox v-model="input_variable.is_file">文件</el-checkbox>
                  <el-input v-if="!input_variable.is_file" v-model="input_variable.actual_value"
                    :placeholder="input_variable.data_type">
                  </el-input>
                  <!-- 不自动上传 -->
                  <el-upload v-else action="nothing" :auto-upload="false" :on-change="handleChange">
                    <el-button type="primary" icon="el-icon-upload2"></el-button>
                  </el-upload>
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
            <el-button type="primary" @click="submitJson()">提 交</el-button>
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
    input_variables: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      dialogInputJsonVisible: false,
      inputJson: null,
      outputJson: {},
    }
  },
  methods: {
    clearInputVariables() {
      this.input_variables.forEach(inputVariable => {
        inputVariable.actual_value = '';
      });
    },
    submitJson() {
      this.dialogInputJsonVisible = false;
      this.$axios.post(`/models/${this.$route.params.id}/predict`, this.inputJson, {
        headers: {
          'Content-Type': 'application/json'
        }
      }).then(response => {
        this.outputJson = response.data.data;
      })
      this.$message({
        message: '提交成功！',
        type: 'success'
      });
    },
    submit() {
      let input = {};
      this.input_variables.forEach(inputVariable => {
        input[inputVariable.field] = inputVariable.actual_value;
      });
      this.$axios.post(`/models/${this.$route.params.id}/predict`, input, {
        headers: {
          'Content-Type': 'multi-part/form-data'
        }
      }).then(response => {
        this.outputJson = response.data.data;
      })
      this.$message({
        message: '提交成功！',
        type: 'success'
      });
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