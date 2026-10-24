# Google Antigravity Science Plugin & Custom Plugin Engineering Cookbook

[![Science Plugin Banner](https://www.gstatic.com/antigravity/buildWithGoogle/science/banner.png)](https://robinamirbahar.github.io/antigravity-science-plugin-cookbook/)

* **[Launch the Interactive 3D Biomolecular & Variant WebGL Studio (`index.html`)](https://robinamirbahar.github.io/antigravity-science-plugin-cookbook/)**
* **[Read the Full Dev.to Engineering Deep-Dive Article (`DEVTO_ANTIGRAVITY_SCIENCE_PLUGIN_GUIDE.md`)](./DEVTO_ANTIGRAVITY_SCIENCE_PLUGIN_GUIDE.md)**

A hands-on engineering cookbook and starter kit for building **Google Antigravity Customizations**—including **Progressive-Disclosure Skills (`SKILL.md`)**, **Always-On Rules (`AGENTS.md`)**, **Lifecycle Hooks (`hooks.json`)**, **Zero-Leak Credential Protocols**, and **Interactive 3D MCP Sidecars (`sidecar.json`)**—modeled on the official **Google Antigravity Science Plugin (`v1.3.1`)**.

![AlphaFold pLDDT Profile & PAE Domain Matrix](./examples/generated_p53_demo/p53_plddt_pae_dashboard.svg)

---

## Repository Structure

```text
antigravity-science-plugin-cookbook/
├── index.html                                             # Interactive 3D Biomolecular & Variant WebGL Studio
├── README.md                                              # Quickstart & architecture overview
├── DEVTO_ANTIGRAVITY_SCIENCE_PLUGIN_GUIDE.md              # Full Dev.to engineering deep-dive article
├── examples/
│   ├── generate_3d_protein_pae_demo.py                    # PEP 723 3D protein (.pdb) + PAE JSON + SVG generator
│   ├── sample_crambin_fragment.pdb                        # Sample PDB structure with disordered linker + rigid core
│   ├── inspect_plugins_rpc.sh                             # Safe Connect RPC helper for GetAllPlugins / JetboxWriteState
│   └── generated_p53_demo/
│       ├── synthetic_p53_multidomain.pdb                  # Generated 56-residue 3-domain 3D coordinate file
│       ├── synthetic_p53_pae.json                         # Generated 56x56 PAE matrix
│       └── p53_plddt_pae_dashboard.svg                    # Generated dark-mode pLDDT + PAE vector dashboard
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

```bash
git clone https://github.com/RobinaMirbahar/antigravity-science-plugin-cookbook.git
cd antigravity-science-plugin-cookbook

# 1. Generate a 56-residue 3-domain 3D .pdb structure, PAE matrix JSON, and SVG dashboard
uv run examples/generate_3d_protein_pae_demo.py

# 2. Run the PEP 723 C-alpha pLDDT/B-factor QC auditor on both PDB files
uv run plugins/bio-structural-qc/skills/structure-qc-audit/scripts/audit_structure.py \
  examples/generated_p53_demo/synthetic_p53_multidomain.pdb \
  examples/sample_crambin_fragment.pdb
```

---

## License

Apache License 2.0
