#!/usr/bin/env python3
"""Inspects installed Google Antigravity plugin bundles in ~/.gemini/config/plugins/ and ./plugins/."""

# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///

from __future__ import annotations

import argparse
import json
import pathlib


def inspect_plugin_dir(plugin_dir: pathlib.Path) -> dict | None:
    manifest_path = plugin_dir / "plugin.json"
    if not manifest_path.is_file():
        return None
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    skills_dir = plugin_dir / "skills"
    skills = sorted(p.parent.name for p in skills_dir.glob("*/SKILL.md")) if skills_dir.is_dir() else []
    rules_dir = plugin_dir / "rules"
    rules = sorted(p.name for p in rules_dir.glob("*.md")) if rules_dir.is_dir() else []
    mcp_path = plugin_dir / "mcp_config.json"
    mcp_servers = []
    if mcp_path.is_file():
        mcp_data = json.loads(mcp_path.read_text(encoding="utf-8"))
        mcp_servers = list((mcp_data.get("mcpServers") or {}).keys())
    sidecars_dir = plugin_dir / "sidecars"
    sidecars = sorted(p.parent.name for p in sidecars_dir.glob("*/sidecar.json")) if sidecars_dir.is_dir() else []
    return {
        "dir": plugin_dir.name,
        "name": manifest.get("name", plugin_dir.name),
        "version": manifest.get("version", "0.0.0"),
        "skill_count": len(skills),
        "rules": rules,
        "hooks_enabled": (plugin_dir / "hooks.json").is_file(),
        "mcp_servers": mcp_servers,
        "sidecars": sidecars,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Inspect installed Antigravity plugin bundles.")
    parser.add_argument(
        "--root",
        default=str(pathlib.Path(__file__).resolve().parents[1] / "plugins"),
        help="Plugin root directory to scan (default: ./plugins, or pass ~/.gemini/config/plugins)",
    )
    args = parser.parse_args()
    root = pathlib.Path(args.root).expanduser().resolve()
    results = []
    if root.is_dir():
        for child in sorted(root.iterdir()):
            if child.is_dir():
                info = inspect_plugin_dir(child)
                if info:
                    results.append(info)
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
