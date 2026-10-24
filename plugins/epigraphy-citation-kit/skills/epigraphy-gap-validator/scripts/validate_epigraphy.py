#!/usr/bin/env python3
"""Validates damaged Latin & Ancient Greek inscriptions for Aeneas / Ithaca inference."""

# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///

import argparse
import json
import re


def validate_inscription(text: str, language: str = "latin") -> dict:
    # Convert Leiden unknown-length gap [---] or [- - -] into '#' before stripping editorial brackets
    normalized = re.sub(r"\[\s*-[-\s]*\]", "#", text.lower().strip())
    # Convert Leiden known-length dot gaps [. . .] or [...] into '?' per dot
    normalized = re.sub(
        r"\[\s*(\.+)\s*\]",
        lambda m: "?" * len(m.group(1).replace(" ", "")),
        normalized,
    )
    cleaned = re.sub(r"[\[\]\(\)]", "", normalized)
    cleaned = re.sub(r"\d+", "0", cleaned)

    issues = []
    if "##" in cleaned:
        issues.append("Contains forbidden consecutive unknown-length gaps ('##').")
    if "?#" in cleaned or "#?" in cleaned:
        issues.append("Contains forbidden adjacent '?#' or '#?' gap markers.")

    padded = cleaned
    if len(cleaned) < 25:
        pad_len = 25 - len(cleaned)
        padded = cleaned + ("-" * pad_len)
        issues.append(f"Input length ({len(cleaned)}) < 25 chars; auto-padded to 25 chars with '-'.")

    q_count = cleaned.count("?")
    h_count = cleaned.count("#")

    return {
        "language": language,
        "model_target": "DeepMind Aeneas (Latin)" if language == "latin" else "DeepMind Ithaca (Ancient Greek)",
        "raw_input": text,
        "normalized_input": padded,
        "char_length": len(padded),
        "known_length_gaps_q": q_count,
        "unknown_length_gaps_hash": h_count,
        "ready_for_inference": not any("forbidden" in i for i in issues),
        "notes": issues,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate epigraphic gap markup for Aeneas/Ithaca.")
    parser.add_argument("--text", default="imp caesar divi f ???????? cos xi trib potest")
    parser.add_argument("--language", choices=["latin", "greek"], default="latin")
    args = parser.parse_args()

    print(json.dumps(validate_inscription(args.text, args.language), indent=2))


if __name__ == "__main__":
    main()
