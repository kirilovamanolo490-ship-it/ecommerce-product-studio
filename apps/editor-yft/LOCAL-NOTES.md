# 本地画布验证版

> 本文件保留 2026-10-14 的历史技术记录。公开仓库的安装与重建以 [README.md](README.md) 为准；下面提到的研究目录不随核心仓库公开。当前发布验证见 [验证记录](../../docs/verification.md)。

来源：`../../github/yft-design` 的本地快照，MIT 许可证保留在本目录。它是第三方编辑器的运行验证副本，还没有接入本项目的商品档案、分镜或生图队列。

## 启动

本轮用 Node 24.20.0 / npm 11.19.0 执行 `npm install --ignore-scripts`，生成 package-lock.json；仓库原配置声明 Node 18.19.0。开发服务器仅绑定 127.0.0.1：

```sh
npm run dev -- --host 127.0.0.1 --port 5178 --strictPort
```

打开 http://127.0.0.1:5178/ 。这是本地开发服务，停止后按上面命令重新启动。未部署外网。

首次使用关闭引导弹窗；左侧编辑面板可能折叠，点击蓝色箭头展开。标题可双击改字；“上传文件”可选择本地 PNG/JPEG/SVG 或添加一页工程 JSON；“打开项目 JSON”会用单个 Template 或 Template[] 文件替换当前浏览器工作区；选中图片后可替换图片；右上角“下载”可导出单页/整套 JSON 或 PNG/SVG。

## 本轮最小修复

1. `src/views/Editor/CanvasRight/ElementStylePanel/TextboxStylePanel.vue`：OpenType.js 使用 namespace 导入，字体解析改 fetch + parse，消除路由初始化白屏。
2. `src/views/Editor/CanvasLeft/Menu/components/EditorPool.vue`：SVG/JSON/本地图片/MP4 处理完成即返回；避免又进入后台上传。JSON 等待模板导入再调整画布。
3. `src/hooks/useCanvasExport.ts`：保存模板 id/version/clip 与背景字段，保留 JSON 重开所需元数据。
4. `src/views/Editor/CanvasLeft/Menu/components/EditorPool.vue` / `src/hooks/useHandleTemplate.ts`：本地 JSON 文件可导入一个 Template 或 Template[] 页面数组；数组导入仍是浏览器本地操作，不会发送到后端。
5. `src/views/Editor/CanvasLeft/Menu/components/EditorPool.vue`：独立“打开项目 JSON”文件选择器校验页面/图层ID和画布元数据，并确认后替换当前浏览器工作区、复位到第1页；不改磁盘文件。
6. `src/store/modules/template.ts` / `src/hooks/useCanvasExport.ts`：切页/增删页/排序前同步活动 Fabric 画布；整套 JSON 导出为保留顺序与原页面ID的 Template 数组。
7. `src/components/FileExport/ExportImage.vue`：全部页面图片导出仍未实现，按钮已禁用并说明只导出当前页。

## 浏览器验证（2026-10-14）

使用 Playwright 和本机 Chrome，1440×1000。当前会话无 Browser 插件技能，因此使用普通 Playwright；内置 Chromium 浏览器缓存缺失，改用已安装 Chrome。测试素材为上游项目自带图标，仅作技术测试，不是商品宣传设计。

- 页面显示正常，没有框架错误遮罩。
- 添加标题 → 双击改中文 → 拖动，对象内容与坐标实际变化。
- 插入本地图片 → 替换同一图片对象，对象 ID 保持且图片数据改变。
- 从界面导出 JSON，确认有独立文字对象和嵌入图片数据。
- 关闭页面，打开新页面，从界面导入 JSON，恢复对象并再次改字。
- 修改后从界面导出 PNG，得到非空输出文件。
- 测试过程没有 POST 请求、没有浏览器应用错误；有上游 Fabric 警告 `Setting type has no effect Image`。

机器可读检查见 `../../research/validation.json`。不是真实商品成图质量验收。

## 尚未覆盖

在线模板、素材、字体服务指向 `127.0.0.1:8789`，该后台未部署；PDF/PSD 转换依赖后台，不能承诺开箱可用。未实测 AI 抠图、字体转曲、视频、多页批量导出、手机端编辑、跨浏览器与多商品批量任务。

`vue-tsc --noEmit` 受上游现有 TS6504 配置问题阻断（`CanvasTour/index.vue.js`）；正式生产构建未验收。因此当前状态是“本地编辑核心闭环通过的技术底座”，不是可直接商用发布的一体化软件。

接入时需要把 storyboard 转为实际 Fabric/编辑器对象，设定商品图画布尺寸，保存主图/详情的页面顺序和素材路径，并检查导出的全部页面。当前默认示例画布不是电商尺寸模板。
