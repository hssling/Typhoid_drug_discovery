# Typhoid Host-Directed Therapy Drug Discovery Pipeline

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## 🌡️ Overview

An integrated multi-omics and chemoinformatics pipeline for identifying **host-directed therapy (HDT) targets** in typhoid fever. This addresses the **MDR/XDR Salmonella Typhi crisis** through resistance-bypassing host-targeted approaches.

### The MDR/XDR Crisis

| Resistance | Agents Affected | Impact |
|------------|-----------------|--------|
| MDR | Chloramphenicol, Ampicillin, TMP-SMX | First-line failure |
| FQ-Resistant | Ciprofloxacin, Ofloxacin | Second-line failure |
| **XDR** | + Ceftriaxone | Only azithromycin left |
| Azithro-R | Emerging | **Total treatment failure** |

> **Key Insight:** HDT targets the HOST macrophage response, completely bypassing bacterial resistance mechanisms!

### Global Burden

| Statistic | Value |
|-----------|-------|
| Annual cases | **14 million** |
| Annual deaths | 135,000 |
| India burden | **60% of global** |
| MDR prevalence | 50-70% |

---

## 🔬 Key Findings

### Top Prioritized Targets

| Rank | Target | Pathway | Score | Drug Candidate |
|------|--------|---------|-------|----------------|
| 1 | MTOR | Autophagy | 0.52 | Rapamycin |
| 2 | TNF | Cytokine | 0.49 | (Caution) |
| 3 | IL6 | Cytokine | 0.47 | Tocilizumab |
| 4 | IFNG | Macrophage | 0.45 | IFN-gamma |
| 5 | NLRP3 | Inflammasome | 0.42 | Colchicine |

### Priority Repurposing Candidates

| Drug | Target | Mechanism | Phase |
|------|--------|-----------|-------|
| **Rapamycin** | mTOR | Autophagy enhancer | FDA |
| **Metformin** | AMPK | Autophagy/metabolism | FDA |
| **Anakinra** | IL-1R | Inflammasome | FDA |
| **Deferasirox** | Iron | Nutrient deprivation | FDA |
| **IFN-gamma** | IFNGR | Macrophage activation | FDA |

---

## 📁 Project Structure

```
Typhoid_HDT_Pipeline/
├── config/typhoid_config.yaml
├── data/gene_signature.csv
├── outputs/
│   ├── figures/ (5 PNG files)
│   └── tables/ (2 CSV files)
├── manuscripts/
├── scripts/
├── tests/
├── .github/workflows/
├── README.md
└── LICENSE
```

## 🚀 Quick Start

```bash
git clone https://github.com/hssling/Typhoid_drug_discovery.git
cd Typhoid_drug_discovery
pip install -r requirements.txt
python scripts/run_pipeline.py
python scripts/generate_figures.py
```

## 👤 Author

**Dr. Siddalingaiah H S**  
Professor, Department of Community Medicine  
Shridevi Institute of Medical Sciences  
Tumkur, Karnataka, India  
Email: hssling@yahoo.com  
ORCID: 0000-0002-4771-8285

## 📄 License

MIT License
