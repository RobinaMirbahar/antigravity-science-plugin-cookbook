# Biomolecular Structure QC Gate

Whenever a workflow downloads or modifies a 3D coordinate file (`.pdb`, `.cif`, or `.mmcif`) for downstream structural analysis, homology search, or variant mapping:

1. **Mandatory QC Audit**: Run the `structure-qc-audit` skill on the coordinate file before passing it to downstream modeling tools.
2. **Disorder Warning**: If more than 30% of alpha-carbon (`CA`) atoms have a B-factor / pLDDT score below `50.0`, explicitly warn the user about disordered or low-confidence regions and highlight the high-confidence domain boundaries in the [Biomolecular Structure Viewer](sidecar://science/biomolecular_structure_viewer/ui.html).
