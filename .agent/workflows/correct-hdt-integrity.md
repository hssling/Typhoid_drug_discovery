---
description: Restore scientific integrity to HDT discovery pipelines by replacing fabricated data with authentic analysis.
---

# Workflow: HDT Project Scientific Integrity Restoration

Use this workflow when auditing or rebuilding a Host-Directed Therapy (HDT) target discovery project that may contain fabricated data, misattributed sources, or hardcoded results.

## Phase 1: Scientific Integrity Audit 🔍

1.  **Verify GEO Accessions**: 
    - Search NCBI Gene Expression Omnibus for every GSE ID cited in the config or manuscript.
    - Check if the description, organism, and sample count match the project's claims.
2.  **Verify Compound Bioactivity**:
    - cross-check any hardcoded compound list against the ChEMBL web interface.
    - Check if the project claims to use an API but actually has hardcoded dictionaries in the script.
3.  **Audit Deliverables**:
    - Inspect the `manuscripts/` directory for simulated peer review reports or revision responses (often a red flag).

## Phase 2: Data Foundation Restoration 🧬

1.  **Identify Verified Datasets**: 
    - Use the `verify_geo_datasets.py` script (or equivalent) to create a `verified_datasets.json` provenance file.
2.  **Select Implementation Depth**:
    - **Full**: Perform new differential expression analysis in R/Bioconductor (limma/DESeq2).
    - **Simplified**: Use published gene lists (DEGs) from verified high-impact peer-reviewed studies (citing PMIDs).
3.  **Update Configuration**:
    - Remove all non-existent or misattributed GEO IDs from `typhoid_config.yaml` or equivalent.

## Phase 3: Authentic Tooling Integration 🛠️

1.  **ChEMBL API Integration**:
    - Install `chembl_webresource_client`.
    - Implement a mining script that queries ChEMBL by target gene symbol and retrieves real `pChEMBL` and `Max_Phase` data.
2.  **Transparent Scouring Algorithm (v2.0)**:
    - Implement a prioritization function with **documented weights**.
    - **Standard Weights**: DE Evidence (40%), Druggability (30%), Pathway Relevance (20%), Clinical Phase (10%).
    - Avoid arbitrary bonuses; use stats-based scoring (e.g., $|logFC| \times -log10(FDR)$).

## Phase 4: Deliverable Regeneration & Purge 📄

1.  **Regenerate Figures**: Update `generate_figures.py` to pull data from the new authentic CSV outputs.
2.  **Enhanced Manuscript**: 
    - Refactor `generate_manuscript.py` to describe the actual methodology (NCBI/ChEMBL verification).
    - Update all tables and result text with real counts and scores.
3.  **The Purge**: 
    - Delete all `.md` files containing simulated peer reviews or fictional revision responses.
    - Remove legacy CSV files containing fabricated target lists.

## Phase 5: Verification & Commit ✅

1.  **Automated Check**: Run the pipeline and ensure `outputs/` are generated from API calls.
2.  **Git Commit**: Use a clear commit message: `[RESTORED INTEGRITY] Rebuilt pipeline with verified data and real API integration. Removed fabricated content.`
3.  **Push**: Ensure remote synchronization if applicable.
