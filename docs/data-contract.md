# 商品任务数据约定与校验范围

以下协议由 `project.py` 使用，版本为 `schema_version: 1`。四份 JSON 均位于商品任务根目录，顶层必须是对象。它们用于事实、策划和状态，不是编辑器原生工程。

## `product.json`：商品与证据

| 字段 | 含义与填写方式 | 当前校验 |
|---|---|---|
| `schema_version` | 整数 `1` | 必须等于 1 |
| `name` | 商品名称 | 必须为非空字符串 |
| `target` | `platform`、`site`、`locale`，未知用 `null` | 保留字段，不自动核验站点规则 |
| `sources` | 来源数组，不能空 | 验证 ID、role、文件路径和可选哈希 |
| `identity_lock` | 由真实照片确认的产品外观约束 | 由人工/Agent 核对，脚本不做视觉识别 |
| `claims` | 事实或营销宣称数组，可以为空 | 验证 ID、正文、状态及 supported 的来源定位 |

来源条目例子：

```json
{
  "id": "src-manual",
  "path": "input/manual.pdf",
  "role": "official_manual",
  "sha256": "填入该文件实际计算得到的64位SHA-256"
}
```

上面的哈希是说明占位，不能原样使用。路径采用相对于任务根目录的 `/` 分隔路径；不能使用绝对路径、反斜线或逃逸任务目录的 `../`。路径必须指向存在的普通文件。若提供 `sha256`，内容必须与文件实际哈希相符；不提供时只给出警告，仍不能证明来源真实性。

可用 Python 标准库计算哈希：

```sh
python3 -c "import hashlib,pathlib; print(hashlib.sha256(pathlib.Path('products/sku-001/input/manual.pdf').read_bytes()).hexdigest())"
```

事实条目例子：

```json
{
  "id": "claim-size",
  "text": "尺寸以该型号说明书标注为准",
  "status": "supported",
  "source_id": "src-manual",
  "locator": "PDF 第6页，尺寸表中本型号一行"
}
```

实际使用时将正文换成已经核实的具体内容。`supported` 是工作流中的核对结果，不能冒充独立检测、认证或平台审核。`pending` 和 `conflicting` 可以保留，但页面不可引用。

## `storyboard.json`：逐页计划

顶层有 `main` 和 `detail` 两个数组。主图最多 9 页；详情不设固定上限。两者都为空时验证返回失败。页面 ID 在两组之间也必须唯一。

| 每页字段 | 类型 | 用途 |
|---|---|---|
| `id` | 非空字符串 | 稳定页面编号，例如 `M01`、`D01` |
| `buyer_question` | 非空字符串 | 买家当下想知道什么 |
| `takeaway` | 非空字符串 | 本页唯一核心结论 |
| `visual_evidence` | 非空字符串 | 哪个画面或真实资料支持结论 |
| `headline` | 字符串，可以为空 | 可见主标题；无字目录图可留空 |
| `body` | 字符串数组 | 可见正文、条件与提示 |
| `claim_ids` | 字符串数组 | 只引用商品档案中 supported 的宣称，可为空 |
| `source_ids` | 非空字符串数组 | 引用本页使用的来源；ID 必须存在 |
| `visual_route` | 枚举字符串 | `real_photo`、`reference_generation` 或 `mixed` |

`real_photo` 表示以实拍为视觉主体；`reference_generation` 表示参考真实商品生成视觉；`mixed` 表示二者结合。无论哪条路线，真实商品制作时都要有产品参考，不能仅靠一段提示词锁定产品身份。

脚本只检查引用是否存在和状态是否允许，不理解图片是否真实、语义是否夸大、证据是否足够。它也不验证某个来源角色一定是商品照片。[结构演示](../examples/README.md)特意使用占位示意，说明“结构通过”不等于“已满足真实制作前提”。

## `style.json`：本套图的视觉规则

初始化包含 `photography`、`typography`、`color`、`composition`，值都为 `null`。实际制作应补充光线与场景、字体来源与层级、色值分工、网格安全区、图片尺度及允许的道具等。

当前脚本只检查这份文件能否读为对象和版本号，不检查设计字段的内容完整性。风格空白时即使其他结构通过，也不能报告设计完成。

## `status.json`：如实记录阶段

初始化值为：

```json
{
  "schema_version": 1,
  "stage": "planning_only",
  "generation": "not_completed",
  "editor_roundtrip": "not_completed",
  "platform_profile": "not_verified"
}
```

脚本不会自动推进状态，也不对后续状态值执行完整状态机校验。可在任务中补充审阅者、日期和证据路径；要在实际操作完成后再更新。若 `stage` 不为 `planning_only`，校验器会提示核对实际阶段，不因此否定已完成任务。

## CLI 与退出码

```sh
python3 .agents/skills/ecommerce-product-studio/scripts/project.py --help
python3 .agents/skills/ecommerce-product-studio/scripts/project.py init --help
python3 .agents/skills/ecommerce-product-studio/scripts/project.py validate --help
```

- `init`：成功 `0`；文件不存在、后缀不支持、空文件、空商品名或目标已存在等情况返回 `1`。
- `validate`：结构通过 `0`；缺文件、JSON 错误、引用/哈希/字段错误或空计划返回 `1`。
- 命令行参数错误由 argparse 处理，通常返回 `2`。

主要防错项包括来源路径越界、重复来源/宣称/页面 ID、缺来源、哈希不符、引用待核实宣称、主图超过 9 页。脚本不联网、不做 OCR、不调用模型、不读凭据、不核验平台规则。
