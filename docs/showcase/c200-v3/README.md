# Tapo C200 · 实际制作效果

这组图片来自本项目 **2026-10-14 实际完成导出的 production-v3**，展示从真实产品参考、功能资料和页面规划，到商品主图、详情模块及可编辑画布的结果。本次更新直接复制原有 PNG，未重新生图或修改画面。

**9 张主图 · 9 个详情模块 · 18 页编辑工程。** 点击下方图片可以查看原尺寸文件。主图均为 1620×1620；详情宽 1620，高度按页面内容分别为 1860 或 2160。

这是仍在迭代的设计案例；场景含 AI 生成内容，并非摄像机实际拍摄画面、客户评价或品牌官方广告。产品为 C200 V1，功能与版本依据见[官方产品页](https://www.tp-link.com/us/home-networking/cloud-camera/tapo-c200/v1/)。

## 主图整套效果

[![C200 第三版九张主图总览](main-overview.png)](main-overview.png)

<table>
  <tr>
    <td width="33%"><a href="main/M01.png"><img src="main/M01.png" alt="M01 商品识别" width="360"></a><br><strong>M01 · 商品识别</strong></td>
    <td width="33%"><a href="main/M02.png"><img src="main/M02.png" alt="M02 云台转动" width="360"></a><br><strong>M02 · 云台转动</strong></td>
    <td width="33%"><a href="main/M03.png"><img src="main/M03.png" alt="M03 镜头与画质信息" width="360"></a><br><strong>M03 · 镜头与画质信息</strong></td>
  </tr>
  <tr>
    <td width="33%"><a href="main/M04.png"><img src="main/M04.png" alt="M04 红外夜视" width="360"></a><br><strong>M04 · 红外夜视</strong></td>
    <td width="33%"><a href="main/M05.png"><img src="main/M05.png" alt="M05 移动侦测通知" width="360"></a><br><strong>M05 · 移动侦测通知</strong></td>
    <td width="33%"><a href="main/M06.png"><img src="main/M06.png" alt="M06 双向语音" width="360"></a><br><strong>M06 · 双向语音</strong></td>
  </tr>
  <tr>
    <td width="33%"><a href="main/M07.png"><img src="main/M07.png" alt="M07 本地存储" width="360"></a><br><strong>M07 · 本地存储</strong></td>
    <td width="33%"><a href="main/M08.png"><img src="main/M08.png" alt="M08 隐私模式" width="360"></a><br><strong>M08 · 隐私模式</strong></td>
    <td width="33%"><a href="main/M09.png"><img src="main/M09.png" alt="M09 尺寸与安装" width="360"></a><br><strong>M09 · 尺寸与安装</strong></td>
  </tr>
</table>

## 详情模块整套效果

[![C200 第三版九个详情模块总览](detail-overview.png)](detail-overview.png)

<table>
  <tr>
    <td width="33%"><a href="detail/D01.png"><img src="detail/D01.png" alt="D01 场景与核心功能" width="360"></a><br><strong>D01 · 场景与核心功能</strong></td>
    <td width="33%"><a href="detail/D02.png"><img src="detail/D02.png" alt="D02 云台操作" width="360"></a><br><strong>D02 · 云台操作</strong></td>
    <td width="33%"><a href="detail/D03.png"><img src="detail/D03.png" alt="D03 侦测区域与提醒" width="360"></a><br><strong>D03 · 侦测区域与提醒</strong></td>
  </tr>
  <tr>
    <td width="33%"><a href="detail/D04.png"><img src="detail/D04.png" alt="D04 夜视条件" width="360"></a><br><strong>D04 · 夜视条件</strong></td>
    <td width="33%"><a href="detail/D05.png"><img src="detail/D05.png" alt="D05 语音与隐私" width="360"></a><br><strong>D05 · 语音与隐私</strong></td>
    <td width="33%"><a href="detail/D06.png"><img src="detail/D06.png" alt="D06 存储与设置" width="360"></a><br><strong>D06 · 存储与设置</strong></td>
  </tr>
  <tr>
    <td width="33%"><a href="detail/D07.png"><img src="detail/D07.png" alt="D07 联网与供电" width="360"></a><br><strong>D07 · 联网与供电</strong></td>
    <td width="33%"><a href="detail/D08.png"><img src="detail/D08.png" alt="D08 尺寸与安装方式" width="360"></a><br><strong>D08 · 尺寸与安装方式</strong></td>
    <td width="33%"><a href="detail/D09.png"><img src="detail/D09.png" alt="D09 规格与包装清单" width="360"></a><br><strong>D09 · 规格与包装清单</strong></td>
  </tr>
</table>

## 实际可编辑画面

下面是当时打开真实 18 页母版的编辑器截图。左侧是页面列表，中间是 M02 云台范围页，文字、图片与图形使用独立对象。

[![真实18页工程在本地编辑器中打开](editor-open.png)](editor-open.png)

当时的 QA 操作包括：将标题“云台转动，灵活查看”改为“云台可转动，App 调整视角”，把房间示意图替换为真实商品照片，切页返回，保存整个项目，关闭后重新打开，再从界面导出 PNG。下图是保存重开后的**测试副本**；替换后的图片尺度是为了检验换图与持久化，不作为新的排版成稿。

<details>
<summary>查看改字、换图并保存重开的实际截图</summary>

[![QA副本保存重开后保留修改标题与替换图片](editor-reopened.png)](editor-reopened.png)

</details>

历史记录与当前母版 SHA-256 已核对，18 页母版保持一致。对应检查步骤和展示图片的来源、尺寸、哈希保存在 [manifest.json](manifest.json)。这证明这些是项目已有输出及记录；本轮没有重新执行完整编辑测试，也没有将设计稿标成商业验收或平台上线成果。

## 文件与使用范围

- `main/`：9 张主图原始 PNG 导出。
- `detail/`：9 个详情模块原始 PNG 导出。
- 两张 `*-overview.png`：当时生成的整套总览。
- `editor-open.png`、`editor-reopened.png`：真实编辑器 QA 截图。
- `manifest.json`：文件来源、像素尺寸、SHA-256 及编辑记录摘要。

公开的是本次选定的效果展示。品牌标识、产品外观与官方资料属于相应权利人；案例不代表品牌背书，也不声明整套素材可任意复用。完整母版、说明书、提示词和输入资料仍保留在本地商品任务中。

[返回项目首页](../../../README.md) · [查看工作流程](../../workflow.md) · [启动本地编辑器](../../../apps/editor-yft/README.md)
