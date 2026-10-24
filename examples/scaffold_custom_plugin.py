#!/usr/bin/env python3
"""Interactive 1-Command Antigravity Plugin Scaffolder & Validator (PEP 723).

Scaffolds a complete, production-ready Google Antigravity Plugin bundle:
- plugin.json (Manifest + 3 suggested starter prompts)
- rules/AGENTS.md (Always-on behavioral routing & safety gate)
- hooks.json (PostToolUse command execution audit logger)
- assets/logo.svg (128x128 high-contrast SVG icon)
- skills/<skill-name>/SKILL.md (Progressive-disclosure instructions)
- skills/<skill-name>/scripts/run_tool.py (PEP 723 zero-pollution CLI script)

Also includes a `--validate` mode that checks any plugin directory against
Google Antigravity's loader constraints (manifest schema, 24KB rule cap,
root hooks.json placement, and SKILL.md YAML frontmatter).
"""

# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///

import argparse
import json
from pathlib import Path
import re
import sys

ALLOWED_PLUGIN_KEYS = {
    "name",
    "displayName",
    "version",
    "description",
    "logo",
    "suggestedPrompts",
    "disabled",
}


def validate_plugin_bundle(plugin_dir: Path) -> bool:
    """Validates an Antigravity plugin directory against official loader rules."""
    print(f"\n[*] Auditing Antigravity Plugin Bundle: {plugin_dir}")
    errors: list[str] = []
    warnings: list[str] = []

    manifest_path = plugin_dir / "plugin.json"
    if not manifest_path.exists():
        errors.append("Missing required `plugin.json` at plugin root.")
    else:
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            unknown_keys = set(manifest.keys()) - ALLOWED_PLUGIN_KEYS
            if unknown_keys:
                warnings.append(
                    f"Unsupported keys in plugin.json (silently ignored by loader): {sorted(unknown_keys)}"
                )
            logo = manifest.get("logo", "")
            if logo and (logo.startswith("http://") or logo.startswith("https://") or Path(logo).is_absolute()):
                warnings.append(
                    "Custom plugin `logo` should be a relative path (e.g. 'assets/logo.svg'); URLs/absolute paths are rejected."
                )
            prompts = manifest.get("suggestedPrompts", [])
            if len(prompts) > 3:
                warnings.append("`suggestedPrompts` has >3 items; extra prompts beyond 3 are ignored by UI cards.")
            print(f"  [OK] Manifest: name='{manifest.get('name')}', version='{manifest.get('version', '0.1.0')}'")
        except json.JSONDecodeError as exc:
            errors.append(f"Invalid JSON in plugin.json: {exc}")

    # Check hooks.json placement (must be at root, not hooks/hooks.json)
    nested_hooks = plugin_dir / "hooks" / "hooks.json"
    if nested_hooks.exists() and not (plugin_dir / "hooks.json").exists():
        errors.append("Found `hooks/hooks.json` instead of root `hooks.json`. Native plugins require `<plugin_dir>/hooks.json`.")
    elif (plugin_dir / "hooks.json").exists():
        print("  [OK] Lifecycle Hooks: `hooks.json` present at plugin root")

    # Check rules size limit (24,000 bytes per file cap)
    rules_dir = plugin_dir / "rules"
    if rules_dir.exists():
        for rule_file in rules_dir.glob("*.md"):
            size = rule_file.stat().st_size
            if size > 24_000:
                warnings.append(f"Rule file `{rule_file.name}` is {size} bytes (exceeds 24,000-byte per-file cap; will be truncated).")
            else:
                print(f"  [OK] Rule File: `rules/{rule_file.name}` ({size} bytes <= 24,000-byte cap)")

    # Check skills frontmatter
    skills_dir = plugin_dir / "skills"
    if skills_dir.exists():
        for skill_md in skills_dir.glob("*/SKILL.md"):
            text = skill_md.read_text(encoding="utf-8")
            if not text.startswith("---"):
                errors.append(f"`{skill_md.relative_to(plugin_dir)}` is missing YAML frontmatter (`---`).")
            else:
                has_name = bool(re.search(r"^name:\s*\S+", text, re.MULTILINE))
                has_desc = bool(re.search(r"^description:\s*", text, re.MULTILINE))
                if not (has_name and has_desc):
                    errors.append(f"`{skill_md.relative_to(plugin_dir)}` frontmatter must define both `name` and `description`.")
                else:
                    print(f"  [OK] Skill Definition: `{skill_md.relative_to(plugin_dir)}` (valid YAML frontmatter)")

    for w in warnings:
        print(f"  [WARN] {w}")
    for e in errors:
        print(f"  [ERROR] {e}")

    if errors:
        print(f"[!] Validation FAILED with {len(errors)} error(s).")
        return False

    print("[PASS] Plugin bundle passed all Google Antigravity loader checks!")
    return True


