# 🧪 Phase 12: In Vitro Validation Protocol (v4.0)

This protocol serves as the "Gold Standard" validation bridge for the Typhoid HDT Discovery Suite. It is designed for execution in a **BSL-3 Biosafety Laboratory**.

## 1. Experimental Objectives
To determine if AI-prioritized host-directed candidates (Top Hits: `IL1B`, `TNF`, `IL6`, `NLRP3`, `MTOR` inhibitors) significantly reduce the intracellular replication of *Salmonella Typhi* in human macrophages.

## 2. Model Systems
- **Cell Line**: Human THP-1 monocytes (differentiated into macrophages using 50nM PMA for 48 hours).
- **Bacterial Strain**: *S. Typhi* Ty2 (Wild-type) or Quailes strain.
- **Reference HDT**: Dexamethasone (Positive control for inflammation dampening) or Metformin (Positive control for Autophagy activation).

## 3. The Gentamicin Protection Assay (Workflow)
1. **Cell Seeding**: Seed THP-1 macrophages in 24-well plates (5x10^5 cells/well).
2. **HDT Pre-Treatment**: Treat cells with prioritized compounds (e.g., Anakinra for IL1B, Infliximab for TNF, or Metformin for MTOR) at 3 concentrations (e.g., 1µM, 10µM, 50µM) for 2 hours.
3. **Infection**: Infect macrophages with *S. Typhi* at an MOI (Multiplicity of Infection) of 10:1.
4. **Internalization**: Incubate for 1 hour at 37°C / 5% CO2. 
5. **Gentamicin Kill**: Wash 3x with PBS; add media containing **100µg/mL Gentamicin** for 1 hour to kill extracellular bacteria.
6. **Maintenance & HDT Incubation**: Replace media with low-dose Gentamicin (10µg/mL) and maintain HDT treatment for 2h, 6h, and 24h post-infection.
7. **Lysis & CFU Counting**:
    - Lyse cells using 0.1% Triton X-100.
    - Perform serial dilutions and plate on LB Agar.
    - Incubate at 37°C for 24 hours.
    - **Outcome Metric**: Colony Forming Units (CFU) per mL.

## 4. Secondary Validations
- **Inflammatory Profiling**: Measure supernatant IL-1β, TNF, and IL-6 via ELISA.
- **Cytotoxicity (MTT/LDH)**: Ensure the drug concentration does not reduce macrophage viability by >10%.
- **Autophagy Visuals**: Use LC3-II/p62 Western Blotting for MTOR-pathway candidates.

---
> [!IMPORTANT]
> **Scrutiny Note**: This protocol addresses the primary mechanism of Typhoid persistence (intracellular replication in macrophages). Success in this assay is a prerequisite for pre-clinical animal models.
