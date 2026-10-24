# Epigraphy Markup & Scholarly Citation Integrity Rules

1. **Pre-Flight Epigraphy Markup Gate**: Before submitting any damaged Latin or Ancient Greek inscription to `predictingthepast` (`Aeneas` or `Ithaca`), run `epigraphy-gap-validator` to verify that:
   - Total cleaned length is at least **25 characters** (padded with `-` if shorter).
   - No forbidden adjacent gap tokens (`##`, `?#`, or `#?`) appear in the string.
2. **No Hallucinated DOIs**: Every scholarly citation or preprint reference must be verified via `literature-search-openalex`, `literature-search-europepmc`, or `pubmed-database`.
