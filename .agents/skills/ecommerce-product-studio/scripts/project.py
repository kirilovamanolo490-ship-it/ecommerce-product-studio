#!/usr/bin/env python3
"""建立并检查商品视觉任务档案；不解码图片、不联网、不生成图片。"""

import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path, PureWindowsPath


SCHEMA_VERSION = 1
IMAGE_EXTENSIONS = {
    ".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp", ".tif", ".tiff",
    ".heic", ".heif", ".avif",
}
REQUIRED_FILES = ("product.json", "storyboard.json", "style.json", "status.json")
VISUAL_ROUTES = {"real_photo", "reference_generation", "mixed"}


def sha256_file(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def init_project(args):
    target = Path(args.directory).expanduser()
    image = Path(args.image).expanduser()
    if not args.name.strip():
        raise ValueError("商品名不能为空")
    if target.exists():
        raise ValueError(f"目标目录已存在，拒绝覆盖：{target}")
    if not image.is_file():
        raise ValueError(f"图片文件不存在或不是普通文件：{image}")
    if image.suffix.lower() not in IMAGE_EXTENSIONS:
        raise ValueError("图片后缀不受支持；支持 jpg/jpeg/png/webp/gif/bmp/tif/tiff/heic/heif/avif")
    if image.stat().st_size == 0:
        raise ValueError("图片文件为空")

    target.parent.mkdir(parents=True, exist_ok=True)
    target.mkdir(exist_ok=False)
    try:
        for folder in ("input", "assets", "masters", "exports", "qa"):
            (target / folder).mkdir()
        suffix = image.suffix.lower()
        copied = target / "input" / f"source-01{suffix}"
        shutil.copy2(image, copied)
        source = {
            "id": "src-01",
            "path": copied.relative_to(target).as_posix(),
            "role": "original_product_image",
            "sha256": sha256_file(copied),
        }
        write_json(target / "product.json", {"schema_version": 1, "name": args.name,
            "target": {"platform": None, "site": None, "locale": None}, "sources": [source],
            "identity_lock": [], "claims": []})
        write_json(target / "storyboard.json", {"schema_version": 1, "main": [], "detail": []})
        write_json(target / "style.json", {"schema_version": 1, "photography": None,
            "typography": None, "color": None, "composition": None})
        write_json(target / "status.json", {"schema_version": 1, "stage": "planning_only",
            "generation": "not_completed", "editor_roundtrip": "not_completed",
            "platform_profile": "not_verified"})
    except Exception:
        shutil.rmtree(target, ignore_errors=True)
        raise

    print(f"已初始化任务目录：{target}")
    print(f"已复制原图并记录 SHA-256：{source['path']}")
    print("图片仅按后缀和非空检查，未进行解码校验；任务状态仍为 planning_only。")
    return 0


class Validator:
    def __init__(self, root):
        self.root = root.resolve()
        self.errors = []
        self.warnings = []

    def error(self, message):
        self.errors.append(message)

    def load_json(self, filename):
        path = self.root / filename
        if not path.is_file():
            self.error(f"缺少必需文件：{filename}")
            return None
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            self.error(f"{filename} 无法读取有效 JSON：{exc}")
            return None
        if not isinstance(value, dict):
            self.error(f"{filename} 顶层必须是对象")
            return None
        if type(value.get("schema_version")) is not int or value["schema_version"] != SCHEMA_VERSION:
            self.error(f"{filename} schema_version 必须为 1")
        return value

    def source_file(self, source, label):
        rel = source.get("path")
        if not isinstance(rel, str) or not rel.strip():
            self.error(f"{label} 缺少有效 path")
            return None
        if "\\" in rel or Path(rel).is_absolute() or PureWindowsPath(rel).is_absolute():
            self.error(f"{label} path 必须是任务目录内的相对路径：{rel}")
            return None
        candidate = (self.root / rel).resolve()
        try:
            candidate.relative_to(self.root)
        except ValueError:
            self.error(f"{label} path 逃逸任务目录：{rel}")
            return None
        if not candidate.is_file():
            self.error(f"{label} 文件不存在：{rel}")
            return None
        expected = source.get("sha256")
        if expected is not None:
            if not isinstance(expected, str) or len(expected) != 64:
                self.error(f"{label} sha256 格式无效")
            elif sha256_file(candidate) != expected.lower():
                self.error(f"{label} SHA-256 与文件不符：{rel}")
        else:
            self.warnings.append(f"{label} 未记录 sha256，无法检查内容是否变化")
        return candidate

    def validate(self):
        docs = {name: self.load_json(name) for name in REQUIRED_FILES}
        product = docs.get("product.json")
        board = docs.get("storyboard.json")
        status = docs.get("status.json")
        sources = {}
        claims = {}

        if product is not None:
            if not isinstance(product.get("name"), str) or not product["name"].strip(): self.error("product.json name 必须是非空字符串")
            raw_sources = product.get("sources")
            if not isinstance(raw_sources, list):
                self.error("product.json sources 必须是数组")
                raw_sources = []
            elif not raw_sources:
                self.error("product.json sources 不能为空")
            for index, item in enumerate(raw_sources):
                label = f"source[{index}]"
                if not isinstance(item, dict):
                    self.error(f"{label} 必须是对象")
                    continue
                sid = item.get("id")
                if not isinstance(sid, str) or not sid.strip():
                    self.error(f"{label} id 必须是非空字符串")
                    continue
                if sid in sources:
                    self.error(f"来源 id 重复：{sid}")
                    continue
                role = item.get("role")
                if not isinstance(role, str) or not role.strip():
                    self.error(f"{label} role 必须是非空字符串")
                sources[sid] = item
                self.source_file(item, label)
            raw_claims = product.get("claims")
            if not isinstance(raw_claims, list):
                self.error("product.json claims 必须是数组")
                raw_claims = []
            for index, item in enumerate(raw_claims):
                label = f"claim[{index}]"
                if not isinstance(item, dict):
                    self.error(f"{label} 必须是对象")
                    continue
                cid, text, state = item.get("id"), item.get("text"), item.get("status")
                if not isinstance(cid, str) or not cid.strip():
                    self.error(f"{label} id 必须是非空字符串")
                    continue
                if cid in claims:
                    self.error(f"claim id 重复：{cid}")
                    continue
                if not isinstance(text, str) or not text.strip(): self.error(f"{label} text 必须是非空字符串")
                if not isinstance(state, str) or state not in ("supported", "pending", "conflicting"): self.error(f"{label} status 必须是 supported/pending/conflicting")
                if state == "supported":
                    sid = item.get("source_id")
                    if not isinstance(sid, str) or sid not in sources: self.error(f"{label} supported 来源不存在：{sid}")
                    locator = item.get("locator")
                    if not isinstance(locator, str) or not locator.strip(): self.error(f"{label} supported 必须有 locator")
                claims[cid] = item

        if board is not None:
            pages = []
            for section in ("main", "detail"):
                items = board.get(section)
                if not isinstance(items, list):
                    self.error(f"storyboard.json {section} 必须是数组")
                    items = []
                if section == "main" and len(items) > 9:
                    self.error(f"主图共 {len(items)} 张，最多允许 9 张")
                pages.extend((section, i, page) for i, page in enumerate(items))
            page_ids = set()
            for section, index, page in pages:
                label = f"{section}[{index}]"
                if not isinstance(page, dict):
                    self.error(f"{label} 必须是对象")
                    continue
                pid = page.get("id")
                if not isinstance(pid, str) or not pid.strip():
                    self.error(f"{label} id 必须是非空字符串")
                elif pid in page_ids:
                    self.error(f"页面 id 全局重复：{pid}")
                else:
                    page_ids.add(pid)
                for key in ("buyer_question", "takeaway", "visual_evidence"):
                    value = page.get(key)
                    if not isinstance(value, str) or not value.strip(): self.error(f"{label} {key} 必须是非空字符串")
                if not isinstance(page.get("headline"), str): self.error(f"{label} headline 必须是字符串（可为空）")
                body = page.get("body")
                if not isinstance(body, list) or any(not isinstance(x, str) for x in body): self.error(f"{label} body 必须是字符串数组")
                for key in ("claim_ids", "source_ids"):
                    if not isinstance(page.get(key), list) or any(not isinstance(x, str) for x in page[key]): self.error(f"{label} {key} 必须是字符串数组")
                source_ids = page.get("source_ids")
                if isinstance(source_ids, list) and not source_ids:
                    self.error(f"{label} 至少需要一个 source_ids（页面需使用真实产品参考）")
                if not isinstance(page.get("visual_route"), str) or page.get("visual_route") not in VISUAL_ROUTES:
                    self.error(f"{label} visual_route 必须是 real_photo/reference_generation/mixed")
                for cid in page.get("claim_ids", []) if isinstance(page.get("claim_ids"), list) else []:
                    if not isinstance(cid, str):
                        self.error(f"{label} claim_ids 只允许字符串 id")
                        continue
                    claim = claims.get(cid)
                    if claim is None: self.error(f"{label} 引用了不存在的 claim：{cid}")
                    elif claim.get("status") != "supported": self.error(f"{label} 只能引用 supported claim：{cid}")
                for sid in page.get("source_ids", []) if isinstance(page.get("source_ids"), list) else []:
                    if not isinstance(sid, str):
                        self.error(f"{label} source_ids 只允许字符串 id")
                        continue
                    if sid not in sources: self.error(f"{label} 引用了不存在的 source：{sid}")
            if not board.get("main") and not board.get("detail"):
                self.warnings.append("空计划：尚未规划主图或详情页")

        if status is not None and status.get("stage") != "planning_only":
            self.warnings.append("当前状态不是 planning_only；请核对是否已实际生成并记录阶段")
        for warning in self.warnings:
            print(f"警告：{warning}")
        for error in self.errors:
            print(f"错误：{error}")
        if self.errors:
            print(f"验证失败：{len(self.errors)} 项错误。结构检查不等于画质、事实或平台合规验证。")
            return 1
        if board is not None and not board.get("main") and not board.get("detail"):
            print("验证未通过：计划为空，需先规划页面。")
            return 1
        print("结构验证通过；不代表事实真实性、图片质量或平台合规已完成。")
        return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description="商品视觉任务档案初始化与结构验证")
    sub = parser.add_subparsers(dest="command", required=True)
    init = sub.add_parser("init", help="创建新任务目录并登记一张原始商品图")
    init.add_argument("directory")
    init.add_argument("--name", required=True)
    init.add_argument("--image", required=True)
    validate = sub.add_parser("validate", help="检查 JSON、来源、引用及分镜结构")
    validate.add_argument("directory")
    args = parser.parse_args(argv)
    try:
        if args.command == "init":
            return init_project(args)
        root = Path(args.directory).expanduser()
        if not root.is_dir():
            raise ValueError(f"任务目录不存在：{root}")
        return Validator(root).validate()
    except (OSError, ValueError) as exc:
        print(f"错误：{exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
