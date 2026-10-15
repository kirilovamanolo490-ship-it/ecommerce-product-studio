#!/usr/bin/env python3
"""Rebuild the YFT editor workspace from a pinned upstream source archive."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import sys
import tarfile
import tempfile
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parent.parent
APP = ROOT / "apps" / "editor-yft"
OVERRIDES = APP / "overrides"
METADATA = APP / "UPSTREAM.json"
DOC_FILES = ("README.md", "LOCAL-NOTES.md", "LICENSE", "UPSTREAM.json")


def load_metadata() -> dict:
    with METADATA.open("r", encoding="utf-8") as stream:
        metadata = json.load(stream)
    commit = metadata.get("commit", "")
    digest = metadata.get("archive_sha256", "")
    if len(commit) != 40 or any(ch not in "0123456789abcdef" for ch in commit):
        raise ValueError("UPSTREAM.json 中的 commit 必须是 40 位小写十六进制 SHA。")
    if len(digest) != 64 or any(ch not in "0123456789abcdef" for ch in digest):
        raise ValueError("UPSTREAM.json 中的 archive_sha256 必须是 64 位小写十六进制值。")
    expected_url = f"https://codeload.github.com/dromara/yft-design/tar.gz/{commit}"
    if metadata.get("archive_url") != expected_url:
        raise ValueError("UPSTREAM.json 的归档地址与固定上游仓库/commit 不一致。")
    return metadata


def download_archive(url: str, expected_sha256: str, archive_path: Path) -> None:
    request = Request(url, headers={"User-Agent": "editor-workspace-bootstrap/1.0"})
    digest = hashlib.sha256()
    with urlopen(request, timeout=60) as response, archive_path.open("wb") as output:
        while True:
            chunk = response.read(1024 * 1024)
            if not chunk:
                break
            digest.update(chunk)
            output.write(chunk)
    actual = digest.hexdigest()
    if actual != expected_sha256:
        raise ValueError(
            "上游归档 SHA-256 不匹配："
            f"期望 {expected_sha256}，实际 {actual}。已停止，不会解压或生成工作区。"
        )


def extract_archive(archive_path: Path, target: Path, commit: str) -> None:
    expected_root = f"yft-design-{commit}"
    seen_roots: set[str] = set()
    with tarfile.open(archive_path, mode="r:gz") as archive:
        members = archive.getmembers()
        for member in members:
            path = PurePosixPath(member.name)
            if path.is_absolute() or ".." in path.parts or not path.parts:
                raise ValueError(f"归档中出现不安全路径：{member.name!r}")
            seen_roots.add(path.parts[0])
            if not (member.isdir() or member.isfile()):
                raise ValueError(f"归档中出现非普通文件或目录，已拒绝：{member.name!r}")
        if seen_roots != {expected_root}:
            raise ValueError(f"归档根目录不符合预期：{sorted(seen_roots)!r}")

        for member in members:
            relative = PurePosixPath(member.name).parts[1:]
            if not relative:
                continue
            destination = target.joinpath(*relative)
            if member.isdir():
                destination.mkdir(parents=True, exist_ok=True)
                continue
            destination.parent.mkdir(parents=True, exist_ok=True)
            source = archive.extractfile(member)
            if source is None:
                raise ValueError(f"无法读取归档文件：{member.name!r}")
            with source, destination.open("wb") as output:
                shutil.copyfileobj(source, output)


def apply_overrides(workspace: Path) -> None:
    for source in sorted(OVERRIDES.rglob("*")):
        if source.is_dir():
            continue
        relative = source.relative_to(OVERRIDES)
        destination = workspace / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)

    for name in DOC_FILES:
        source = APP / name
        destination = workspace / name
        if source.is_file():
            shutil.copy2(source, destination)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="从固定上游 commit 重建 YFT 本地编辑器工作区，不安装依赖或运行第三方脚本。"
    )
    parser.add_argument(
        "--dest",
        type=Path,
        help="新工作区目标目录；默认是仓库根目录下的 workspace/editor-yft。",
    )
    args = parser.parse_args()

    try:
        metadata = load_metadata()
        destination = (args.dest if args.dest else ROOT / "workspace" / "editor-yft").expanduser()
        destination = destination.resolve()
        if destination.exists():
            raise FileExistsError(f"目标目录已存在，拒绝覆盖：{destination}")

        destination.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="yft-editor-setup-") as temporary:
            temporary_path = Path(temporary)
            archive_path = temporary_path / "upstream.tar.gz"
            stage = Path(tempfile.mkdtemp(prefix=".editor-yft-stage-", dir=destination.parent))
            try:
                download_archive(
                    metadata["archive_url"], metadata["archive_sha256"], archive_path
                )
                extract_archive(archive_path, stage, metadata["commit"])
                apply_overrides(stage)
                if destination.exists():
                    raise FileExistsError(f"目标目录在执行期间出现，拒绝覆盖：{destination}")
                os.replace(stage, destination)
            except Exception:
                shutil.rmtree(stage, ignore_errors=True)
                raise

        print(f"已创建编辑器工作区：{destination}")
        print("脚本未安装依赖，也未执行上游或第三方脚本。")
        return 0
    except Exception as error:
        print(f"setup_editor.py: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
