---
title: "From Ancient Epigraphy to 3D Proteins: Building Plugins, Skills & MCP Sidecars in Google Antigravity"
published: true
description: "Exploring the open-source (Apache 2.0 / CC-BY 4.0) architecture of Google Antigravity's Science Plugin (v1.3.1) and Google Cloud MCP endpoints (Vertex AI, BigQuery, Cloud Run) with a 3D WebGL Biomolecular Studio and 3 custom plugins."
tags: ai, gemini, bioinformatics, opensource
cover_image: https://raw.githubusercontent.com/RobinaMirbahar/antigravity-science-plugin-cookbook/main/assets/devto_cover_banner.jpg
---

What happens when you ask an AI coding agent to **score a non-coding human genomic variant with AlphaGenome**, **map a missense mutation onto an AlphaFold 3D protein structure**, **screen ChEMBL for nanomolar small-molecule inhibitors**, or **restore a damaged 2,000-year-old Roman inscription using Google DeepMind's Aeneas model**?

If you try to stuff 40 scientific APIs, rate limiters, clinical safety guardrails, and 3D WebGL visualizers into a single mega-prompt, the agent collapses under context bloat and hallucinated parameters.

**Google Antigravity** solves this at the runtime level with its **Plugin & Customization Architecture** - combining **Progressive-Disclosure Skills (`SKILL.md`)**, **Always-On Rules (`AGENTS.md`)**, **Lifecycle Hooks (`hooks.json`)**, **Zero-Leak Credential Protocols**, and **Dual-Process 3D MCP Sidecars (`mcp_config.json` + `sidecar.json`)**.

