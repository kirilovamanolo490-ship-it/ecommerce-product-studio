# 商品任务数据约定 v1

此协议用于事实与计划，不是某个画布编辑器的原生文件格式。

`product.json`：

- `schema_version` 为 1，`name` 为商品名。
- `target` 保存 platform/site/locale；未知字段保持 null。
- `sources` 为非空数组：`id`、任务内相对 `path`、非空 `role`、`sha256`（可选）。图像/手册/文字均需登记。文件必须存在。
- `identity_lock` 是从真实图片观察后填写的不可改变项列表；初始化留空不算识别成功。
- `claims` 数组：`id`、`text`、`status`、`source_id`、`locator`。`status` 取 supported / pending / conflicting。supported 表示已对照该来源确认，不表示外部检测或平台审核通过；locator 用页码、原句或图中具体位置。

`storyboard.json`：

- `schema_version: 1`，`main` 数组最多 9 项，`detail` 数组不设固定上限。
- 每项包括 `id`、`buyer_question`、`takeaway`、`visual_evidence`、`headline`、`body`（字符串数组）、`claim_ids`、`source_ids`、`visual_route`。
- `visual_route` 取 real_photo / reference_generation / mixed；各路线至少引用一个 `source_ids`。图片素材要真实登记；将 AI 修图过程记录到 assets 中的生成清单。
- `claim_ids` 只引用 supported 的宣称；纯氛围图片可以不含宣称。引用完整不证明文案本身没有扩大结论，仍要语义检查。
- `takeaway` 可以是内部页面目标，尚未确认的具体数值不能混入可见 `headline` / `body`。
- 页面 ID 在主图和详情之间全局唯一。新建任务的空数组代表尚未规划。

`style.json`：本套图的摄影、字体、色彩、构图规范；初始化只有空值。`status.json` 初始明确 planning_only，并将 generation/editor_roundtrip/platform_profile 标为未完成。

目录：`input/` 原始素材副本；`assets/` 已生成/处理素材；`masters/` 实际编辑器文件及资源；`exports/` 输出图片；`qa/` 视觉核查与总览。规划数据不放到平台图片中。

`project.py validate` 检查文件完整性、引用、来源哈希、主图数量和必填页面字段；不联网、不生图、不读取 API key，不做 OCR 或自动证据真实性判决。
