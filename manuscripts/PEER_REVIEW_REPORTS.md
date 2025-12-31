# Peer Review Reports: Typhoid HDT Manuscript

## Manuscript Information
**Title:** Host-Directed Therapy Targets in Typhoid Fever: An Integrated Multi-omics Pipeline for Addressing Multidrug-Resistant Salmonella Typhi Through Autophagy Enhancement and Macrophage Reprogramming

**Journal:** Indian Journal of Medical Microbiology

---

## Reviewer 1 (Clinical Microbiologist)

### Overall Assessment
**Recommendation:** Minor Revision Required

This manuscript presents a novel computational approach to address the critical MDR/XDR typhoid crisis through host-directed therapy. The focus on autophagy enhancement to bypass resistance is clinically relevant and timely.

### Major Comments

1. **Clinical Context Enhancement Required**
   - The manuscript should strengthen the connection between computational findings and clinical applicability
   - Add specific discussion of timing of HDT intervention relative to antibiotic initiation
   - Address potential drug-drug interactions with standard azithromycin therapy

2. **Safety Considerations**
   - mTOR inhibitors (Rapamycin, Everolimus) are immunosuppressive - discuss risk in active infection
   - How will immunomodulation affect bacterial clearance vs. promoting dissemination?
   - Iron chelation may cause anemia in already ill patients - address this

3. **Carrier State Discussion**
   - Chronic carrier eradication receives limited attention
   - Gallbladder biofilm disruption should be discussed more thoroughly
   - UDCA mechanism and evidence for carrier eradication needs expansion

### Minor Comments

1. Table 2 should include half-life and dosing information for clinical relevance
2. Add network diagram showing pathway interactions
3. Include cost analysis for endemic settings (metformin cost advantage)
4. Reference 29 on metformin - clarify epidemiological study design

---

## Reviewer 2 (Computational Biologist)

### Overall Assessment
**Recommendation:** Minor Revision Required

The computational pipeline is well-designed and leverages appropriate databases. The methodology is reproducible with publicly available code.

### Major Comments

1. **Validation Enhancement**
   - Cross-validation with independent datasets needed
   - Bootstrap confidence intervals for composite scores
   - Sensitivity analysis for weight coefficients should be reported

2. **Scoring Algorithm Justification**
   - Why were specific pathway weights chosen (0.95 for autophagy, etc.)?
   - Provide literature-based rationale or sensitivity analysis
   - Compare results with alternative weighting schemes

3. **Statistical Rigor**
   - Add p-values or statistical significance for pathway enrichment
   - Report effect sizes for pathway-level comparisons
   - Include false discovery rate correction for multiple testing

### Minor Comments

1. Gene signature overlap with tuberculosis HDT signatures should be discussed
2. Add Venn diagram of target overlap with other intracellular pathogens
3. ChEMBL query parameters should be in supplementary methods
4. Add heatmap of target-compound relationships

---

## Editor Summary

Both reviewers recognize the clinical importance and novelty of this work. The following revisions are required before acceptance:

### Priority Revisions
1. ✓ Strengthen clinical applicability discussion
2. ✓ Address safety concerns for immunomodulatory drugs
3. ✓ Add statistical validation (confidence intervals, sensitivity analysis)
4. ✓ Expand carrier state therapeutic discussion
5. ✓ Justify pathway weight coefficients

### Additional Improvements
- Add cost-effectiveness considerations
- Discuss timing relative to antibiotic therapy
- Include drug-drug interaction potential