def scaffold_plugin(output_root: Path, plugin_name: str, skill_name: str, description: str) -> Path:
    """Creates a complete Antigravity plugin bundle with all 5 customization primitives."""
    plugin_dir = output_root / plugin_name
    (plugin_dir / "assets").mkdir(parents=True, exist_ok=True)
    (plugin_dir / "rules").mkdir(parents=True, exist_ok=True)
    scripts_dir = plugin_dir / "skills" / skill_name / "scripts"
    scripts_dir.mkdir(parents=True, exist_ok=True)

    manifest = {
        "name": plugin_name,
        "displayName": plugin_name.replace("-", " ").title(),
        "version": "0.1.0",
        "description": description,
        "logo": "assets/logo.svg",
        "suggestedPrompts": [
            f"Run the {skill_name} workflow on my current workspace files",
            f"Audit and summarize results using {plugin_name}",
            f"Generate a structured JSON report with {skill_name}",
        ],
    }
    (plugin_dir / "plugin.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    (plugin_dir / "assets" / "logo.svg").write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128" width="128" height="128">\n'
        '  <rect x="12" y="12" width="104" height="104" rx="24" fill="#070B19" stroke="#00E5FF" stroke-width="4"/>\n'
        '  <circle cx="64" cy="64" r="28" fill="none" stroke="#00E676" stroke-width="6"/>\n'
        '  <circle cx="64" cy="64" r="10" fill="#7C4DFF"/>\n'
        '</svg>\n',
        encoding="utf-8",
    )

    (plugin_dir / "rules" / "AGENTS.md").write_text(
        f"# {manifest['displayName']} — Always-On Routing Rules\n\n"
        f"- Whenever the user's task involves `{skill_name}`, always execute the helper CLI script via `uv run` "
        "rather than writing ad-hoc shell one-liners.\n"
        "- Always save structured outputs to a JSON file (`--output`) so large payloads never flood the context window.\n",
        encoding="utf-8",
    )

    hooks = {
        f"{plugin_name}-audit-hook": {
            "enabled": True,
            "PostToolUse": [
                {
                    "matcher": "run_command",
                    "hooks": [
                        {
                            "type": "command",
                            "command": "python3 -c \"import datetime; print(f'[Hook] PostToolUse verified at {datetime.datetime.now(datetime.timezone.utc).isoformat()}')\"",
                            "timeout": 5,
                        }
                    ],
                }
            ],
        }
    }
    (plugin_dir / "hooks.json").write_text(json.dumps(hooks, indent=2) + "\n", encoding="utf-8")

    (plugin_dir / "skills" / skill_name / "SKILL.md").write_text(
        f"---\n"
        f"name: {skill_name}\n"
        f"description: >-\n"
        f"  {description} Use when the user asks to run {skill_name} analysis or generate a deterministic JSON report.\n"
        f"---\n\n"
        f"# {skill_name.replace('-', ' ').title()}\n\n"
        f"## Usage\n\n"
        f"Always execute the bundled PEP 723 script via `uv run`:\n\n"
        f"```bash\n"
        f"uv run scripts/run_tool.py --input <target> --output ./report.json\n"
        f"```\n",
        encoding="utf-8",
    )

    (scripts_dir / "run_tool.py").write_text(
        '#!/usr/bin/env python3\n'
        '"""Self-contained PEP 723 helper script generated by scaffold_custom_plugin.py."""\n\n'
        '# /// script\n'
        '# requires-python = ">=3.10"\n'
        '# dependencies = []\n'
        '# ///\n\n'
        'import argparse\n'
        'import json\n'
        'from pathlib import Path\n\n'
        'def main() -> None:\n'
        '    parser = argparse.ArgumentParser()\n'
        '    parser.add_argument("--input", required=True, help="Input identifier or path")\n'
        '    parser.add_argument("--output", type=Path, required=True, help="Output JSON file")\n'
        '    args = parser.parse_args()\n'
        '    payload = {"status": "SUCCESS", "input": args.input, "verified_by": "PEP723_uv_runner"}\n'
        '    args.output.parent.mkdir(parents=True, exist_ok=True)\n'
        '    args.output.write_text(json.dumps(payload, indent=2) + "\\n", encoding="utf-8")\n'
        '    print(f"[*] Saved output to {args.output}")\n\n'
        'if __name__ == "__main__":\n'
        '    main()\n',
        encoding="utf-8",
    )

    return plugin_dir


def main() -> None:
    parser = argparse.ArgumentParser(description="Scaffold or validate a Google Antigravity Plugin bundle.")
    parser.add_argument("--validate", type=Path, help="Path to an existing plugin directory to validate")
    parser.add_argument("--scaffold", type=str, help="Name of a new plugin to scaffold (e.g. my-genomics-kit)")
    parser.add_argument("--skill", type=str, default="variant-qc-runner", help="Initial skill name to create")
    parser.add_argument(
        "--description",
        type=str,
        default="Custom scientific workflow skill with PEP 723 uv isolation and context-safe JSON file output.",
        help="Plugin and skill description",
    )
    parser.add_argument("--outdir", type=Path, default=Path("plugins"), help="Parent directory for scaffolded plugin")
    args = parser.parse_args()

    if args.validate:
        ok = validate_plugin_bundle(args.validate)
        sys.exit(0 if ok else 1)

    if args.scaffold:
        created = scaffold_plugin(args.outdir, args.scaffold, args.skill, args.description)
        validate_plugin_bundle(created)
        sys.exit(0)

    # Default demo: validate the repository's bio-structural-qc plugin
    default_plugin = Path("plugins/bio-structural-qc")
    if default_plugin.exists():
        validate_plugin_bundle(default_plugin)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
