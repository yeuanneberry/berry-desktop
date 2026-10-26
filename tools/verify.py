#!/usr/bin/env python3
"""Read-only, bounded candidate integrity checks; never launch selected config."""
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys

ROOT = Path(__file__).resolve().parent.parent


def verify(root):
    failures = []
    manifest = json.loads((root / "source-selection.json").read_text())
    selected = set()
    verified_bodies = {}
    for item in manifest["files"]:
        name = item["path"]
        rel = PurePosixPath(name)
        if rel.is_absolute() or ".." in rel.parts or rel.parts[0] not in {"config", "themes"}:
            failures.append("invalid selected path")
            continue
        if name in selected:
            failures.append("duplicate selected path")
        selected.add(name)
        path = root / name
        if any((root.joinpath(*rel.parts[:i])).is_symlink() for i in range(1, len(rel.parts) + 1)):
            failures.append(f"symlink boundary: {name}")
            continue
        if not path.is_file():
            failures.append(f"missing: {name}")
            continue
        body = path.read_bytes()
        if hashlib.sha256(body).hexdigest() != item["sha256"]:
            failures.append(f"source drift: {name}")
            continue
        verified_bodies[name] = body
        text = body.decode("utf-8")
        if re.search(r"/home/[^\s]+|/mnt/|https?://|berry-session|roblox|berry-lock", text):
            failures.append(f"unexpected machine/runtime dependency: {name}")
    actual = {p.relative_to(root).as_posix() for base in ("config", "themes") for p in (root / base).rglob("*") if p.is_file() or p.is_symlink()}
    if actual != selected:
        failures.append("configuration inventory differs from allowlist")
    waybar_body = verified_bodies.get("config/waybar/config.json")
    if waybar_body is not None:
        waybar = json.loads(waybar_body)
        if any(str(key).startswith("custom/") for key in waybar):
            failures.append("unexpected custom Waybar helper module")
    for guide in [root / "README.md", *sorted((root / "docs").glob("*.md"))]:
        for target in re.findall(r"\]\(([^)]+)\)", guide.read_text()):
            if "://" in target or target.startswith("#"):
                continue
            path = (guide.parent / target.split("#")[0]).resolve()
            if not path.is_relative_to(root.resolve()) or not path.is_file():
                failures.append(f"broken guide link in {guide.name}")
    if len(list((root / "docs").glob("*.md"))) != 6:
        failures.append("expected six reader chapters")
    return failures, len(selected)


def main():
    try:
        failures, count = verify(ROOT)
    except (OSError, ValueError, KeyError, UnicodeError) as exc:
        print(json.dumps({"status": "FAIL", "reason": type(exc).__name__, "writes": 0}))
        return 1
    print(json.dumps({"status": "FAIL" if failures else "PASS", "selected_files": count,
                      "findings": failures, "writes": 0, "applications_launched": 0,
                      "limits": ["hash/path/link checks only", "no live apply, grammar, rendering, hardware or session acceptance"]}, indent=2))
    return bool(failures)


if __name__ == "__main__":
    sys.exit(main())
