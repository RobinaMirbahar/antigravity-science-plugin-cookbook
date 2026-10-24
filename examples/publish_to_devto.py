#!/usr/bin/env python3
"""Publishes DEVTO_ANTIGRAVITY_SCIENCE_PLUGIN_GUIDE.md to DEV.to via the Forem API.

Reads `DEV_TO_API_KEY` safely from `~/.env` without printing the secret.
"""

# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///

import argparse
import json
import os
from pathlib import Path
import sys
import urllib.error
import urllib.request


def load_api_key() -> str:
    for env_path in [Path.home() / ".env", Path(".env")]:
        if env_path.exists():
            for line in env_path.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line.startswith("DEV_TO_API_KEY="):
                    val = line.split("=", 1)[1].strip().strip('"').strip("'")
                    if val:
                        return val
    return os.environ.get("DEV_TO_API_KEY", "")


def main() -> None:
    parser = argparse.ArgumentParser(description="Publish Markdown article to DEV.to")
    parser.add_argument(
        "--file",
        type=Path,
        default=Path("DEVTO_ANTIGRAVITY_SCIENCE_PLUGIN_GUIDE.md"),
        help="Path to the Markdown article with YAML frontmatter",
    )
    parser.add_argument(
        "--update-id",
        type=int,
        default=None,
        help="Optional existing DEV.to article ID to update (PUT) instead of creating (POST)",
    )
    args = parser.parse_args()

    api_key = load_api_key()
    if not api_key:
        print("[ERROR] DEV_TO_API_KEY not found in ~/.env", file=sys.stderr)
        sys.exit(1)

    body_markdown = args.file.read_text(encoding="utf-8")
    payload = {
        "article": {
            "body_markdown": body_markdown,
        }
    }

    url = (
        f"https://dev.to/api/articles/{args.update_id}"
        if args.update_id
        else "https://dev.to/api/articles"
    )
    method = "PUT" if args.update_id else "POST"

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Accept": "application/vnd.forem.api-v1+json",
            "api-key": api_key,
            "User-Agent": "AntigravitySciencePluginCookbook/1.0",
        },
        method=method,
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            print(
                json.dumps(
                    {
                        "status": "PUBLISHED" if result.get("published_at") else "DRAFT_SAVED",
                        "id": result.get("id"),
                        "title": result.get("title"),
                        "url": result.get("url"),
                        "slug": result.get("slug"),
                        "published_at": result.get("published_at"),
                        "tag_list": result.get("tag_list"),
                    },
                    indent=2,
                )
            )
    except urllib.error.HTTPError as exc:
        err_body = exc.read().decode("utf-8", errors="replace")
        print(f"[HTTP {exc.code}] {err_body}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
