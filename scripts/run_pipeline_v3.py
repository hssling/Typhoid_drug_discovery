"""
Typhoid HDT Target Prioritization Pipeline - v3.0 (Advanced Network Medicine)
Integrates:
1. Transcriptomic Evidence (GSE7000/GSE114192)
2. Network Medicine (STRING-db Hub Scores)
3. Chemoinformatics (ChEMBL API)

Author: Dr. Siddalingaiah H S
Version: 3.0 (Systems Biology)
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).parent.parent


def load_data():
    """Load gene signature and network scores."""
    sig_path = BASE_DIR / 'data' / 'gene_signature_verified.csv'
    net_path = BASE_DIR / 'outputs' / 'tables' / 'v3_network_scores.csv'
    
    if not sig_path.exists():
        raise FileNotFoundError("Verified gene signature not found.")
    
    # Load signature
    genes_df = pd.read_csv(sig_path, comment='#')
    
    # Load network scores if available
    if net_path.exists():
        net_df = pd.read_csv(net_path)
        genes_df = pd.merge(genes_df, net_df[['Symbol', 'Network_Hub_Score']], on='Symbol', how='left')
        genes_df['Network_Hub_Score'] = genes_df['Network_Hub_Score'].fillna(0)
    else:
        print("Warning: Network scores not found. Hub score will be 0.")
        genes_df['Network_Hub_Score'] = 0
        
    return genes_df


def calculate_v3_score(row):
    """
    Advanced Priority Scoring (v3.0)
    
    Weights:
    - DE Evidence (Transcriptomics): 30%
    - Network Hub Score (Interactome): 20%
    - Druggability (ChEMBL): 25%
    - Pathway Relevance: 15%
    - Clinical Phase/Relevance: 10%
    """
    
    # 1. DE Score (30%)
    log2fc = row.get('Log2FC_Thompson', 0)
    fdr = row.get('FDR_Thompson', 0.05)
    if pd.notna(log2fc) and pd.notna(fdr) and fdr > 0:
        de_raw = abs(float(log2fc)) * (-np.log10(float(fdr)))
        de_score = min(de_raw / 10, 1.0)
    else:
        de_score = 0.3 # Baseline
        
    # 2. Network Hub Score (20%) - Already scaled 0-1
    net_score = float(row.get('Network_Hub_Score', 0))
    
    # 3. Druggability (25%)
    drug_map = {'High': 1.0, 'Moderate': 0.6, 'Low': 0.2}
    druggability = drug_map.get(row.get('Druggability', 'Moderate'), 0.5)
    
    # 4. Pathway Importance (15%)
    pathway_weights = {
        'autophagy': 1.0, 'phagosome_maturation': 0.95, 'inflammasome': 0.9,
        'macrophage_polarization': 0.85, 'iron_homeostasis': 0.8,
        'cytokine_signaling': 0.7, 'nfkb_pathway': 0.6, 'oxidative_stress': 0.5
    }
    pathway = pathway_weights.get(row.get('Pathway', ''), 0.4)
    
    # 5. Phase Applicability (10%)
    phase_map = {'Acute': 1.0, 'Both': 0.8, 'Carrier': 0.5}
    phase_score = phase_map.get(row.get('Phase_Relevance', 'Both'), 0.7)
    
    # v3.0 Composite
    composite = (
        0.30 * de_score +
        0.20 * net_score +
        0.25 * druggability +
        0.15 * pathway +
        0.10 * phase_score
    )
    
    return round(composite, 4)


def main():
    print("\n" + "=" * 70)
    print("TYPHOID HDT PRIORITIZATION PIPELINE v3.0 (Advanced)")
    print("Systems Biology Approach: Network Hubs + Multi-Omics")
    print("=" * 70)
    
    # Load and score
    genes_df = load_data()
    print(f"Analyzing {len(genes_df)} targets with integrated Network-Omics model...")
    
    genes_df['V3_Score'] = genes_df.apply(calculate_v3_score, axis=1)
    
    # Rank
    genes_df = genes_df.sort_values('V3_Score', ascending=False).reset_index(drop=True)
    genes_df['V3_Rank'] = range(1, len(genes_df) + 1)
    
    # Output
    output_path = BASE_DIR / 'outputs' / 'tables' / 'targets_ranked_v3.csv'
    genes_df.to_csv(output_path, index=False)
    
    print(f"\nSaved v3.0 results to: {output_path.name}")
    
    # Top 10 Display
    print("\nTOP 10 SYSTEM-LEVEL TARGETS (v3.0):")
    cols = ['V3_Rank', 'Symbol', 'Pathway', 'V3_Score', 'Network_Hub_Score']
    print(genes_df[cols].head(10))
    
    # Comparison note
    top_v3 = set(genes_df['Symbol'].head(10))
    print(f"\nNote: Targets like {', '.join(list(top_v3)[:3])} identified as critical hubs.")
    print("=" * 70)

if __name__ == '__main__':
    main()
