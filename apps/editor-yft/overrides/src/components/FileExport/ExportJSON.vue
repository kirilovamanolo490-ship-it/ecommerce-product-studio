<template>
  <div class="export-json-dialog">
    <div class="preview">
      <pre>{{ getJSONData() }}</pre>
    </div>
    <div class="btns">
      <el-button class="btn export" type="primary" @click="exportJSON()">导出当前页 JSON</el-button>
      <el-button class="btn export-project" type="success" @click="exportProjectJSON()">保存整个项目 JSON</el-button>
      <el-button class="btn close" @click="emit('close')">关闭</el-button>
    </div>
  </div>
</template>

<script lang="ts" setup>
import useCanvasExport from '@/hooks/useCanvasExport'

const emit = defineEmits<{(event: 'close'): void}>()

const { exportJSON, exportProjectJSON, getJSONData } = useCanvasExport()

</script>

<style lang="scss" scoped>
.export-json-dialog {
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  position: relative;
  overflow: hidden;
}
.preview {
  width: 100%;
  height: calc(100% - 100px);
  display: flex;
  flex-direction: column;
  justify-content: center;
  background-color: #f9f9f9;
  color: #0451a5;
  pre {
    margin: 0;
  }
}
.btns {
  width: 440px;
  height: 100px;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;

  .export {
    flex: 1;
  }
  .export-project {
    flex: 1.25;
  }
  .close {
    width: 100px;
    flex-shrink: 0;
  }
}
::-webkit-scrollbar {
  width: 10px;
  height: 10px;
  background-color: #f9f9f9;
}
::-webkit-scrollbar-thumb {
  background-color: #c1c1c1;
}
</style>
<style>
.preview svg {
  width: 100%;
  height: 100%;
}
</style>
