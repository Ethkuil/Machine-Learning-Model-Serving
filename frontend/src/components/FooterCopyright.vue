<template>
  <el-row type="flex" justify="center" class="copyright">
    Copyright © {{ oldestDevTime }}-{{ latestDevTime }}
  </el-row>
</template>
<script>
export default {
  name: 'FooterCopyright',
  data() {
    return {
      oldestDevTime: '2022',
      latestDevTime: '2022'
    }
  }
}
</script>
<style scoped>
.copyright {
  padding-top: 35px;
  padding-bottom: 35px;
  background-color: #222;
  color: #BBB;
  font-size: 14px;
}
</style>