# 商品任务目录

每款商品使用一个独立目录，例如 `products/sku-001/`。这里存放你实际制作的任务；公开仓库只保留本说明，任务目录默认被 Git 忽略。仓库提供的无品牌示例放在 [examples](../examples/README.md)。

## 最低输入

至少准备一张可读取的真实商品图和商品名称。建议同时提供型号/SKU、说明书、参数表、品牌文件、已有文案，以及目标平台、站点、语言。没有提供的信息保留未知；不能从一张正面图推断背面、内部结构或全部配件。

## 建立任务

在仓库根目录执行：

```sh
python3 .agents/skills/ecommerce-product-studio/scripts/project.py init products/sku-001 \
  --name '商品名称' --image '/path/to/your-product.jpg'
```

脚本只使用 Python 标准库，不联网、不生图、不上传。它检查图片后缀和非空，将原文件复制到 `input/source-01.<后缀>` 并记录 SHA-256；原文件保持不变。它不解码图片，因此初始化成功后仍须打开图片确认可用。

目标目录已存在时脚本拒绝覆盖。选择新编号或手动维护原任务，不要为了重跑初始化删除已有成果。

## 文件放在哪里

| 文件或目录 | 保存内容 | 谁负责维护 |
|---|---|---|
| `product.json` | 名称、目标渠道、来源、身份锁、事实宣称 | Agent 与资料核对者 |
| `storyboard.json` | 主图/详情逐页问题、结论、文案、引用和视觉路线 | 策划与设计 |
| `style.json` | 摄影、字体、色彩、布局等统一规则 | 设计 |
| `status.json` | 制作、编辑闭环与平台适配状态 | 当前任务执行者 |
| `input/` | 原图、手册、规格、用户文案的副本 | 素材接收环节 |
| `assets/` | 无文字视觉、产品图层、背景、生成记录 | 视觉制作环节 |
| `masters/` | 编辑器原生 JSON、关联资源和版本 | 排版与改稿环节 |
| `exports/` | 供审阅或后续上传的 PNG/JPEG | 导出环节 |
| `qa/` | 整套总览、逐页问题、编辑闭环副本、检查结果 | 复核环节 |

原始输入不覆盖。新版资产、母版和成图使用明确版本名，如 `campaign-v02.json`；改字换图测试保存到 `qa/`，避免污染正式母版。

## 补资料与规划

1. 把新增手册复制到 `input/`，在 `product.json.sources` 登记独立 ID、任务内相对路径、角色与哈希。
2. 阅读图片与手册，把外观约束写入 `identity_lock`。
3. 每条宣称用 `claims` 记录正文、状态、来源 ID 和页码/原句位置。只有 `supported` 的内容才能被页面引用。
4. 给每页填写 `buyer_question`、`takeaway`、`visual_evidence`、`headline`、`body`、`claim_ids`、`source_ids` 和 `visual_route`。
5. 主图最多 9 页，详情按信息量安排；主图与详情 ID 不可重复。

完整字段说明和示例见[数据约定](../docs/data-contract.md)。`style.json` 需要实际设计值，初始化的空字段不代表设计已完成。

## 校验与下一步

```sh
python3 .agents/skills/ecommerce-product-studio/scripts/project.py validate products/sku-001
```

退出码 `0` 表示结构检查通过；`1` 表示失败或计划为空。检查通过后，按[核心工作流](../docs/workflow.md)进行生成、排版和验收。脚本不会自动推进 `status.json`，也不会证明事实真实、图像美观或平台合规。

`storyboard.json` 不能直接在 yft 编辑器打开。先把分镜做成画布对象，再用原生工程完成改字、换图、保存重开和导出。

## 本地与公开边界

所有商品任务默认留在本地。若以后要公开某个案例，应单独检查素材授权、隐私、文案和生成记录，不要用 `git add -f products/` 批量绕过忽略规则。平台发布是独立任务，保存到 `exports/` 不等于已上架。
