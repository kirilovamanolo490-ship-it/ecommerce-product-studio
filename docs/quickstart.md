# 快速开始

先跑任务档案，再按需要启动可视化编辑器。Python 部分不依赖 Node、不需要 API key，也不会调用图像服务。

## 1. 准备环境

| 组件 | 用途 | 要求 |
|---|---|---|
| Python | 初始化、校验、重建编辑器 | Python 3.9+，标准库即可 |
| Git | 克隆公开仓库 | 可用的 Git 命令 |
| Node 与 npm | 编辑器开发服务 | 上游声明 Node 18.19.0；本地历史环境为 Node 24.20.0/npm 11.19.0，不代表所有版本均已验证 |
| 桌面浏览器 | 画布与实际编辑验收 | 历史验证使用 Chrome；其他浏览器需复验 |
| 图像生成工具 | 商品视觉生成/局部修改 | 由运行任务的环境提供，仓库不附带模型或凭据 |

```sh
git clone https://github.com/kirilovamanolo490-ship-it/ecommerce-product-studio.git
cd ecommerce-product-studio
python3 --version
```

除特别注明外，后续命令均从仓库根目录执行。

## 2. 先运行结构示例

```sh
python3 .agents/skills/ecommerce-product-studio/scripts/project.py validate examples/planning-only
```

应输出“结构验证通过”，返回退出码 `0`。此示例采用程序生成的占位图和演示资料，仅用于展示文件协议；它不是可销售商品，也不是 AI 生图结果。

## 3. 新建真实商品任务

```sh
python3 .agents/skills/ecommerce-product-studio/scripts/project.py init products/sku-001 \
  --name '你的商品名称' --image '/path/to/your-product.jpg'
```

把示例路径替换成存在的文件。路径有空格时保留引号。命令会建立任务文件、复制图片、记录哈希；不会修改原图。目标路径已存在则拒绝覆盖。

接着实际查看图片，复制补充手册到 `input/` 并登记来源。填写商品身份、事实宣称、逐页分镜与风格，再运行：

```sh
python3 .agents/skills/ecommerce-product-studio/scripts/project.py validate products/sku-001
```

刚初始化的分镜为空，返回 `1` 是预期。填写方法见[数据约定](data-contract.md)。通过后仍须继续核对事实和画面。

## 4. 让 Agent 执行策划与制作

让 Agent 阅读 [.agents/skills/ecommerce-product-studio/SKILL.md](../.agents/skills/ecommerce-product-studio/SKILL.md)，提供商品目录和目标渠道。执行顺序如下：

1. 看原图和完整相关资料，记录已知、未知与冲突。
2. 先写购买逻辑，再写逐页视觉内容，不为凑满 9 张重复卖点。
3. 先形成主视觉及一张信息页的方向，内部检查后扩展。
4. 生图携带真实产品参考；把精确文案留给独立文本层。
5. 将视觉资产、文字和标注排进原生画布，保留版本。

当前没有统一的模型 provider 配置文件。执行者应明确实际使用的服务与输入素材；不要把“文件在本地”理解为“离线推理”。没有图像工具时可以完成档案和策划，但应如实停在该阶段，不能伪称已经生成。

## 5. 重建并启动编辑器

公开仓库保存固定上游版本和本地覆盖文件，完整运行副本在 `workspace/` 中重建：

```sh
python3 scripts/setup_editor.py
cd workspace/editor-yft
npm ci --ignore-scripts
npm run dev -- --host 127.0.0.1 --port 5178 --strictPort
```

打开 `http://127.0.0.1:5178/`。服务占用当前终端，结束时按 Ctrl+C。`--strictPort` 确保端口被占用时报错，不会悄悄换到另一个地址。不要把此开发服务当作外网部署。

重建脚本需要联网下载固定上游源码，不会安装 npm 依赖或运行其脚本；已存在的目标目录会拒绝覆盖。详细下载、来源和本地修改说明见[编辑器 README](../apps/editor-yft/README.md)。

## 6. 试一次原生画布操作

在编辑器左侧“编辑”面板选择“打开项目 JSON”，打开 `examples/editor-demo.json`。这是两页演示，包含独立标题、图片与背景对象。打开项目会替换当前浏览器画布，先保存已有工作。

改动第一页标题，切到第二页再返回；用你自己的图片替换演示图。通过“保存整个项目 JSON”下载新文件，关闭页面后重新打开该文件，确认文字、图片、页数和顺序都保持，最后从界面导出当前页 PNG。

这些操作须真实完成后才能标记编辑验收通过。输入的照片内部仍是位图，独立文本和外加标注才是对象层。详见[验收规范](quality-and-delivery.md)。

## 常见问题

| 情况 | 原因与处理 |
|---|---|
| `目标目录已存在` | 初始化或重建保护已有文件，换一个新目录，或继续维护现有任务 |
| `计划为空` | 尚未填写主图和详情页；不是 Python 安装失败 |
| `SHA-256 与文件不符` | 源文件发生变化。先确认改动来源，再登记新版本，不直接清空哈希掩盖问题 |
| 页面引用 pending/conflicting claim | 先补证据并人工核实，或从页面删除该宣称 |
| 编辑器不能导入 storyboard | 策划协议与原生画布格式不同，使用真正的 Template/Template[] 工程 |
| 在线模板/字体/PDF/PSD 不可用 | 这些功能可能需要未部署后台，核心本地编辑不代表所有在线服务可用 |
| 字体换行不同 | 字体依赖设备与授权资源，替换为有权使用且可取得的字体并重新检查 |
| 主图输出不符合平台限制 | 当前是内部制作规格，需按实际平台、站点和类目重新适配 |
