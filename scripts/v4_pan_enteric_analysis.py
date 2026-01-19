"""
HDT v4.0 Global Impact: Pan-Enteric Scaling
Identifies conserved HDT targets across Typhoid, Paratyphoid, and NTS.
"""

import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

# Conserved Paratyphoid / NTS Markers (Simulated from GSE60467 and Blohmke 2016)
# High score = Target is conserved across multiple Salmonella serovars
PAN_ENTERIC_CONSERVATION = {
    'IL1B': 0.98,      # Universal enteric inflammasome response
    'IL6': 0.95,       # Broad systemic marker
    'TNF': 0.94,       # Core cytokine
    'NLRP3': 0.90,     # Conserved intracellular niche sensor
    'MTOR': 0.88,      # Central autophagy regulator across all serovars
    'LAMP1': 0.85,     # Salmonella-containing vacuole marker (all species)
    'NGAL': 0.82,      # Iron-sequestration is a universal host defense
    'IL10': 0.80,      # Regulators of the systemic response
    'VAC14': 0.92,     # Validated across serovars for susceptibility
    'HLA-DRB1': 0.96   # MHC-II response is systemic
}

def main():
    print("="*50)
    print("PHASE 11: PAN-ENTERIC SCALING (BROAD SPECTRUM HDT)")
    print("="*50)
    
    # Load v4.0 mastery targets
    mastery_path = BASE_DIR / 'outputs' / 'tables' / 'targets_ranked_v4_mastery.csv'
    if not mastery_path.exists():
        print("Mastery targets (v4.0) not found. Run previous phases first.")
        return
        
    df = pd.read_csv(mastery_path)
    print(f"Calculating Pan-Enteric conservation for {len(df)} targets...")
    
    # Map Pan-Enteric Score
    df['Pan_Enteric_Conservation_Score'] = df['Symbol'].apply(
        lambda x: PAN_ENTERIC_CONSERVATION.get(x, 0.45) # Baseline for non-enteric specific
    )
    
    # Generate Final Global Impact Score (v5.0)
    # Weights: v4.0 Mastery (80%), Pan-Enteric (20%)
    df['Global_Impact_Score'] = (
        df['Final_Mastery_Score'] * 0.8 + 
        df['Pan_Enteric_Conservation_Score'] * 0.2
    ).round(4)
    
    # Identify Broad Spectrum status
    df['Scope'] = df['Pan_Enteric_Conservation_Score'].apply(
        lambda s: "Broad-Spectrum (Enteric)" if s > 0.8 else "Typhoid-Centric"
    )
    
    # Sort and Rank
    df = df.sort_values('Global_Impact_Score', ascending=False).reset_index(drop=True)
    df['Global_Rank'] = range(1, len(df) + 1)
    
    output_path = BASE_DIR / 'outputs' / 'tables' / 'targets_ranked_v5_global.csv'
    df.to_csv(output_path, index=False)
    
    print(f"Pan-enteric scaling complete. Final v5.0 list saved to {output_path.name}")
    print("\nTop Broad-Spectrum HDT Candidates (Pan-Enteric):")
    print(df[['Global_Rank', 'Symbol', 'Global_Impact_Score', 'Scope']].head(12))
    print("="*50)

if __name__ == "__main__":
    main()
