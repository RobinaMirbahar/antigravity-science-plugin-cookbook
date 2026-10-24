---
name: epigraphy-gap-validator
description: >-
  Validates and normalizes damaged Latin and Ancient Greek inscriptions against
  Google DeepMind Aeneas and Ithaca markup constraints (>=25 chars, no adjacent
  ##, ?#, or #? tokens) and generates a structured readiness report.
---

# Epigraphy Gap Validator & Normalizer Skill

## Usage

Run the PEP 723 validator script via `uv run`:

```bash
uv run plugins/epigraphy-citation-kit/skills/epigraphy-gap-validator/scripts/validate_epigraphy.py \
  --text "imp caesar divi f ???????? cos xi trib potest" \
  --language latin
```
