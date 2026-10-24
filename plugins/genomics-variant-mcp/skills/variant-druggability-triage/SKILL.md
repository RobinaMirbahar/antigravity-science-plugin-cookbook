---
name: variant-druggability-triage
description: >-
  Coordinates the genomics_variant_mcp server tools (score_variant_impact,
  evaluate_lipinski_ro5) and the clinical-variant-curator subagent to triage
  genomic variants alongside small-molecule inhibitor properties.
---

# Variant & Druggability Triage Skill

## Workflow

1. **Score the Variant via MCP**: Call `score_variant_impact` (or run `uv run plugins/genomics-variant-mcp/mcp/variant_mcp_server.py --self-test` to verify the server).
2. **Check Inhibitor Druggability**: Call `evaluate_lipinski_ro5` with Molecular Weight (`mw_daltons`), `clogp`, `h_bond_donors`, and `h_bond_acceptors`.
3. **Subagent Delegation**: For multi-gene panels, invoke the `clinical-variant-curator` subagent.
