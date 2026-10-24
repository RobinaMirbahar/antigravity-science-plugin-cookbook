---
name: structure-qc-audit
description: >-
  Audits 3D protein coordinate files (.pdb, .cif, .mmcif) for C-alpha chain
  completeness, mean/median pLDDT or B-factor distribution, and disordered
  regions (< 50.0). Use whenever validating downloaded PDB or AlphaFold
  structures before docking, alignment, or 3D visualization.
---

# Structure QC Audit Skill

## Execution

Run the helper script via `uv run` and pass `--output` when auditing multiple structures:

```bash
uv run scripts/audit_structure.py /path/to/structure.cif -o ./qc_report.json
```

## Interpreting Results

1. **`status == "PASS"`**: Less than 30% of C-alpha residues fall below 50.0. Safe to proceed.
2. **`status == "WARN_HIGH_DISORDER"`**: More than 30% of residues have scores `< 50.0`.
   - Use the `high_confidence_span` coordinates from the JSON output to call `highlight_region` in `science_biomolecular_structure_viewer_mcp` so the user can visually distinguish rigid domains from disordered tails.
