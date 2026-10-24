# Google Antigravity Science Plugin & Custom Plugin Engineering Cookbook

[![Science Plugin Banner](https://www.gstatic.com/antigravity/buildWithGoogle/science/banner.png)](https://antigravity.google/use-cases/science)

A hands-on engineering cookbook and starter kit for building **Google Antigravity Customizations**—including **Progressive-Disclosure Skills (`SKILL.md`)**, **Always-On Rules (`AGENTS.md`)**, **Lifecycle Hooks (`hooks.json`)**, **Zero-Leak Credential Protocols**, and **Interactive 3D MCP Sidecars (`sidecar.json`)**—modeled on the official **Google Antigravity Science Plugin (`v1.3.1`)**.

---

## Repository Structure

```text
antigravity-science-plugin-cookbook/
├── README.md                                              # Quickstart & architecture overview
├── DEVTO_ANTIGRAVITY_SCIENCE_PLUGIN_GUIDE.md              # Full Dev.to engineering deep-dive article
├── examples/
│   ├── sample_crambin_fragment.pdb                        # Sample PDB structure with disordered linker + rigid core
│   └── inspect_plugins_rpc.sh                             # Safe Connect RPC helper for GetAllPlugins / JetboxWriteState
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

## Quick Start

### 1. Run the PEP 723 Structure QC Auditor (`audit_structure.py`)

Test the standalone C-alpha B-factor / pLDDT auditor on the included sample PDB structure (`examples/sample_crambin_fragment.pdb`):

```bash
git clone https://github.com/RobinaMirbahar/antigravity-science-plugin-cookbook.git
cd antigravity-science-plugin-cookbook

# Run directly with Python 3.10+ or uv run (PEP 723 inline script metadata)
python plugins/bio-structural-qc/skills/structure-qc-audit/scripts/audit_structure.py \
  examples/sample_crambin_fragment.pdb
```

Expected JSON output:

```json
[
  {
    "file": "sample_crambin_fragment.pdb",
    "status": "PASS",
    "total_ca_residues": 16,
    "overall_mean_score": 80.36,
    "overall_pct_low_lt_50": 25.0,
    "chains": {
      "A": {
        "residue_count": 16,
        "mean_score": 80.36,
        "median_score": 91.9,
        "pct_high_confidence_ge_70": 75.0,
        "pct_low_confidence_lt_50": 25.0,
        "high_confidence_span": [
          5,
          16
        ]
      }
    }
  }
]
```

### 2. Install the `bio-structural-qc` Plugin in Antigravity

Copy the `plugins/bio-structural-qc` bundle into your global Antigravity plugins directory (or `.agents/plugins/` inside any project workspace):

```bash
# Linux / macOS
cp -r plugins/bio-structural-qc ~/.gemini/config/plugins/bio-structural-qc

# Windows PowerShell
Copy-Item -Recurse -Force .\plugins\bio-structural-qc "$HOME\.gemini\config\plugins\bio-structural-qc"
```

Restart Antigravity so the new plugin directory is discovered.

---

## License

Apache License 2.0
