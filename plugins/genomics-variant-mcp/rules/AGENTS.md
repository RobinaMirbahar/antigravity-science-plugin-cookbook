# Genomics Variant MCP & Subagent Delegation Rules

- When triaging single nucleotide variants (`chr:pos:ref>alt`) or checking small-molecule oral bioavailability (Lipinski Rule of 5), use the eager tools exposed by `genomics_variant_mcp` (`score_variant_impact` and `evaluate_lipinski_ro5`).
- When auditing a batch of variants across multiple genes, delegate the curation task to the `clinical-variant-curator` subagent so the main conversation context stays compact.
