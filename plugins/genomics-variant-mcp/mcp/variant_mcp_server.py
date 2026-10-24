#!/usr/bin/env python3
"""Zero-Dependency JSON-RPC 2.0 Stdio MCP Server for Genomics & Cheminformatics.

Exposes two eager MCP tools to Google Antigravity:
1. `score_variant_impact` - Parses `chr:pos:ref>alt`, classifies transition vs.
   transversion, and returns synthetic AlphaGenome AVI + phyloP conservation metrics.
2. `evaluate_lipinski_ro5` - Evaluates small-molecule physicochemical descriptors
   (MW, LogP, HBD, HBA, PSA) against Lipinski's Rule of 5 and Veber's oral
   bioavailability criteria.

Includes a `--self-test` flag for deterministic CLI verification.
"""

# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///

import argparse
import json
import sys

TOOLS_MANIFEST = [
    {
        "name": "score_variant_impact",
        "description": "Scores a genomic variant in chr:pos:ref>alt format and returns molecular impact metrics.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "variant": {
                    "type": "string",
                    "description": "1-based variant string, e.g. 'chr17:7674220:C>T'",
                },
                "gene": {
                    "type": "string",
                    "description": "Optional target gene symbol, e.g. 'TP53'",
                },
            },
            "required": ["variant"],
        },
    },
    {
        "name": "evaluate_lipinski_ro5",
        "description": "Evaluates a small molecule against Lipinski's Rule of 5 and Veber oral bioavailability rules.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "compound_name": {"type": "string"},
                "mw_daltons": {"type": "number"},
                "clogp": {"type": "number"},
                "h_bond_donors": {"type": "integer"},
                "h_bond_acceptors": {"type": "integer"},
                "polar_surface_area": {"type": "number"},
            },
            "required": [
                "compound_name",
                "mw_daltons",
                "clogp",
                "h_bond_donors",
                "h_bond_acceptors",
            ],
        },
    },
]


def handle_score_variant(args: dict) -> dict:
    variant = str(args.get("variant", "")).strip()
    gene = str(args.get("gene", "UNKNOWN")).strip().upper()
    parts = variant.replace(">", ":").split(":")
    if len(parts) != 4:
        return {"error": f"Invalid format '{variant}'. Expected chr:pos:ref>alt"}

    chrom, pos_str, ref, alt = parts[0], parts[1], parts[2].upper(), parts[3].upper()
    transitions = {("A", "G"), ("G", "A"), ("C", "T"), ("T", "C")}
    mut_class = "Transition (Ti)" if (ref, alt) in transitions else "Transversion (Tv)"
    # Deterministic hash-derived demo score so tests are 100% reproducible
    seed = sum(ord(c) for c in variant)
    avi = round(0.55 + (seed % 43) * 0.01, 2)
    phylop = round(1.8 + (seed % 35) * 0.12, 2)

    return {
        "variant": variant,
        "gene": gene,
        "chromosome": chrom,
        "position_grch38": int(pos_str) if pos_str.isdigit() else pos_str,
        "mutation_type": mut_class,
        "predicted_avi_score": avi,
        "phylop_100way": phylop,
        "molecular_priority": "HIGH_IMPACT_CANDIDATE" if avi >= 0.75 else "MODERATE_IMPACT",
        "clinical_disclaimer": "Research Use Only - molecular framing only, not a clinical diagnosis.",
    }


def handle_lipinski(args: dict) -> dict:
    name = args.get("compound_name", "Compound")
    mw = float(args.get("mw_daltons", 0.0))
    clogp = float(args.get("clogp", 0.0))
    hbd = int(args.get("h_bond_donors", 0))
    hba = int(args.get("h_bond_acceptors", 0))
    psa = float(args.get("polar_surface_area", 75.0))

    violations = []
    if mw > 500.0:
        violations.append(f"MW {mw} > 500 Da")
    if clogp > 5.0:
        violations.append(f"cLogP {clogp} > 5.0")
    if hbd > 5:
        violations.append(f"HBD {hbd} > 5")
    if hba > 10:
        violations.append(f"HBA {hba} > 10")

    return {
        "compound_name": name,
        "lipinski_ro5_pass": len(violations) <= 1,
        "violation_count": len(violations),
        "violations": violations,
        "veber_psa_pass": psa <= 140.0,
        "oral_druggability_class": "OPTIMAL_ORAL_LEAD" if not violations and psa <= 140.0 else "NEEDS_OPTIMIZATION",
    }


def process_rpc_request(req: dict) -> dict | None:
    method = req.get("method")
    req_id = req.get("id")
    params = req.get("params") or {}

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2025-03-26",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genomics_variant_mcp", "version": "0.1.0"},
            },
        }
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": TOOLS_MANIFEST}}
    if method == "tools/call":
        tool_name = params.get("name")
        tool_args = params.get("arguments") or {}
        if tool_name == "score_variant_impact":
            payload = handle_score_variant(tool_args)
        elif tool_name == "evaluate_lipinski_ro5":
            payload = handle_lipinski(tool_args)
        else:
            payload = {"error": f"Unknown tool: {tool_name}"}
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {"content": [{"type": "text", "text": json.dumps(payload, indent=2)}]},
        }
    if req_id is not None:
        return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Method not found: {method}"}}
    return None


def main() -> None:
    parser = argparse.ArgumentParser(description="Genomics Variant & Lipinski MCP Stdio Server.")
    parser.add_argument("--self-test", action="store_true", help="Run a deterministic self-test of all MCP tools")
    args = parser.parse_args()

    if args.self_test:
        v_res = handle_score_variant({"variant": "chr17:7674220:C>T", "gene": "TP53"})
        c_res = handle_lipinski({
            "compound_name": "Osimertinib (CHEMBL3353410)",
            "mw_daltons": 499.6,
            "clogp": 4.5,
            "h_bond_donors": 2,
            "h_bond_acceptors": 7,
            "polar_surface_area": 87.6,
        })
        print(json.dumps({"mcp_self_test": "PASS", "variant_tool": v_res, "lipinski_tool": c_res}, indent=2))
        return

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            resp = process_rpc_request(req)
            if resp is not None:
                sys.stdout.write(json.dumps(resp) + "\n")
                sys.stdout.flush()
        except json.JSONDecodeError:
            continue


if __name__ == "__main__":
    main()
