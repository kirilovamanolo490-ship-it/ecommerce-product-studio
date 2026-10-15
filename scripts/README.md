# 公共辅助脚本

本目录保存公开核心流程需要的辅助工具。商品档案 CLI 位于 `.agents/skills/ecommerce-product-studio/scripts/project.py`，详细字段见[数据约定](../docs/data-contract.md)。

## `setup_editor.py`

用途：下载已固定版本的 yft-design，校验归档，应用本仓库的覆盖文件，建立可安装依赖的运行副本。

```sh
python3 scripts/setup_editor.py --help
python3 scripts/setup_editor.py
# 或明确使用另一个尚不存在的目录：
python3 scripts/setup_editor.py --dest workspace/editor-yft-second
```

默认目标相对于仓库根目录，为 `workspace/editor-yft/`；显式 `--dest` 相对于当前工作目录，也可以是用户指定的完整路径。目标必须不存在，现有目录不会被覆盖。

脚本依次读取 `apps/editor-yft/UPSTREAM.json`、验证固定 codeload URL、下载归档、核对 SHA-256、检查归档根目录/路径/文件类型、解压到临时位置、复制 `overrides/` 与说明文件，最后将结果放入目标目录。失败返回 `1` 并清理本次暂存内容；成功返回 `0`。它不安装依赖、不启动服务、不运行上游脚本，也不访问商品素材。

重建成功后：

```sh
cd workspace/editor-yft
npm ci --ignore-scripts
npm run dev -- --host 127.0.0.1 --port 5178 --strictPort
```

若归档哈希不一致，不要直接去掉验证。先核查是否下载异常或上游归档变化，再决定是否更新来源和重新验证。若目标已存在，继续使用该目录，或指定一个新的目录。网络受限时，先解决对 GitHub codeload 的访问，不把失败的 HTML 页面当源码归档。

## 当前没有的工具

本仓库没有统一的 `generate`、`publish` 或任意商品的 `storyboard → Template[]` 编译命令。具体商品的历史编译和渲染脚本依赖其资产与版式，未纳入公共通用脚本。制作、编辑与交付顺序见[核心工作流](../docs/workflow.md)。
