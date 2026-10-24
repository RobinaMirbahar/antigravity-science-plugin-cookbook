#!/usr/bin/env python3
"""PostToolUse reproducibility hook: logs redacted commands, script SHA-256 versions, and input file hashes."""

# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///

from __future__ import annotations

import datetime
import hashlib
import json
import pathlib
import re
import shlex
import subprocess
import sys

SECRET_PATTERNS = [
    # Mask ENV_VAR=value where name contains KEY, TOKEN, SECRET, PASS, CRED, AUTH
    (
        re.compile(
            r"\b([A-Za-z0-9_]*(?:KEY|TOKEN|SECRET|PASS|PASSWORD|CRED|AUTH)[A-Za-z0-9_]*)\s*=\s*('[^']*'|\"[^\"]*\"|\S+)",
            re.IGNORECASE,
        ),
        r"\1=[REDACTED]",
    ),
    # Mask Bearer / Basic tokens
    (
        re.compile(r"(Bearer|Basic)\s+[A-Za-z0-9._\-+/=]+", re.IGNORECASE),
        r"\1 [REDACTED]",
    ),
    # Mask CLI flags like --api-key, --token, -H "x-goog-api-key: ..."
    (
        re.compile(
            r"(--(?:api[-_]?key|token|secret|password)|x-goog-api-key:|api-key:)\s*([=:]?\s*)('[^']*'|\"[^\"]*\"|\S+)",
            re.IGNORECASE,
        ),
        r"\1\2[REDACTED]",
    ),
]

TRACKED_EXTENSIONS = {
    ".py",
    ".sh",
    ".pdb",
    ".cif",
    ".mmcif",
    ".json",
    ".fasta",
    ".fa",
    ".aln",
    ".sdf",
    ".vcf",
    ".gtf",
    ".tsv",
    ".csv",
}


def redact_secrets(command_line: str) -> str:
    """Strips API keys, tokens, and authorization headers from a shell command string."""
    redacted = command_line
    for pattern, replacement in SECRET_PATTERNS:
        redacted = pattern.sub(replacement, redacted)
    return redacted


def sha256_file(path: pathlib.Path) -> str:
    """Computes the first 16 hex chars of a file's SHA-256 digest."""
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return f"sha256:{h.hexdigest()[:16]}"


def get_git_revision(cwd: pathlib.Path) -> str:
    """Returns short git commit hash (+dirty if modified) or 'unversioned'."""
    try:
        commit = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=str(cwd),
            stderr=subprocess.DEVNULL,
            text=True,
            timeout=2,
        ).strip()
        dirty = subprocess.check_output(
            ["git", "status", "--porcelain"],
            cwd=str(cwd),
            stderr=subprocess.DEVNULL,
            text=True,
            timeout=2,
        ).strip()
        return f"{commit}{'-dirty' if dirty else ''}"
    except Exception:
        return "unversioned"


def extract_script_and_file_hashes(
    command_line: str, base_dir: pathlib.Path
) -> tuple[dict[str, str], dict[str, str]]:
    """Identifies executed scripts and existing input/output data files and hashes them."""
    try:
        tokens = shlex.split(command_line, posix=True)
    except ValueError:
        tokens = command_line.split()

    script_hashes: dict[str, str] = {}
    file_hashes: dict[str, str] = {}

    for raw_tok in tokens:
        clean_tok = raw_tok.strip("\"'`;|&()")
        if not clean_tok or clean_tok.startswith("-"):
            continue
        if "=" in clean_tok and not clean_tok.startswith(("./", "/", "~")):
            _, clean_tok = clean_tok.split("=", 1)

        candidate = pathlib.Path(clean_tok).expanduser()
        if not candidate.is_absolute():
            candidate = (base_dir / candidate).resolve()

        if candidate.is_file() and candidate.suffix.lower() in TRACKED_EXTENSIONS:
            rel_key = clean_tok
            digest = sha256_file(candidate)
            if candidate.suffix.lower() in {".py", ".sh"}:
                script_hashes[rel_key] = digest
            else:
                file_hashes[rel_key] = digest

    return script_hashes, file_hashes


def build_audit_record(payload: dict, base_dir: pathlib.Path | None = None) -> dict:
    """Builds a structured, secret-redacted reproducibility log entry from a PostToolUse payload."""
    workspace_paths = payload.get("workspacePaths") or []
    resolved_base = (
        base_dir
        or (pathlib.Path(workspace_paths[0]) if workspace_paths else pathlib.Path.cwd())
    )

    tool_call = payload.get("toolCall") or {}
    args = tool_call.get("args") or {}
    raw_cmd = str(args.get("CommandLine") or args.get("command") or "")

    script_hashes, input_file_hashes = extract_script_and_file_hashes(
        raw_cmd, resolved_base
    )

    return {
        "timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "event": "PostToolUse",
        "tool": tool_call.get("name", "run_command"),
        "conversation_id": payload.get("conversationId", "local-session"),
        "step_idx": payload.get("stepIdx", 0),
        "git_revision": get_git_revision(resolved_base),
        "redacted_command": redact_secrets(raw_cmd),
        "script_versions": script_hashes,
        "file_hashes": input_file_hashes,
        "status": "ERROR" if payload.get("error") else "OK",
    }


def main() -> None:
    if "--self-test" in sys.argv:
        repo_root = pathlib.Path(__file__).resolve().parents[3]
        sample_payload = {
            "conversationId": "conv-repro-demo-01",
            "stepIdx": 7,
            "workspacePaths": [str(repo_root)],
            "toolCall": {
                "name": "run_command",
                "args": {
                    "CommandLine": (
                        "ALPHAGENOME_API_KEY=ag_live_987654321_secret "
                        "uv run plugins/bio-structural-qc/skills/structure-qc-audit/scripts/audit_structure.py "
                        "examples/generated_p53_demo/synthetic_p53_multidomain.pdb "
                        "examples/sample_crambin_fragment.pdb"
                    )
                },
            },
        }
        record = build_audit_record(sample_payload, base_dir=repo_root)
        print(json.dumps(record, indent=2))
        return

    raw_stdin = sys.stdin.read().strip()
    payload = json.loads(raw_stdin) if raw_stdin else {}
    record = build_audit_record(payload)

    log_path = pathlib.Path.home() / ".gemini" / "qc_command_audit.jsonl"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")

    # Antigravity PostToolUse stdout contract requires an empty JSON object
    print("{}")


if __name__ == "__main__":
    main()
