# Google Antigravity Science Plugin & Custom Plugin Engineering Cookbook

[![From Ancient Epigraphy to 3D Proteins: Antigravity Science Plugin!](./assets/devto_cover_banner.jpg)](https://robinamirbahar.github.io/antigravity-science-plugin-cookbook/)

* **[Launch the Interactive 3D Biomolecular & Variant WebGL Studio (`index.html`)](https://robinamirbahar.github.io/antigravity-science-plugin-cookbook/)**
* **[Read the Full Dev.to Engineering Deep-Dive Article (`DEVTO_ANTIGRAVITY_SCIENCE_PLUGIN_GUIDE.md`)](./DEVTO_ANTIGRAVITY_SCIENCE_PLUGIN_GUIDE.md)**
* **[Jump to the Hands-On Plugin Authoring Codelab & 1-Command Scaffolder](#hands-on-plugin-authoring-codelab-build-validate--deploy-in-5-minutes)**

A hands-on engineering cookbook and starter kit for building **Google Antigravity Customizations**—including **Progressive-Disclosure Skills (`SKILL.md`)**, **Always-On Rules (`AGENTS.md`)**, **Lifecycle Hooks (`hooks.json`)**, **Zero-Leak Credential Protocols**, and **Interactive 3D MCP Sidecars (`sidecar.json`)**—modeled on the official **Google Antigravity Science Plugin (`v1.3.1`)**.

---

## Visual Overview: 5 End-to-End Multi-Skill Pipelines Across the 33 Science Skills

Run `uv run examples/multi_domain_science_use_cases.py` to execute all 5 multi-skill pipelines deterministically and generate the JSON benchmark report ([`examples/generated_use_cases/science_use_cases_report.json`](./examples/generated_use_cases/science_use_cases_report.json)) and vector visual dashboards below:

![Google Antigravity Science Plugin — 5 End-to-End Multi-Skill Pipelines Scorecard](./examples/generated_use_cases/science_use_cases_scorecard.svg)

### Use Case 1: Precision Oncology & 3D Kinase Pocket Triage (`EGFR L858R` / `CHEMBL203`)
**Skills Chained:** `clinvar-database` $\rightarrow$ `gnomad-database` (`LOEUF = 0.24`) $\rightarrow$ `alphafold-database-fetch-and-analyze` (`P00533`) $\rightarrow$ `chembl-database` (`Erlotinib`, `Osimertinib`, `Gefitinib`) $\rightarrow$ `biomolecular-structure-viewer` (`highlight_region` in 3D Mol\* Sidecar).

![Use Case 1 — Precision Oncology & 3D Kinase Pocket Triage](./examples/generated_use_cases/uc1_precision_oncology_3d.svg)

---

### Use Case 2: Non-Coding GWAS Enhancer Variant Triage (`SORT1` 1p13 Locus `rs12740374`)
**Skills Chained:** `alphagenome-variant-impact-score` (`AVI = 0.94`) $\rightarrow$ `alphagenome-single-variant-analysis` $\rightarrow$ `ucsc-conservation-and-tfbs` (`phyloP100way = +4.82`) $\rightarrow$ `encode-ccres-database` (`dELS`) $\rightarrow$ `jaspar-database` (`MA0102.4 CEBPA` de novo binding site gain) $\rightarrow$ `gtex-database` (Liver eQTL `NES = +1.42`).

![Use Case 2 — Non-Coding GWAS Enhancer Variant Triage](./examples/generated_use_cases/uc2_noncoding_alphagenome.svg)

---

### Use Case 3: Dark-Proteome Enzyme Discovery in the Sequence "Twilight Zone" (`Foldseek 3D Search`)
**Skills Chained:** `ncbi-sequence-fetch` $\rightarrow$ `alphafold-database-fetch-and-analyze` $\rightarrow$ `foldseek-structural-search` (`afdb50`, `mgnify_esm30`, `pdb100`, `cath50`) $\rightarrow$ `interpro-database` $\rightarrow$ `protein-sequence-msa` (`Clustal Omega` conserving the `Ser160-Asp206-His237` catalytic triad at `21.4%` sequence identity) $\rightarrow$ `pymol` (headless OSMesa rendering).

![Use Case 3 — Dark-Proteome Enzyme Discovery with Foldseek](./examples/generated_use_cases/uc3_dark_proteome_foldseek.svg)

---

### Use Case 4: Clinical Trial Portfolio & openFDA FAERS Disproportionality Audit (`MONDO_0005090` NSCLC)
**Skills Chained:** `opentargets-database` $\rightarrow$ `clinical-trials-database` (`--count-total` + `--fields` context-saving projection cutting payload size by `98.7%`) $\rightarrow$ `openfda-database` (FAERS Reporting Odds Ratio $ROR$ forest plot with `FDA_API_KEY` zero-leak `.env` verification raising quota from `1,000` $\rightarrow$ `120,000` req/day).

![Use Case 4 — Clinical Trial Portfolio & openFDA FAERS Safety Audit](./examples/generated_use_cases/uc4_clinical_trials_openfda.svg)

---

### Use Case 5: Ancient Roman & Greek Epigraphy Restoration (`Google DeepMind Aeneas & Ithaca`)
**Skills Chained:** `predictingthepast` (`preprocess.py` $\rightarrow$ `run_inference.py` $\rightarrow$ `visualize_results.py` restoring `imp caesar divi f ???????? cos xi` $\rightarrow$ `augustus` at `96.4%` confidence, attributed to *Latium et Campania*, `23 BCE`) $\rightarrow$ `literature-search-openalex`.

![Use Case 5 — Ancient Roman & Greek Epigraphy Restoration](./examples/generated_use_cases/uc5_aeneas_latin_epigraphy.svg)

---

## Synthetic 3D Multi-Domain Protein & PAE Matrix Generator

Run `uv run examples/generate_3d_protein_pae_demo.py` to procedurally generate a 56-residue 3-domain 3D `.pdb` coordinate file (`synthetic_p53_multidomain.pdb`), a $56 \times 56$ Predicted Aligned Error (PAE) matrix (`synthetic_p53_pae.json`), and the vector QC dashboard below:

![AlphaFold pLDDT Profile & PAE Domain Matrix](./examples/generated_p53_demo/p53_plddt_pae_dashboard.svg)

---

## Hands-On Plugin Authoring Codelab: Build, Validate & Deploy in 5 Minutes

Want to create your own custom Google Antigravity plugin from scratch? Follow this interactive 4-step hands-on lab using our **1-Command Plugin Scaffolder & Loader Validator ([`examples/scaffold_custom_plugin.py`](./examples/scaffold_custom_plugin.py))**.

### Step 1: Clone & Run the Built-In Plugin Validator
First, verify the included `plugins/bio-structural-qc` reference plugin against Google Antigravity's loader rules (manifest schema, `<= 24,000`-byte rule cap, root `hooks.json` placement, and `SKILL.md` YAML frontmatter):

```bash
git clone https://github.com/RobinaMirbahar/antigravity-science-plugin-cookbook.git
cd antigravity-science-plugin-cookbook

uv run examples/scaffold_custom_plugin.py --validate plugins/bio-structural-qc
```

Expected output:

```text
[*] Auditing Antigravity Plugin Bundle: plugins/bio-structural-qc
  [OK] Manifest: name='bio-structural-qc', version='0.1.0'
  [OK] Lifecycle Hooks: `hooks.json` present at plugin root
  [OK] Rule File: `rules/AGENTS.md` (666 bytes <= 24,000-byte cap)
  [OK] Skill Definition: `skills/structure-qc-audit/SKILL.md` (valid YAML frontmatter)
[PASS] Plugin bundle passed all Google Antigravity loader checks!
```

### Step 2: Scaffold a Brand-New Custom Plugin in One Command
Use `--scaffold` to generate a new plugin bundle (including `plugin.json`, `assets/logo.svg`, `rules/AGENTS.md`, `hooks.json`, `SKILL.md`, and a PEP 723 `scripts/run_tool.py` helper):

```bash
uv run examples/scaffold_custom_plugin.py \
  --scaffold my-genomics-qc \
  --skill vcf-filter-audit \
  --description "Deterministic VCF quality filtering and AlphaGenome coordinate readiness checks."
```

### Step 3: Test Your New Skill's PEP 723 Script Locally

```bash
uv run plugins/my-genomics-qc/skills/vcf-filter-audit/scripts/run_tool.py \
  --input "chr17:7674220:C>T" \
  --output ./artifacts/vcf_qc_report.json
```

### Step 4: Install into Antigravity & Toggle Live via Connect RPC
Copy your plugin into `~/.gemini/config/plugins/` (or `.agents/plugins/` inside any project repository):

```bash
# Linux / macOS
cp -r plugins/bio-structural-qc ~/.gemini/config/plugins/bio-structural-qc

# Windows PowerShell
Copy-Item -Recurse -Force .\plugins\bio-structural-qc "$HOME\.gemini\config\plugins\bio-structural-qc"
```

After restarting Antigravity once so the new plugin directory is discovered, you can inspect or toggle it live at any time via the Language Server Connect RPC ([`examples/inspect_plugins_rpc.sh`](./examples/inspect_plugins_rpc.sh)).

---

## Repository Structure

```text
antigravity-science-plugin-cookbook/
├── index.html                                             # Interactive 3D Biomolecular & Variant WebGL Studio
├── README.md                                              # Visual showcase, 5 use cases & hands-on plugin codelab
├── DEVTO_ANTIGRAVITY_SCIENCE_PLUGIN_GUIDE.md              # Full Dev.to engineering deep-dive article
├── assets/
│   └── devto_cover_banner.jpg                             # Custom 16:9 editorial comic cover illustration
├── examples/
│   ├── generate_3d_protein_pae_demo.py                    # PEP 723 3D protein (.pdb) + PAE JSON + SVG generator
│   ├── multi_domain_science_use_cases.py                  # PEP 723 5-use-case runner + 6 SVG visual cards generator
│   ├── scaffold_custom_plugin.py                          # 1-command Antigravity plugin scaffolder & validator
│   ├── sample_crambin_fragment.pdb                        # Sample PDB structure with disordered linker + rigid core
│   ├── inspect_plugins_rpc.sh                             # Safe Connect RPC helper for GetAllPlugins / JetboxWriteState
│   ├── generated_p53_demo/
│   │   ├── synthetic_p53_multidomain.pdb                  # Generated 56-residue 3-domain 3D coordinate file
│   │   ├── synthetic_p53_pae.json                         # Generated 56x56 PAE matrix
│   │   └── p53_plddt_pae_dashboard.svg                    # Generated dark-mode pLDDT + PAE vector dashboard
│   └── generated_use_cases/
│       ├── science_use_cases_report.json                  # Structured output for all 5 multi-skill pipelines
│       ├── science_use_cases_scorecard.svg                # Executive benchmark scorecard SVG
│       ├── uc1_precision_oncology_3d.svg                  # UC1 Hill-Langmuir IC50 curves & 3D Mol* state card
│       ├── uc2_noncoding_alphagenome.svg                  # UC2 AlphaGenome 18-modality & JASPAR CEBPA motif card
│       ├── uc3_dark_proteome_foldseek.svg                 # UC3 Foldseek twilight-zone hits & Clustal MSA triad card
│       ├── uc4_clinical_trials_openfda.svg                # UC4 ClinicalTrials.gov projection & FAERS ROR forest plot
│       └── uc5_aeneas_latin_epigraphy.svg                 # UC5 DeepMind Aeneas restoration & 23 BCE dating curve
└── plugins/
    └── bio-structural-qc/                                 # Production example plugin bundle
        ├── plugin.json                                    # Manifest & suggested starter prompts
        ├── hooks.json                                     # PostToolUse command audit hook
        ├── assets/
        │   └── logo.svg                                   # High-contrast 128x128 SVG icon
        ├── rules/
        │   └── AGENTS.md                                  # Always-on QC gate & Mol* 3D sidecar routing rule
        └── skills/
            └── structure-qc-audit/
                ├── SKILL.md                               # Progressive-disclosure skill definition
                └── scripts/
                    └── audit_structure.py                 # PEP 723 zero-dependency C-alpha pLDDT/B-factor auditor
```

---

## License

Apache License 2.0