Instead of just reading the docs, I explored the open-source (Apache 2.0 / CC-BY 4.0) architecture of the newly released **Google Antigravity Science Plugin (`v1.3.1`)** and built the open-source **[Antigravity Science Plugin Cookbook & Interactive 3D Studio](https://github.com/RobinaMirbahar/antigravity-science-plugin-cookbook)** - complete with a **live browser-based 3D Biomolecular & Variant WebGL Sandbox**, a **zero-dependency PEP 723 3D protein + PAE generator**, and a production **`bio-structural-qc` custom plugin**.

---

## Try the Live 3D Biomolecular & MCP Sidecar Studio in Your Browser

* **[Launch the Interactive 3D Biomolecular & Variant WebGL Studio (`index.html`)](https://robinamirbahar.github.io/antigravity-science-plugin-cookbook/)**
  * Explore 3D C-alpha backbones & non-covalent contact networks for **TP53 (`AF-P04637`)**, **Crambin (`1CRN`)**, and **EGFR Kinase + Gefitinib (`CHEMBL203`)**.
  * Click any 3D residue sphere via raycasting to trigger live **`annotate_region`** MCP tool calls, inspect **AlphaFold pLDDT** & **AlphaGenome Variant Impact (AVI)** scores, upload your own `.pdb`/`.cif` files, or run the interactive **Aeneas Latin Epigraphy** restoration demo!
* **[Full Source Code & `bio-structural-qc` Plugin on GitHub (`RobinaMirbahar/antigravity-science-plugin-cookbook`)](https://github.com/RobinaMirbahar/antigravity-science-plugin-cookbook)**

---

## 1. The Antigravity Customization Architecture & Context Economics

Why can the Science plugin bundle **40 complex scientific skills** and a **9-tool 3D WebGL MCP server** without slowing down everyday coding turns? Because Antigravity strictly separates **always-on behavioral guardrails** from **on-demand procedural execution**:

```mermaid
flowchart TB
    subgraph Discovery["1. Hierarchical Discovery & Precedence (Highest -> Lowest)"]
        P1["1. Workspace (.agents/ walking up to repo root)"]
        P2["2. Workspace Declared (skills.json / plugins.json)"]
        P3["3. Global Config (~/.gemini/config/)"]
        P4["4. Built-in Bundles (/builtin/plugins/)"]
        P5["5. Global Declared JSON"]
        P1 --> P2 --> P3 --> P4 --> P5
    end

    subgraph Bundle["2. Plugin Bundle (~/.gemini/config/plugins/science/)"]
        Manifest["plugin.json (Manifest & Metadata)"]
        Rules["rules/AGENTS.md (Always-On Guardrails)"]
        Skills["skills/*/SKILL.md (40 On-Demand Skills)"]
        Hooks["hooks.json (PreToolUse / PostToolUse)"]
        MCP["mcp_config.json (Stdio / Streamable HTTP)"]
        Sidecar["sidecars/*/sidecar.json (Background Sidecar Process)"]
    end

    subgraph Runtime["3. Agent Context & Execution Loop"]
        SysPrompt["System Prompt\n• Rules inlined (24KB/file, 20K token cap)\n• Skill names + descriptions ONLY\n• Eager MCP tool schemas"]
        Activate["Progressive Disclosure\nAgent calls read_file(SKILL.md)\nONLY when task matches description"]
        Exec["Deterministic Execution\n• uv run scripts/*.py (PEP 723)\n• Call MCP tools & Sidecar workers\n• Render 3D PyMOL / WebGL outputs"]
        SysPrompt --> Activate --> Exec
    end

    Discovery --> Bundle --> Runtime
```

### The 5 Customization Primitives & Their Token Budgets

| Primitive | Config File / Path | Loading Behavior | Token Budget & Engineering Role |
| :--- | :--- | :--- | :--- |
| **Rules** | `GEMINI.md`, `AGENTS.md`, `rules/AGENTS.md` | **Always-On** (within directory or active plugin scope) | **24,000 bytes/file cap**; shares a dedicated **20,000-token aggregate rules budget** . Over-budget rules gracefully demote to file path pointers. |
| **Skills** | `skills/<name>/SKILL.md` | **Progressive Disclosure** (On-Demand) | Only the YAML `name` and `description` (~40-80 tokens) are injected into the system prompt. The full `SKILL.md` (up to 32 KB!) and `references/` are read *only* when activated. |
| **Plugins** | `plugins/<dir>/plugin.json` | **Atomic Bundle** | Namespaces and toggles related `skills/`, `rules/`, `hooks.json`, `mcp_config.json`, and `sidecars/` as a single unit. |
| **Hooks** | `hooks.json` (at plugin or `.agents/` root) | **Lifecycle Event Triggers** | Intercepts `SessionStart`, `PreInvocation`, `PreToolUse`, `PostToolUse`, `PostInvocation`, and `Stop` to run shell validators, audit loggers, or linters. |
| **MCP & Sidecars** | `mcp_config.json` + `sidecars/<name>/sidecar.json` | **Tool + UI Integration** | Connects local (`stdio`) or remote (`Streamable HTTP`) tool servers (`mcp_config.json`) and manages persistent background sidecar processes (`sidecar.json`). |

---

## 2. Inside the Open-Source Architecture of the Antigravity `science` Plugin (`v1.3.1`)

When installed from the Antigravity Marketplace (`antigravity-plugins-official/plugin/science`), the bundle unpacks into `~/.gemini/config/plugins/science/`. Look at how cleanly the 40 open-source skills and manifest files are organized:

```text
google-deepmind/science-skills/ (installed at ~/.gemini/config/plugins/science/)
├── plugin.json                                  # Bundle manifest (name, description, $schema)
├── LICENSE                                      # Apache 2.0 & CC-BY 4.0 Open-Source Licenses
├── README.md                                    # User-facing setup & documentation
├── SKILL_LICENSES.md                            # Third-party database attribution & terms
└── skills/                                      # 40 Progressive-Disclosure Scientific Skills
    ├── alphafold_database_fetch_and_analyze/    # pLDDT & sliding-window PAE domain heuristics
    ├── alphagenome_atlas_website_links/         # Deep-links to AlphaGenome Atlas
    ├── alphagenome_single_variant_analysis/     # RNA-seq, DNASE, ChIP & splicing effects
    ├── alphagenome_variant_impact_score/        # AVI scoring, VCF annotation, GENCODE v46 GTF
    ├── chembl_database/                         # Bioactivity (IC50/Ki), targets, drug mechanisms
    ├── clinical_trials_database/                # ClinicalTrials.gov APIv2 queries
    ├── clinvar_database/                        # Pathogenicity & clinical review status
    ├── credentials/                             # Zero-leak .env verification protocol
    ├── dbsnp_database/                          # rsID <-> GRCh38 VCF/HGVS resolution
    ├── embl_ebi_ols/                            # 250+ biomedical ontologies (GO, HP, DOID)
    ├── encode_ccres_database/                   # ENCODE SCREEN GraphQL & cis-regulatory elements
    ├── ensembl_database/                        # Gene/transcript lookup, sequences & VEP
    ├── foldseek_structural_search/              # 3D structure similarity search (.cif/.pdb)
    ├── gnomad_database/                         # Allele frequencies & gene constraint (pLI/LOEUF)
    ├── gtex_database/                           # Tissue-specific RNA expression & eQTLs
    ├── human_protein_atlas_database/            # Spatial & tissue protein expression
    ├── interpro_database/                       # Protein domains, families & InterPro-N
    ├── jaspar_database/                         # TF binding profiles (PFMs/PWMs)
    ├── literature_search_arxiv/                 # arXiv preprints & full-text extraction
    ├── literature_search_biorxiv/               # bioRxiv / medRxiv narrow-window search
    ├── literature_search_europepmc/             # Europe PMC XML/PDF & citation graphs
    ├── literature_search_openalex/              # Bibliometrics, citation counts & OA PDFs
    ├── ncbi_sequence_fetch/                     # NCBI E-utilities nucleotide/protein fetch
    ├── openfda_database/                        # 28 FDA endpoints (adverse events, 510k, NDC)
    ├── opentargets_database/                    # Target-disease associations & tractability
    ├── pdb_database/                            # Experimental 3D structures from RCSB PDB
    ├── predictingthepast/                       # Aeneas (Latin) & Ithaca (Ancient Greek) epigraphy
    ├── protein_sequence_msa/                    # EBI Clustal Omega multiple sequence alignment
    ├── protein_sequence_similarity_search/      # MMseqs2 (fast) & BLAST homology search
    ├── pubchem_database/                        # SMILES/CID chemical properties & substructures
    ├── pubmed_database/                         # NCBI PubMed + PMC BioC full-text linking
    ├── pymol/                                   # Headless PyMOL rendering & structural superposition
    ├── quickgo_database/                        # Gene Ontology & ECO evidence mapping
    ├── reactome_database/                       # Pathway enrichment & reaction participants
    ├── string_database/                         # Protein-protein interaction (PPI) networks
    ├── ucsc_conservation_and_tfbs/              # phyloP, phastCons & ENCODE/JASPAR/ReMap TFBS
    ├── unibind_database/                        # Experimentally validated direct TF-DNA binding
    ├── uniprot_database/                        # UniProtKB/UniParc/UniRef metadata & sequences
    ├── uv/                                      # Prerequisite uv environment bootstrapper
    └── workflow_skill_creator/                  # Interactive distiller: turns chat workflows into skills
```

---

## 3. Five Production Engineering Patterns Inside the Science Plugin

While inspecting the source files across all 40 skills, five engineering patterns stood out that every Google Cloud and agentic AI builder can adopt.

### Pattern 1: Always-On Behavioral Routing via `rules/AGENTS.md`

As documented in the public **[Antigravity Rules Guide (`antigravity.google/docs/rules`)](https://antigravity.google/docs/rules)**, rules define persistent coding standards and architectural constraints (`always_on`, `model_decision`, `glob`, or `manual`) within a **24,000-byte per-file limit** and a **20,000-token aggregate rules budget**.

In our custom `bio-structural-qc` plugin (`plugins/bio-structural-qc/rules/AGENTS.md`), we use a compact `AGENTS.md` rule so the agent automatically audits 3D coordinate files (`.pdb`, `.cif`, `.mmcif`) and warns about low-confidence disordered regions before running downstream structural searches or headless PyMOL renders:

```markdown
# Biomolecular Structure QC Gate

Whenever a workflow downloads or modifies a 3D coordinate file (`.pdb`, `.cif`, or `.mmcif`) for downstream structural analysis, homology search, or variant mapping:

1. **Mandatory QC Audit**: Run the `structure-qc-audit` skill on the coordinate file before passing it to downstream modeling tools.
2. **Disorder Warning**: If more than 30% of alpha-carbon (`CA`) atoms have a B-factor / pLDDT score below `50.0`, explicitly warn the user about disordered or low-confidence regions and report the high-confidence domain boundaries (`pLDDT >= 70`).
```

---

### Pattern 2: Zero-Pollution Python Micro-Environments (`uv` + PEP 723 + Sliding-Window PAE Math)

Running global `pip install` inside a user's repository breaks virtual environments. Instead, every Science skill uses `uv run` with **PEP 723 inline script metadata (`# /// script`)** and enforces rate limits and mathematical heuristics inside deterministic Python scripts.

For example, in `skills/alphafold_database_fetch_and_analyze/scripts/`:
* `fetch_structure.py` uses `polite-http` with a hard `qps=1.0` rate limit (`CLIENT = http_client.HttpClient("https://alphafold.ebi.ac.uk", qps=1.0)`) and automatically falls back to the longest isoform for massive proteins (`> 2,700` amino acids like Dystrophin).
* `analyze_pae.py` forbids the LLM from guessing domain boundaries by running a **20-residue sliding-window Predicted Aligned Error (PAE) clustering algorithm** (`distance_cutoff=7.0 Å`, `min_domain_size=40`, `merge_cutoff=15.0 Å`):

```python
"""Analyzes Predicted Aligned Error (PAE) and detects domain boundaries."""

# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///

def find_sub_domains(pae_matrix, distance_cutoff=7.0, min_domain_size=40):
    """Identifies structurally independent sub-domains based on the PAE matrix."""
    n_res = len(pae_matrix)
    domains, current_domain = [], []

    for i in range(n_res):
        if not current_domain:
            current_domain.append(i)
            continue

        window_size = min(20, len(current_domain))
        recent_res = current_domain[-window_size:]
        pae_sum = sum(pae_matrix[r][i] + pae_matrix[i][r] for r in recent_res)
        avg_pae = pae_sum / (2.0 * window_size)

        if avg_pae < distance_cutoff:
            current_domain.append(i)
        else:
            if len(current_domain) >= min_domain_size:
                domains.append(current_domain)
            current_domain = [i]

    if len(current_domain) >= min_domain_size:
        domains.append(current_domain)
    return [[comp[0] + 1, comp[-1] + 1] for comp in domains]
```

---

### Pattern 3: The Zero-Leak Credential Protocol (`skills/credentials/SKILL.md`)

Genomic and literature APIs like **AlphaGenome** (`ALPHAGENOME_API_KEY`) require secret keys. If an agent asks a user to paste their API key into the chat - or runs `cat ~/.env` - that secret is permanently recorded in the conversation transcript and model context.

The `credentials` skill solves this with a strict **Zero-Leak Protocol**:
1. **Silent Exit-Code Verification:** The agent checks whether the variable exists in `~/.env` using `grep -sq` (quiet + suppress errors), reading *only* the `0` vs. non-zero exit code:

    ```bash
    grep -sq "^ALPHAGENOME_API_KEY=" ~/.env
    ```

2. **Hidden Terminal Prompting (`read -s`):** If missing, the agent stops immediately and outputs a terminal command for the user to run locally where keystrokes are hidden (`read -s`):

    ```bash
    printf "Enter ALPHAGENOME_API_KEY (typing hidden): " && read -s val && echo && echo "ALPHAGENOME_API_KEY=$val" >> "$HOME/.env" && echo "Saved."
    ```

3. **Internal `dotenv` Ingestion:** Helper scripts load `~/.env` internally via `dotenv`, so the key never appears in command-line flags or stdout.

---

### Pattern 4: Background Sidecars (`sidecar.json`) & Custom 3D WebGL / MCP Tool Servers (`mcp_config.json`)

As documented in the public **[Antigravity Sidecars Guide (`antigravity.google/docs/sidecars`)](https://antigravity.google/docs/sidecars)** and **[MCP Guide (`antigravity.google/docs/mcp`)](https://antigravity.google/docs/mcp)**, Antigravity lets plugins pair **Model Context Protocol (`mcp_config.json`)** tool servers with managed background **Sidecar processes (`sidecar.json`)** that support `command`, `builtin` (`schedule`), `args`, `restart_policy` (`always`, `on-failure`, `never`), `description`, `env`, and `display_name`, plus programmatic interaction via `agentapi`.

In our open-source **[Antigravity Science Plugin Cookbook](https://github.com/RobinaMirbahar/antigravity-science-plugin-cookbook)**, we pair a zero-dependency Python Stdio MCP Server (`plugins/genomics-variant-mcp/mcp_config.json`) with a documented background Sidecar worker (`sidecar.json`) and our browser-based **3D PDBe Mol\* / WebGL Biomolecular Studio (`index.html`)**:

```mermaid
sequenceDiagram
    participant User
    participant Agent as Antigravity Agent
    participant AF as Skill: alphafold / pdb / pymol
    participant MCP as Custom MCP: variant_mcp_server.py
    participant Sidecar as Sidecar: worker.py + 3D Studio

    User->>Agent: "Analyze TP53 (UniProt P04637) and evaluate the R248Q DNA-contact hotspot"
    Agent->>AF: uv run scripts/fetch_structure.py P04637 -o <artifact_dir>
    AF-->>Agent: Saved AF-P04637-F1-model_v6.cif + PAE JSON
    Agent->>MCP: score_variant_impact(variant="chr17:7674220:C>T", gene="TP53")
    MCP-->>Agent: Returns AVI score, phyloP100way conservation & domain coordinates
    Agent->>Sidecar: Updates 3D structure state & renders headless PyMOL / 3D WebGL view
```

Here are the two standard configuration files documented in `antigravity.google/docs/mcp` and `antigravity.google/docs/sidecars`:

* **`mcp_config.json` (connecting a local Stdio MCP server at the plugin root):**
  ```json
  {
    "mcpServers": {
      "genomics_variant_mcp": {
        "command": "uv",
        "args": ["run", "mcp/variant_mcp_server.py"],
        "timeoutSeconds": 180
      }
    }
  }
  ```
* **`sidecars/qc_monitor/sidecar.json` (configuring a managed background sidecar process per `antigravity.google/docs/sidecars`):**
  ```json
  {
    "description": "Background 3D structure QC & artifact monitor",
    "display_name": "Structure QC Sidecar",
    "command": "uv",
    "args": ["run", "worker.py"],
    "restart_policy": "on-failure"
  }
  ```

---

### Pattern 5: Domain-Specific Guardrails - From Clinical Genetics (`AlphaGenome`) to Ancient Epigraphy (`Aeneas` & `Ithaca`)

Two of the most fascinating skills in the bundle demonstrate how `SKILL.md` enforces domain-specific scientific rigor:

1. **`alphagenome-variant-impact-score` (Strict Molecular Framing + Context-Overflow Protection):**
   * **Clinical Safety Gate:** Explicitly forbids extrapolating high AlphaGenome Variant Impact (AVI) scores into clinical diagnoses or patient prognosis, restricting outputs to molecular mechanisms (splicing disruption, chromatin accessibility, TF binding, or GENCODE v46 transcript coordinates).
   * **Stdout Overflow Guard:** Warns the agent that `--include_track_info --format json` emits `~3.9 KB` per variant, requiring direct file redirection (`-o query_results.json`) whenever querying `> 3` variants so stdout never floods the context window.
2. **`predictingthepast` (Ancient Latin & Greek Epigraphy with DeepMind's Aeneas & Ithaca):**
   * Restores damaged ancient inscriptions, attributes geographical province + chronological date ranges, and finds parallel inscriptions using special gap syntax (`?` for a single missing character, `#` for an unknown-length damaged gap):
     ```bash
     uv run scripts/preprocess.py --language=latin --input="imp caesar divi f ???????? cos xi"
     ```
   * Enforces a **Self-Contained Epigraphy Rule**: forbids the agent from using web search to "cheat" or override the neural restoration probabilities returned by Aeneas/Ithaca.

---

## 4. Five End-to-End Multi-Skill Use Cases Across the 40 Science Skills

Because all 40 skills share the conversation's artifact directory, Antigravity can chain multiple domain-specific CLI scripts and MCP sidecars in a single research session.

I included a runnable benchmark suite in [`examples/multi_domain_science_use_cases.py`](https://github.com/RobinaMirbahar/antigravity-science-plugin-cookbook/blob/main/examples/multi_domain_science_use_cases.py) (`uv run examples/multi_domain_science_use_cases.py`) that executes and scores all five multi-skill pipelines below:

![5 End-to-End Multi-Skill Pipelines Scorecard](https://raw.githubusercontent.com/RobinaMirbahar/antigravity-science-plugin-cookbook/main/examples/generated_use_cases/science_use_cases_scorecard.png)

---

### Use Case 1: Precision Oncology & 3D Pocket Triage (`ClinVar` → `gnomAD` → `AlphaFold` → `ChEMBL` → `PyMOL / 3D WebGL Studio`)

**Scenario:** A translational oncology team wants to evaluate an **EGFR L858R** (`rs121434568`, `chr7:55191822:T>G`) driver mutation, verify gene loss-of-function constraint, inspect 3D active-site confidence, rank nanomolar kinase inhibitors, and highlight the pocket in 3D.

```bash
# 1. Check allele rarity & gene constraint (pLI / LOEUF) in gnomAD
uv run ~/.gemini/config/plugins/science/skills/gnomad_database/scripts/get_gene_constraint.py \
  --gene EGFR --output ./artifacts/egfr_constraint.json

# 2. Fetch AlphaFold 3D structure (P00533) & audit pLDDT + PAE domains
uv run ~/.gemini/config/plugins/science/skills/alphafold_database_fetch_and_analyze/scripts/fetch_structure.py \
  P00533 -o ./artifacts/P00533/
uv run ~/.gemini/config/plugins/science/skills/alphafold_database_fetch_and_analyze/scripts/analyze_pae.py \
  ./artifacts/P00533/AF-P00533-F1-predicted_aligned_error_v6.json

# 3. Screen ChEMBL for EGFR (CHEMBL203) bioactivities & download 3D SDF ligands
uv run ~/.gemini/config/plugins/science/skills/chembl_database/scripts/chembl_api.py \
  activity --search "EGFR" --limit 10 --output ./artifacts/egfr_chembl_ic50.json
uv run ~/.gemini/config/plugins/science/skills/chembl_database/scripts/chembl_api.py \
  molecule --id CHEMBL939 --dl_format sdf --output ./artifacts/gefitinib.sdf
```

Finally, the agent renders the 3D kinase pocket (`residues 855-862` in chain `A`) using headless PyMOL (`pymol` skill) or our interactive **[3D Biomolecular & Variant WebGL Studio (`index.html`)](https://robinamirbahar.github.io/antigravity-science-plugin-cookbook/)**:

![Use Case 1 - Precision Oncology & 3D Kinase Pocket Triage](https://raw.githubusercontent.com/RobinaMirbahar/antigravity-science-plugin-cookbook/main/examples/generated_use_cases/uc1_precision_oncology_3d.png)

---

### Use Case 2: Non-Coding GWAS Enhancer Variant Triage (`AlphaGenome` → `UCSC phyloP` → `ENCODE cCRE` → `JASPAR` → `GTEx`)

**Scenario:** Over 90% of GWAS risk loci fall in non-coding DNA. Suppose you are investigating `chr1:109274968:G>T` (`rs12740374` at the *SORT1* 1p13 locus) and want to know *how* it alters gene regulation across human tissues without hallucinating clinical diagnoses:

```bash
# 1. Score variant impact across 18 biological modalities + GENCODE v46 coordinates
uv run ~/.gemini/config/plugins/science/skills/alphagenome_variant_impact_score/scripts/alphagenome_atlas_avi.py \
  query "chr1:109274968:G>T" --include_track_info --format json -o ./artifacts/sort1_avi.json

# 2. Check 100-vertebrate evolutionary constraint (phyloP100way & phastCons100way)
uv run ~/.gemini/config/plugins/science/skills/ucsc_conservation_and_tfbs/scripts/get_conservation.py \
  --coordinates "chr1:109274968" --output ./artifacts/sort1_phylop.json

# 3. Fetch Transcription Factor Position Weight Matrices (PWMs) from JASPAR (CEBPA)
uv run ~/.gemini/config/plugins/science/skills/jaspar_database/scripts/jaspar_cli.py \
  search --query "CEBPA" --output ./artifacts/cebpa_jaspar.json
```

* **Engineering Guardrail in Action:** The `alphagenome-variant-impact-score` skill enforces that `--include_track_info` outputs (`~3.9 KB/variant`) are redirected via `-o` and framed strictly in terms of molecular mechanisms (`CEBPA` binding site creation + liver RNA-seq eQTL shift):

![Use Case 2 - Non-Coding GWAS Enhancer Variant Triage](https://raw.githubusercontent.com/RobinaMirbahar/antigravity-science-plugin-cookbook/main/examples/generated_use_cases/uc2_noncoding_alphagenome.png)

---

### Use Case 3: Dark-Proteome Enzyme Discovery (`AlphaFold` → `Foldseek 3D Search` → `InterPro` → `Clustal Omega MSA` → `Headless PyMOL`)

**Scenario:** A protein engineering group wants to discover novel thermostable plastic-degrading **PETase** homologs hidden in environmental metagenomes where sequence identity is below 25% (the "twilight zone" where BLAST fails, but 3D fold geometry is conserved):

```bash
# 1. Search the 3D coordinate file against Foldseek's metagenomic & AlphaFold databases
uv run ~/.gemini/config/plugins/science/skills/foldseek_structural_search/scripts/search.py \
  ./artifacts/PETase_AF.cif \
  --databases afdb50,mgnify_esm30,pdb100,cath50 \
  -o ./artifacts/petase_foldseek.json > ./artifacts/petase_foldseek_summary.md

# 2. Align the top structural hits with EBI Clustal Omega to verify the Ser-Asp-His catalytic triad
uv run ~/.gemini/config/plugins/science/skills/protein_sequence_msa/scripts/clustalo.py \
  --input ./artifacts/petase_homologs.fasta --output ./artifacts/petase_msa.aln
```

* **Engineering Guardrail in Action:** Look at `foldseek-structural-search/SKILL.md`:
  1. **Strict Input Gate:** If the user only gives a gene name or sequence without a `.pdb`/`.cif` file, the skill **halts immediately** and instructs the agent to fetch the 3D structure first.
  2. **Database Allowlist:** Enforces validation against the exact 9 supported Foldseek databases (`afdb50`, `afdb-swissprot`, `pdb100`, `BFVD`, `mgnify_esm30`, `cath50`, `gmgcl_id`, `bfmd`, `afdb-proteome`).
  3. **Headless OSMesa PyMOL Superposition (`pymol` skill):** When generating static publication figures alongside `.pse` session files, the `pymol` skill runs headless via `PYOPENGL_PLATFORM=osmesa` and automatically checks `cmd.count_atoms("name CA") == cmd.count_atoms("all")` so C-alpha-only traces still render as smooth cartoons!

![Use Case 3 - Dark-Proteome Enzyme Discovery with Foldseek](https://raw.githubusercontent.com/RobinaMirbahar/antigravity-science-plugin-cookbook/main/examples/generated_use_cases/uc3_dark_proteome_foldseek.png)

---

### Use Case 4: Clinical Trial Intelligence & Pharmacovigilance Audit (`OpenTargets` → `ClinicalTrials.gov` → `openFDA` → `OpenAlex`)

**Scenario:** A clinical data science team wants to map all recruiting **Phase 3 trials** for a target indication, inspect inclusion/exclusion criteria without overflowing the LLM context window, and audit real-world post-market adverse events across **28 FDA endpoints**:

```bash
# 1. Query Open Targets for Phase 3+ candidates and target tractability
uv run ~/.gemini/config/plugins/science/skills/opentargets_database/scripts/query_opentargets.py \
  --output ./artifacts/nsclc_drugs.json --limit 15 \
  get-disease-drugs MONDO_0005090 --min-stage PHASE_3

# 2. Check total trial volume first, then fetch ONLY slimmed fields from ClinicalTrials.gov APIv2
uv run ~/.gemini/config/plugins/science/skills/clinical_trials_database/scripts/clinical_trials_api.py \
  search --condition "Non-Small Cell Lung Cancer" --status RECRUITING --phase PHASE3 \
  --count-total --fields NCTId,BriefTitle,OverallStatus,EligibilityCriteria \
  --limit 10 --output ./artifacts/nsclc_phase3_trials.json

# 3. Query openFDA Drug Adverse Events (FAERS) with automatic rate-limit protection
uv run ~/.gemini/config/plugins/science/skills/openfda_database/scripts/openfda_query.py \
  count --category drug --endpoint event \
  --search "patient.drug.medicinalproduct:osimertinib" \
  --count "patient.reaction.reactionmeddrapt.exact" \
  --limit 10 --output ./artifacts/osimertinib_faers_counts.json
```

* **Engineering Guardrails in Action:**
  * **ClinicalTrials.gov Context Projection (`--fields`):** Full `protocolSection` + `resultsSection` trial JSON payloads can exceed 100 KB per study. `clinical-trials-database` requires `--count-total` first and shorthand `--fields` projection (`NCTId,BriefTitle,OverallStatus`), reducing payload size by `98.7%`.
  * **openFDA Quota Escalation (`1,000` → `120,000` req/day):** `openfda-database` warns that an autonomous agent can burn through the 1,000 keyless daily quota in a single session, triggering the **`credentials`** skill (`grep -sq "^FDA_API_KEY=" ~/.env`) before running multi-query workflows:

![Use Case 4 - Clinical Trial Portfolio & openFDA FAERS Safety Audit](https://raw.githubusercontent.com/RobinaMirbahar/antigravity-science-plugin-cookbook/main/examples/generated_use_cases/uc4_clinical_trials_openfda.png)

---

### Use Case 5: Systems Biology & Ancient Epigraphy (`STRING` → `Reactome` & DeepMind's `Aeneas` / `Ithaca`)

Two more specialized workflows show how the Science plugin handles **ambiguous biological identifiers** and **digital humanities**:

1. **Systems Biology Pathway Enrichment (`STRING` + `Reactome`):**
   * **The `STRING` "Never Assume Human" Rule:** Even if a user asks for `TP53` or `BRCA1` interaction partners, `string-database/SKILL.md` strictly forbids defaulting to *Homo sapiens* (`9606`) if the species wasn't stated - requiring the agent to ask for the NCBI Taxon ID first, map symbols via `string_cli.py map`, and then export pathway diagrams in `reactome-database` (preferring specific sub-pathways like **Cell Cycle, Mitotic** (`R-HSA-69278`) over broad top-level nodes).
2. **Restoring Damaged Roman & Greek Stone Inscriptions (`predictingthepast`):**
   * Powered by Google DeepMind's **Aeneas** (Latin) and **Ithaca** (Ancient Greek) models:
     ```bash
     # Preprocess damaged Latin epigraphy (? = single missing character, # = unknown-length gap)
     uv run ~/.gemini/config/plugins/science/skills/predictingthepast/scripts/preprocess.py \
       --language=latin \
       --input="imp caesar divi f ???????? cos xi trib potest"
     ```
   * Returns ranked character restorations (`augustus`, `96.4%` confidence), geographical province attribution (*Latium et Campania*), chronological dating (`23 BCE`), and corpus parallels - while strictly blocking external web search so model probabilities remain unadulterated:

![Use Case 5 - Ancient Roman & Greek Epigraphy Restoration](https://raw.githubusercontent.com/RobinaMirbahar/antigravity-science-plugin-cookbook/main/examples/generated_use_cases/uc5_aeneas_latin_epigraphy.png)

---

## 5. Hands-On Cookbook: Build & Run the Custom `bio-structural-qc` Plugin

In the companion repository (**[RobinaMirbahar/antigravity-science-plugin-cookbook](https://github.com/RobinaMirbahar/antigravity-science-plugin-cookbook)**), I built a complete, installable custom plugin called **`bio-structural-qc`** plus a zero-dependency **3D Protein + PAE Generator & SVG Dashboard (`examples/generate_3d_protein_pae_demo.py`)**.

![AlphaFold pLDDT Profile & PAE Domain Matrix](https://raw.githubusercontent.com/RobinaMirbahar/antigravity-science-plugin-cookbook/main/examples/generated_p53_demo/p53_plddt_pae_dashboard.png)

### Directory Structure of `bio-structural-qc`

```text
plugins/bio-structural-qc/
├── plugin.json                                    # Manifest & 3 starter prompts
├── hooks.json                                     # PostToolUse command reproducibility hook
├── assets/
│   └── logo.svg                                   # 128x128 high-contrast SVG icon
├── rules/
│   └── AGENTS.md                                  # Mandatory QC gate before docking/Foldseek
├── scripts/
│   └── log_reproducibility_audit.py               # Redacts secrets + hashes scripts & input files
└── skills/
    └── structure-qc-audit/
        ├── SKILL.md                               # Progressive-disclosure instructions
        └── scripts/
            └── audit_structure.py                 # PEP 723 C-alpha B-factor/pLDDT auditor
```

### 1. The Always-On QC Gate (`plugins/bio-structural-qc/rules/AGENTS.md`)

```markdown
# Biomolecular Structure QC Gate

Whenever a workflow downloads or modifies a 3D coordinate file (`.pdb`, `.cif`, or `.mmcif`) for downstream structural analysis, homology search, or variant mapping:

1. **Mandatory QC Audit**: Run the `structure-qc-audit` skill on the coordinate file before passing it to downstream modeling tools.
2. **Disorder Warning**: If more than 30% of alpha-carbon (`CA`) atoms have a B-factor / pLDDT score below `50.0`, explicitly warn the user about disordered or low-confidence regions and report the high-confidence domain boundaries (`pLDDT >= 70`) before rendering.
```

### 2. The Zero-Dependency PEP 723 Structure Auditor (`audit_structure.py`)

```python
#!/usr/bin/env python3
"""Audits PDB and mmCIF coordinate files for chain completeness and B-factor/pLDDT distribution."""

# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///

import argparse, json, statistics
from pathlib import Path

def parse_ca_bfactors(filepath: Path) -> dict:
    chains: dict[str, list[tuple[int, float]]] = {}
    ext = filepath.suffix.lower()
    with filepath.open("r", encoding="utf-8", errors="replace") as f:
        for line in f:
            if ext == ".pdb" and line.startswith("ATOM  ") and line[12:16].strip() == "CA":
                chain_id = line[21].strip() or "A"
                chains.setdefault(chain_id, []).append((int(line[22:26]), float(line[60:66])))
            elif ext in {".cif", ".mmcif"} and line.startswith("ATOM "):
                parts = line.split()
                if len(parts) >= 15 and parts[3] == "CA":
                    chains.setdefault(parts[6], []).append((int(parts[8]), float(parts[14])))
    return chains
```

Test both the 3D generator and the QC auditor in two commands using `uv run`:

```bash
git clone https://github.com/RobinaMirbahar/antigravity-science-plugin-cookbook.git
cd antigravity-science-plugin-cookbook

# 1. Generate a 56-residue 3-domain 3D .pdb structure, PAE matrix JSON, and SVG dashboard
uv run examples/generate_3d_protein_pae_demo.py

# 2. Audit both the synthetic multi-domain protein and the Crambin structure
uv run plugins/bio-structural-qc/skills/structure-qc-audit/scripts/audit_structure.py \
  examples/generated_p53_demo/synthetic_p53_multidomain.pdb \
  examples/sample_crambin_fragment.pdb
```

Output:

```json
[
  {
    "file": "synthetic_p53_multidomain.pdb",
    "status": "PASS",
    "total_ca_residues": 56,
    "overall_mean_score": 82.11,
    "overall_pct_low_lt_50": 17.9,
    "chains": {
      "A": {
        "residue_count": 56,
        "mean_score": 82.11,
        "median_score": 90.26,
        "pct_high_confidence_ge_70": 82.1,
        "pct_low_confidence_lt_50": 17.9,
        "high_confidence_span": [11, 56]
      }
    }
  }
]
```

### 3. Reproducibility Lifecycle Hook (`hooks.json` & `log_reproducibility_audit.py`)

A bare timestamp log only tells you *when* `run_command` fired, not *what* actually executed or which version of a script and input `.pdb`/`.cif` coordinates produced a scientific result. At the same time, logging raw shell commands is dangerous if an inline environment variable or `--api-key` flag is present.

Because Antigravity passes a structured JSON payload to every `PostToolUse` hook over `stdin` (`toolCall.args.CommandLine`, `workspacePaths`, `conversationId`, `stepIdx`), we can wire `plugins/bio-structural-qc/hooks.json` to a zero-dependency PEP 723 audit script (`plugins/bio-structural-qc/scripts/log_reproducibility_audit.py`) that:
1. **Redacts Secrets Before Logging:** Strips any environment variables matching `*KEY*`, `*TOKEN*`, `*SECRET*`, `*PASS*`, `*CRED*`, or `*AUTH*`, plus `Bearer`/`Basic` headers and `--api-key`/`--token` CLI flags.
2. **Records Exact Script Versions & Git State:** Captures `git rev-parse --short HEAD` (`+dirty` if uncommitted changes exist) and computes a 16-character SHA-256 digest (`script_versions`) for every executed `.py` or `.sh` script.
3. **Hashes All Referenced Input & Output Files:** Tokenizes the command line and computes SHA-256 digests (`file_hashes`) for every referenced `.pdb`, `.cif`, `.mmcif`, `.vcf`, `.json`, `.fasta`, or `.sdf` file.
4. **Honors the `PostToolUse` Stdout Contract:** Appends the JSONL record to `~/.gemini/qc_command_audit.jsonl` and emits `{}` on `stdout`.

* **`plugins/bio-structural-qc/hooks.json`:**

```json
{
  "qc-command-audit-log": {
    "enabled": true,
    "PostToolUse": [
      {
        "matcher": "run_command",
        "hooks": [
          {
            "type": "command",
            "command": "uv run plugins/bio-structural-qc/scripts/log_reproducibility_audit.py",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

* **`plugins/bio-structural-qc/scripts/log_reproducibility_audit.py` (Core Redaction & Hashing Logic):**

```python
#!/usr/bin/env python3
"""PostToolUse reproducibility hook: logs redacted commands, script SHA-256 versions, and input file hashes."""

# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///

import datetime, hashlib, json, pathlib, re, shlex, subprocess, sys

SECRET_PATTERNS = [
    (re.compile(r"\b([A-Za-z0-9_]*(?:KEY|TOKEN|SECRET|PASS|PASSWORD|CRED|AUTH)[A-Za-z0-9_]*)\s*=\s*('[^']*'|\"[^\"]*\"|\S+)", re.I), r"\1=[REDACTED]"),
    (re.compile(r"(Bearer|Basic)\s+[A-Za-z0-9._\-+/=]+", re.I), r"\1 [REDACTED]"),
    (re.compile(r"(--(?:api[-_]?key|token|secret|password)|x-goog-api-key:|api-key:)\s*([=:]?\s*)('[^']*'|\"[^\"]*\"|\S+)", re.I), r"\1\2[REDACTED]"),
]
TRACKED_EXTENSIONS = {".py", ".sh", ".pdb", ".cif", ".mmcif", ".json", ".fasta", ".fa", ".aln", ".sdf", ".vcf", ".gtf", ".tsv", ".csv"}

def redact_secrets(cmd: str) -> str:
    for pattern, repl in SECRET_PATTERNS:
        cmd = pattern.sub(repl, cmd)
    return cmd

def sha256_file(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return f"sha256:{h.hexdigest()[:16]}"
```

#### Verified Commands: Test Secret Redaction & Input File Hashing Locally

You can verify both the built-in `--self-test` mode and the live `stdin` hook contract in two commands:

```bash
# 1. Run the built-in self-test (simulates an inline ALPHAGENOME_API_KEY + 2 PDB input files)
uv run plugins/bio-structural-qc/scripts/log_reproducibility_audit.py --self-test

# 2. Simulate Antigravity's PostToolUse stdin payload and inspect ~/.gemini/qc_command_audit.jsonl
printf '{"conversationId":"conv-demo","stepIdx":1,"toolCall":{"name":"run_command","args":{"CommandLine":"FDA_API_KEY=secret123 uv run plugins/bio-structural-qc/skills/structure-qc-audit/scripts/audit_structure.py examples/sample_crambin_fragment.pdb"} } }' \
  | uv run plugins/bio-structural-qc/scripts/log_reproducibility_audit.py
tail -n 1 ~/.gemini/qc_command_audit.jsonl
```

Verified `--self-test` output:

```json
{
  "timestamp_utc": "2026-10-24T19:27:00.315004+00:00",
  "event": "PostToolUse",
  "tool": "run_command",
  "conversation_id": "conv-repro-demo-01",
  "step_idx": 7,
  "git_revision": "06fd7e9",
  "redacted_command": "ALPHAGENOME_API_KEY=[REDACTED] uv run plugins/bio-structural-qc/skills/structure-qc-audit/scripts/audit_structure.py examples/generated_p53_demo/synthetic_p53_multidomain.pdb examples/sample_crambin_fragment.pdb",
  "script_versions": {
    "plugins/bio-structural-qc/skills/structure-qc-audit/scripts/audit_structure.py": "sha256:b305f0ca720d7673"
  },
  "file_hashes": {
    "examples/generated_p53_demo/synthetic_p53_multidomain.pdb": "sha256:f929c693e8e2fbfa",
    "examples/sample_crambin_fragment.pdb": "sha256:5ddc4bb4a2f0e889"
  },
  "status": "OK"
}
```

### 4. Interactive 1-Command Plugin Scaffolder & Loader Validator (`scaffold_custom_plugin.py`)

To make authoring and testing your own plugins effortless, I also included an interactive **1-Command Plugin Scaffolder & Loader Validator** ([`examples/scaffold_custom_plugin.py`](https://github.com/RobinaMirbahar/antigravity-science-plugin-cookbook/blob/main/examples/scaffold_custom_plugin.py)) that:
1. **Validates** any plugin directory against Antigravity's loader rules (`plugin.json` allowed keys, relative logo path, `<= 24,000`-byte per-file rule cap, root `hooks.json` placement, and `SKILL.md` YAML frontmatter).
2. **Scaffolds** a complete new plugin bundle (`plugin.json`, `assets/logo.svg`, `rules/AGENTS.md`, `hooks.json`, `SKILL.md`, and a PEP 723 `scripts/run_tool.py` CLI script) in a single command:

```bash
# 1. Validate all 3 starter plugins in the cookbook repository
uv run examples/scaffold_custom_plugin.py

# 2. Scaffold a brand-new custom plugin bundle from scratch
uv run examples/scaffold_custom_plugin.py \
  --scaffold my-genomics-qc \
  --skill vcf-filter-audit \
  --description "Deterministic VCF quality filtering and AlphaGenome coordinate readiness checks."

# 3. Install into your global Antigravity plugins directory
cp -r plugins/bio-structural-qc ~/.gemini/config/plugins/bio-structural-qc
cp -r plugins/genomics-variant-mcp ~/.gemini/config/plugins/genomics-variant-mcp
cp -r plugins/epigraphy-citation-kit ~/.gemini/config/plugins/epigraphy-citation-kit
```

---

## 6. Deep Dive: The 4 Public Antigravity MCP Server Patterns + 2 More Starter Plugins (`genomics-variant-mcp` & `epigraphy-citation-kit`)

As documented in the public **[Antigravity MCP Guide (`antigravity.google/docs/mcp`)](https://antigravity.google/docs/mcp)**, `mcp_config.json` supports **four core server connection patterns** across local developer tools and Google Cloud services:

### A. The 4 Documented `mcp_config.json` Patterns

1. **Pattern 1 - Local Stdio Subprocess (`command` + `args` + `env`):**
   Spawns a local MCP process over `stdio` using `uv`, `node`, `python3`, or `dart` (for example, our cookbook's `genomics_variant_mcp` server or local SQLite/file-system explorers).
2. **Pattern 2 - Google-Credentials Authenticated HTTP (`authProviderType: "google_credentials"`):**
   Connects directly to managed Google Cloud and developer MCP endpoints (such as **BigQuery**, **AlloyDB for PostgreSQL**, **Spanner**, **Cloud SQL**, **Bigtable**, **Dataplex**, and **Google Developer Knowledge** at `https://developerknowledge.googleapis.com/mcp`) using local Application Default Credentials (`gcloud auth application-default login`).
3. **Pattern 3 - Remote Streamable HTTP with Custom Headers (`serverUrl` + `headers` + `timeoutSeconds`):**
   Connects to remote Streamable HTTP MCP endpoints (such as `https://gemini-api-docs-mcp.dev` for `gemini_search_docs` and `gemini_get_doc`) with custom `Authorization` headers and configurable timeouts (`timeoutSeconds: 600`).
4. **Pattern 4 - OAuth 2.0 Remote Servers (Dynamic Client Registration or Manual `oauth` Object):**
   Authenticates against remote SaaS and enterprise MCP servers using automatic OAuth Dynamic Client Registration (DCR) or a manual `oauth` (`clientId`, `clientSecret`) configuration redirecting to `https://antigravity.google/oauth-callback`.

### B. Starter Plugin #2: `plugins/genomics-variant-mcp` (Custom Python Stdio MCP Server + Specialist Subagent)

To show how to package your own **MCP server** and **Specialist Subagent** inside an Antigravity plugin, the cookbook includes **[`plugins/genomics-variant-mcp`](https://github.com/RobinaMirbahar/antigravity-science-plugin-cookbook/tree/main/plugins/genomics-variant-mcp)**:

* **[`mcp_config.json`](https://github.com/RobinaMirbahar/antigravity-science-plugin-cookbook/blob/main/plugins/genomics-variant-mcp/mcp_config.json)** - Registers `genomics_variant_mcp` via `uv run mcp/variant_mcp_server.py` and marks both tools as `"eager": true` so they load directly into the agent's native tool declarations:
  ```json
  {
    "mcpServers": {
      "genomics_variant_mcp": {
        "command": "uv",
        "args": ["run", "mcp/variant_mcp_server.py"],
        "tools": [
          { "name": "score_variant_impact", "eager": true },
          { "name": "evaluate_lipinski_ro5", "eager": true }
        ]
      }
    }
  }
  ```
* **[`mcp/variant_mcp_server.py`](https://github.com/RobinaMirbahar/antigravity-science-plugin-cookbook/blob/main/plugins/genomics-variant-mcp/mcp/variant_mcp_server.py)** - A zero-dependency PEP 723 JSON-RPC 2.0 Stdio MCP server implementing `initialize`, `tools/list`, and `tools/call` for:
  * `score_variant_impact`: Scores 1-based `chr:pos:ref>alt` SNVs (transition/transversion class, predicted AlphaGenome AVI impact score, PhyloP 100-way conservation, and molecular priority).
  * `evaluate_lipinski_ro5`: Evaluates small-molecule leads against Lipinski's Rule of Five (`MW ≤ 500`, `LogP ≤ 5`, `HBD ≤ 5`, `HBA ≤ 10`) and Veber's polar surface area rule (`PSA ≤ 140 Å²`).
* **[`agents/clinical-variant-curator.md`](https://github.com/RobinaMirbahar/antigravity-science-plugin-cookbook/blob/main/plugins/genomics-variant-mcp/agents/clinical-variant-curator.md)** - A specialist subagent (modeled on `firebase`'s `agents/firestore-rules-author.md`) with YAML frontmatter (`mainAgent: true`, `subagent: true`, `commandExecutionPolicy: auto`) that enforces research-only molecular framing.

Run its built-in self-test with `uv`:
```bash
uv run plugins/genomics-variant-mcp/mcp/variant_mcp_server.py --self-test
```

### C. Starter Plugin #3: `plugins/epigraphy-citation-kit` (Ancient Epigraphy Validator + `PreToolUse` Hook)

The third starter plugin, **[`plugins/epigraphy-citation-kit`](https://github.com/RobinaMirbahar/antigravity-science-plugin-cookbook/tree/main/plugins/epigraphy-citation-kit)**, pairs a `PreToolUse` lifecycle hook (`hooks.json`) with a PEP 723 Leiden bracket normalizer ([`validate_epigraphy.py`](https://github.com/RobinaMirbahar/antigravity-science-plugin-cookbook/blob/main/plugins/epigraphy-citation-kit/skills/epigraphy-gap-validator/scripts/validate_epigraphy.py)) that automatically converts standard Leiden epigraphic brackets (`[---]` and `[...]`) into DeepMind Aeneas/Ithaca `#` and `?` tokens, checks for forbidden `##` or `?#` sequences, and pads short inscriptions to the 25-character minimum:

```bash
uv run plugins/epigraphy-citation-kit/skills/epigraphy-gap-validator/scripts/validate_epigraphy.py \
  --text "IMP CAESAR DIVI F [---] COS [...] III" --language latin
```

---

## 7. Bonus: Distilling Live Chat Sessions into Skills & Auditing Installed Bundles

### A. Automatic Skill Distillation with `workflow-skill-creator`
Don't want to write `SKILL.md` files from scratch? After completing any multi-step scientific workflow in chat, trigger the Science plugin's **`workflow-skill-creator`** skill:
> *"Package the workflow we just ran into a reusable skill."*

It walks you through a mandatory **4-round brainstorming protocol** (confirming inputs/outputs, error-handling rigidity, composing existing Science skills without duplicating code, and generating a CLI helper script) before writing the new skill to `~/.gemini/config/skills/<name>/`.

### B. Managing Plugins with `/plugin` & Auditing Installed Bundles (`inspect_installed_plugins.py`)
In Google Antigravity, you can install, enable, disable, or package plugins interactively using the built-in **`/plugin`** slash command or the **Customizations -> Plugins** panel in the UI.
* **Directory-Keyed Discovery:** Antigravity resolves each installed bundle by its directory name under `~/.gemini/config/plugins/<dir>/` (or workspace `.agents/plugins/<dir>/`).
* **Zero-Context-Bloat Inventory:** Never dump raw `SKILL.md` bodies across all installed plugins into your shell prompt. Instead, run [`examples/inspect_installed_plugins.py`](https://github.com/RobinaMirbahar/antigravity-science-plugin-cookbook/blob/main/examples/inspect_installed_plugins.py) to summarize manifest versions, skill counts, active `hooks.json` files, `mcp_config.json` servers, and `sidecar.json` views:

```bash
# Audit the 3 cookbook plugins in ./plugins
uv run examples/inspect_installed_plugins.py

# Or audit your global Antigravity plugins directory
uv run examples/inspect_installed_plugins.py --root ~/.gemini/config/plugins
```

### C. Installing & Inspecting Plugins from the Shell with `agy plugin`
As documented in the **[Antigravity Plugins Guide (`antigravity.google/docs/plugins`)](https://antigravity.google/docs/plugins)**, you can install the open-source DeepMind Science skills or our cookbook plugins directly via `npx` or the `agy plugin` CLI:
```bash
# Install Google DeepMind's open-source science-skills bundle
npx skills add google-deepmind/science-skills/

# Or install and inspect plugins using the Antigravity CLI
agy plugin install https://github.com/google-deepmind/science-skills
agy plugin list --json
```

---

## 8. Official Documentation & Scientific Database References

### A. Official Google Antigravity Documentation
* **[Google DeepMind Science Skills Open-Source Repository (`github.com/google-deepmind/science-skills`)](https://github.com/google-deepmind/science-skills)**
* **[Google Antigravity Science Use Cases & Demos (`antigravity.google/use-cases/science`)](https://antigravity.google/use-cases/science)**
* **[Google Antigravity Documentation Home (`antigravity.google/docs`)](https://antigravity.google/docs)**
* **[Plugins Guide (`antigravity.google/docs/plugins`)](https://antigravity.google/docs/plugins)**
* **[Progressive-Disclosure Skills Guide (`antigravity.google/docs/skills`)](https://antigravity.google/docs/skills)**
* **[Rules & Workflows Guide (`antigravity.google/docs/rules-workflows`)](https://antigravity.google/docs/rules-workflows)**
* **[Lifecycle Hooks Guide (`antigravity.google/docs/hooks`)](https://antigravity.google/docs/hooks)**
* **[Auxiliary Pane Sidecars Guide (`antigravity.google/docs/sidecars`)](https://antigravity.google/docs/sidecars)**
* **[Model Context Protocol (MCP) Guide (`antigravity.google/docs/mcp`)](https://antigravity.google/docs/mcp)**
* **[Agent Permissions & Security (`antigravity.google/docs/permissions`)](https://antigravity.google/docs/permissions)**
* **[Google Antigravity Python SDK (`github.com/google-antigravity/antigravity-sdk-python`)](https://github.com/google-antigravity/antigravity-sdk-python)**

### B. Scientific AI Models, Databases & Open-Source Viewers
* **[Google DeepMind AlphaGenome (`deepmind.google.com/science/alphagenome`)](https://deepmind.google.com/science/alphagenome/)**
* **[AlphaFold Protein Structure Database (`alphafold.ebi.ac.uk`)](https://alphafold.ebi.ac.uk/)**
* **[Google DeepMind Aeneas & Ithaca - Predicting the Past (`predictingthepast.com`)](https://predictingthepast.com/)**
* **[PDBe Mol\* 3D Biomolecular WebGL Viewer (`github.com/molstar/pdbe-molstar`)](https://github.com/molstar/pdbe-molstar)**
* **[Foldseek Structural Similarity Search (`search.foldseek.com`)](https://search.foldseek.com/search)**
* **[EMBL-EBI ChEMBL Bioactivity Database (`ebi.ac.uk/chembl`)](https://www.ebi.ac.uk/chembl/)**, **[gnomAD (`gnomad.broadinstitute.org`)](https://gnomad.broadinstitute.org/)**, **[NCBI ClinVar (`ncbi.nlm.nih.gov/clinvar`)](https://www.ncbi.nlm.nih.gov/clinvar/)**, **[Open Targets Platform (`platform.opentargets.org`)](https://platform.opentargets.org/)**, **[openFDA API (`open.fda.gov/apis`)](https://open.fda.gov/apis/)**, and **[ClinicalTrials.gov APIv2 (`clinicaltrials.gov`)](https://clinicaltrials.gov/)**

### C. Licensing, Academic Citations & Dataset Acknowledgements
* **Google Antigravity Science Plugin License (`README.md` & `SKILL_LICENSES.md`):** Copyright 2026 Google LLC. All software and helper scripts in the Science Plugin (including `analyze_pae.py`) are licensed under the **[Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0)**, and all skill definitions and documentation materials (including `SKILL.md` and `rules/AGENTS.md`) are licensed under the **[Creative Commons Attribution 4.0 International License (CC-BY 4.0)](https://creativecommons.org/licenses/by/4.0/legalcode)**. Third-party biological and clinical databases referenced by individual skills are governed by their respective terms listed in `SKILL_LICENSES.md`.
* **Google DeepMind `predictingthepast` (`Aeneas` & `Ithaca`) Citations:**
  * **Aeneas (Latin):** Assael, Y., Sommerschield, T., Cooley, A. et al. *Contextualizing ancient texts with generative neural networks.* **Nature** 645, 141-147 (2025). ([github.com/google-deepmind/predictingthepast](https://github.com/google-deepmind/predictingthepast))
  * **Ithaca (Ancient Greek):** Assael, Y., Sommerschield, T., Shillingford, B. et al. *Restoring and attributing ancient texts using deep neural networks.* **Nature** 603, 280-283 (2022).
* **Epigraphic Dataset Acknowledgements (`predictingthepast`):**
  * **Ithaca (Ancient Greek):** Draws on the 2019 version of the *Searchable Greek Inscriptions* database made available under Fair Use license by the **Packard Humanities Institute**, generously supported by David Packard ([inscriptions.packhum.org](https://inscriptions.packhum.org)).
  * **Aeneas (Latin):** Trained on data from the **Epigraphic Database Roma (EDR)** ([edr-edr.it](http://www.edr-edr.it/), CC-BY 4.0 on [Zenodo](https://zenodo.org/records/3575495)), the **Epigraphic Database Heidelberg (EDH)** ([edh.ub.uni-heidelberg.de](https://edh.ub.uni-heidelberg.de/), CC-BY-SA 4.0 on [Zenodo](https://zenodo.org/records/3575155)), and the **ETL repository for Epigraphic Database Clauss-Slaby (`EDCS_ETL`)** ([manfredclauss.de](http://www.manfredclauss.de/) and [github.com/sdam-au/EDCS_ETL](https://github.com/sdam-au/EDCS_ETL), CC-BY 4.0 on [Zenodo](https://zenodo.org/records/7072337)).

---

## Support, Star, Fork & Contribute on GitHub

If you find the **Antigravity Science Plugin Cookbook & Interactive 3D WebGL Studio** useful for your research or engineering workflows:

* **Star this Repository:** [**Star `RobinaMirbahar/antigravity-science-plugin-cookbook` on GitHub**](https://github.com/RobinaMirbahar/antigravity-science-plugin-cookbook) to bookmark the 3 starter plugins and help other developers discover the cookbook.
* **Fork & Customize:** [**Fork `RobinaMirbahar/antigravity-science-plugin-cookbook`**](https://github.com/RobinaMirbahar/antigravity-science-plugin-cookbook/fork) to scaffold and publish your own custom [**Google Antigravity (`@google-antigravity`)**](https://antigravity.google/docs) plugins, progressive-disclosure skills, and MCP servers.
* **Play Live in Your Browser:** [**Launch the Interactive 3D Biomolecular & Variant WebGL Studio**](https://robinamirbahar.github.io/antigravity-science-plugin-cookbook/)

### Official Ecosystem Links & Tags
* **Google:** [github.com/google (`@google`)](https://github.com/google) | [about.google](https://about.google/)
* **Google Gemini API & SDKs:** [github.com/google-gemini (`@google-gemini`)](https://github.com/google-gemini) | [ai.google.dev/gemini-api/docs](https://ai.google.dev/gemini-api/docs)
* **Google DeepMind Science & Models:** [github.com/google-deepmind (`@google-deepmind`)](https://github.com/google-deepmind) | [deepmind.google](https://deepmind.google/) | [AlphaGenome](https://deepmind.google.com/science/alphagenome/) | [AlphaFold](https://alphafold.ebi.ac.uk/) | [Aeneas & Ithaca](https://predictingthepast.com/)
* **Google Antigravity Platform:** [antigravity.google/docs](https://antigravity.google/docs) | [antigravity.google/use-cases/science](https://antigravity.google/use-cases/science) | [github.com/google-antigravity (`@google-antigravity`)](https://github.com/google-antigravity/antigravity-sdk-python)
* **Google Cloud Platform:** [github.com/GoogleCloudPlatform (`@GoogleCloudPlatform`)](https://github.com/GoogleCloudPlatform) | [cloud.google.com](https://cloud.google.com/)

Let me know in the comments what domain you're packaging into an Antigravity plugin next - whether it's **3D structural biology**, **genomic variant scoring**, **ancient epigraphy**, or **autonomous cloud SRE**!
