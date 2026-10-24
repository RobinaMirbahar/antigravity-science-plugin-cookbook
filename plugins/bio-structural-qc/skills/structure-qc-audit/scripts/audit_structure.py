#!/usr/bin/env python3
"""Audits PDB and mmCIF coordinate files for chain completeness and B-factor/pLDDT distribution."""

# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///

import argparse
import json
from pathlib import Path
import statistics


def parse_ca_bfactors(filepath: Path) -> dict:
    """Extracts C-alpha (CA) residue numbers and B-factor/pLDDT values per chain."""
    chains: dict[str, list[tuple[int, float]]] = {}
    ext = filepath.suffix.lower()

    with filepath.open("r", encoding="utf-8", errors="replace") as f:
        for line in f:
            if ext == ".pdb" and line.startswith("ATOM  "):
                atom_name = line[12:16].strip()
                if atom_name != "CA":
                    continue
                chain_id = line[21].strip() or "A"
                try:
                    res_seq = int(line[22:26].strip())
                    b_factor = float(line[60:66].strip())
                except ValueError:
                    continue
                chains.setdefault(chain_id, []).append((res_seq, b_factor))

            elif ext in {".cif", ".mmcif"} and line.startswith("ATOM "):
                parts = line.split()
                if len(parts) >= 15 and parts[3] == "CA":
                    chain_id = parts[6]
                    try:
                        res_seq = int(parts[8])
                        b_factor = float(parts[14])
                    except ValueError:
                        continue
                    chains.setdefault(chain_id, []).append((res_seq, b_factor))

    return chains


def audit_file(filepath: Path) -> dict:
    chains = parse_ca_bfactors(filepath)
    if not chains:
        return {"file": str(filepath), "status": "ERROR", "reason": "No CA atoms found"}

    chain_reports = {}
    all_scores: list[float] = []

    for chain_id, residues in sorted(chains.items()):
        scores = [b for _, b in residues]
        all_scores.extend(scores)
        low_conf = [res for res, b in residues if b < 50.0]
        high_conf = [res for res, b in residues if b >= 70.0]

        chain_reports[chain_id] = {
            "residue_count": len(residues),
            "mean_score": round(statistics.fmean(scores), 2),
            "median_score": round(statistics.median(scores), 2),
            "pct_high_confidence_ge_70": round(100.0 * len(high_conf) / len(residues), 1),
            "pct_low_confidence_lt_50": round(100.0 * len(low_conf) / len(residues), 1),
            "high_confidence_span": [min(high_conf), max(high_conf)] if high_conf else None,
        }

    overall_low_pct = round(
        100.0 * sum(1 for s in all_scores if s < 50.0) / len(all_scores), 1
    )
    return {
        "file": filepath.name,
        "status": "WARN_HIGH_DISORDER" if overall_low_pct > 30.0 else "PASS",
        "total_ca_residues": len(all_scores),
        "overall_mean_score": round(statistics.fmean(all_scores), 2),
        "overall_pct_low_lt_50": overall_low_pct,
        "chains": chain_reports,
    }


def main():
    parser = argparse.ArgumentParser(description="Audit PDB/mmCIF structure confidence.")
    parser.add_argument("files", nargs="+", type=Path, help="Paths to .pdb or .cif files")
    parser.add_argument("-o", "--output", type=Path, help="Optional JSON output file path")
    args = parser.parse_args()

    results = [audit_file(p) for p in args.files]
    payload = json.dumps(results, indent=2)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
        print(f"[*] Saved QC report to {args.output}")
    else:
        print(payload)


if __name__ == "__main__":
    main()
