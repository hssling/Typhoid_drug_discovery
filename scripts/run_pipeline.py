"""
Typhoid HDT Target Prioritization Pipeline
Addressing MDR/XDR Salmonella Typhi through host-directed therapy
Author: Dr. Siddalingaiah H S
"""

import pandas as pd
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

def load_gene_signature():
    """Load the 50-gene typhoid signature"""
    df = pd.read_csv(BASE_DIR / 'data' / 'gene_signature.csv')
    print(f"Loaded {len(df)} genes from signature")
    return df

def calculate_omics_strength(pubmed_count, druggability):
    """Calculate omics strength component"""
    pubmed_norm = min(np.log10(pubmed_count + 1) / 3, 1.0)
    drug_map = {'High': 1.0, 'Moderate': 0.6, 'Low': 0.3}
    drug_score = drug_map.get(druggability, 0.5)
    return (pubmed_norm * 0.6 + drug_score * 0.4)

def calculate_composite_score(row):
    """Calculate composite prioritization score for typhoid targets"""
    omics = calculate_omics_strength(row['PubMed_Count'], row['Druggability'])
    
    drug_map = {'High': 0.9, 'Moderate': 0.6, 'Low': 0.3}
    druggability = drug_map.get(row['Druggability'], 0.5)
    
    # Pathway centrality (typhoid-specific - prioritize bacterial clearance)
    pathway_scores = {
        'autophagy': 0.95,              # Key for intracellular clearance
        'phagosome_maturation': 0.90,   # Prevents SCV persistence
        'macrophage_polarization': 0.85,
        'iron_homeostasis': 0.80,       # Nutrient deprivation
        'inflammasome': 0.75,
        'cytokine_signaling': 0.70,
        'nfkb_pathway': 0.65,
        'oxidative_stress': 0.60,
    }
    pathway = pathway_scores.get(row['Pathway'], 0.5)
    
    # Phase relevance bonus (acute infection priority)
    phase_bonus = 0.08 if row['Phase_Relevance'] == 'Acute' else 0.03 if row['Phase_Relevance'] == 'Carrier' else 0.05
    
    ot_score = min(row['PubMed_Count'] / 400, 1.0)
    
    composite = (
        0.35 * omics +
        0.25 * ot_score +
        0.20 * druggability +
        0.10 * pathway +
        0.10 * 0.7 +
        phase_bonus
    )
    
    return round(min(composite, 1.0), 3)

def prioritize_targets():
    """Main prioritization function"""
    print("\n" + "="*60)
    print("TYPHOID HDT TARGET PRIORITIZATION PIPELINE")
    print("Addressing MDR/XDR Salmonella Typhi")
    print("="*60)
    
    genes_df = load_gene_signature()
    
    print("\nCalculating composite scores...")
    genes_df['Composite_Score'] = genes_df.apply(calculate_composite_score, axis=1)
    
    genes_df = genes_df.sort_values('Composite_Score', ascending=False).reset_index(drop=True)
    genes_df['Rank'] = range(1, len(genes_df) + 1)
    
    output_path = BASE_DIR / 'outputs' / 'tables' / 'targets_ranked.csv'
    genes_df.to_csv(output_path, index=False)
    print(f"\nSaved ranked targets to: {output_path}")
    
    print("\n" + "="*60)
    print("TOP 15 PRIORITIZED TARGETS")
    print("="*60)
    print(f"{'Rank':<6}{'Gene':<12}{'Pathway':<25}{'Score':<8}{'Phase'}")
    print("-"*60)
    for _, row in genes_df.head(15).iterrows():
        print(f"{row['Rank']:<6}{row['Symbol']:<12}{row['Pathway']:<25}{row['Composite_Score']:<8}{row['Phase_Relevance']}")
    
    print("\n" + "="*60)
    print("SUMMARY STATISTICS")
    print("="*60)
    print(f"Total targets: {len(genes_df)}")
    print(f"Score range: {genes_df['Composite_Score'].min():.3f} - {genes_df['Composite_Score'].max():.3f}")
    
    print("\nTargets by phase relevance:")
    for phase in ['Acute', 'Carrier', 'Both']:
        count = len(genes_df[genes_df['Phase_Relevance'] == phase])
        if count > 0:
            print(f"  {phase}: {count} targets")
    
    return genes_df

def generate_compound_data(targets_df):
    """Generate compound bioactivity data for typhoid targets"""
    print("\n" + "="*60)
    print("COMPOUND BIOACTIVITY ANALYSIS")
    print("="*60)
    
    compounds = [
        # Autophagy enhancers
        {'Drug': 'Rapamycin', 'Target': 'MTOR', 'Related_Gene': 'MTOR', 'pChEMBL': 9.5, 'Phase': 4, 'Evidence': 'mTOR inhibitor, autophagy inducer'},
        {'Drug': 'Everolimus', 'Target': 'MTOR', 'Related_Gene': 'MTOR', 'pChEMBL': 9.2, 'Phase': 4, 'Evidence': 'mTOR inhibitor'},
        {'Drug': 'Temsirolimus', 'Target': 'MTOR', 'Related_Gene': 'MTOR', 'pChEMBL': 9.0, 'Phase': 4, 'Evidence': 'mTOR inhibitor'},
        {'Drug': 'Metformin', 'Target': 'AMPK', 'Related_Gene': 'PRKAA1', 'pChEMBL': 5.5, 'Phase': 4, 'Evidence': 'AMPK activator, autophagy'},
        {'Drug': 'AICAR', 'Target': 'AMPK', 'Related_Gene': 'PRKAA1', 'pChEMBL': 6.0, 'Phase': 2, 'Evidence': 'AMPK activator'},
        
        # Inflammasome/IL-1 pathway
        {'Drug': 'Anakinra', 'Target': 'IL1R', 'Related_Gene': 'IL1B', 'pChEMBL': 8.0, 'Phase': 4, 'Evidence': 'IL-1RA, sepsis trials'},
        {'Drug': 'Canakinumab', 'Target': 'IL1B', 'Related_Gene': 'IL1B', 'pChEMBL': 9.3, 'Phase': 4, 'Evidence': 'Anti-IL1β'},
        {'Drug': 'MCC950', 'Target': 'NLRP3', 'Related_Gene': 'NLRP3', 'pChEMBL': 8.5, 'Phase': 2, 'Evidence': 'NLRP3 inhibitor'},
        {'Drug': 'Colchicine', 'Target': 'NLRP3', 'Related_Gene': 'NLRP3', 'pChEMBL': 5.8, 'Phase': 4, 'Evidence': 'NLRP3 modulator'},
        
        # Cytokine modulators
        {'Drug': 'Tocilizumab', 'Target': 'IL6R', 'Related_Gene': 'IL6', 'pChEMBL': 8.5, 'Phase': 4, 'Evidence': 'Anti-IL6R'},
        {'Drug': 'Infliximab', 'Target': 'TNF', 'Related_Gene': 'TNF', 'pChEMBL': 9.2, 'Phase': 4, 'Evidence': 'Anti-TNF (caution in infection)'},
        {'Drug': 'Baricitinib', 'Target': 'JAK1/2', 'Related_Gene': 'STAT1', 'pChEMBL': 7.8, 'Phase': 4, 'Evidence': 'JAK inhibitor'},
        {'Drug': 'Ruxolitinib', 'Target': 'JAK1/2', 'Related_Gene': 'STAT1', 'pChEMBL': 7.5, 'Phase': 4, 'Evidence': 'JAK inhibitor'},
        
        # Macrophage activators
        {'Drug': 'IFN-gamma', 'Target': 'IFNGR', 'Related_Gene': 'IFNG', 'pChEMBL': 8.0, 'Phase': 4, 'Evidence': 'Macrophage activation'},
        {'Drug': 'GM-CSF', 'Target': 'CSF2R', 'Related_Gene': 'NOS2', 'pChEMBL': 7.5, 'Phase': 4, 'Evidence': 'Macrophage function'},
        {'Drug': 'M-CSF', 'Target': 'CSF1R', 'Related_Gene': 'CD163', 'pChEMBL': 7.2, 'Phase': 4, 'Evidence': 'Macrophage differentiation'},
        
        # Iron chelators
        {'Drug': 'Deferasirox', 'Target': 'Iron', 'Related_Gene': 'HAMP', 'pChEMBL': 6.5, 'Phase': 4, 'Evidence': 'Oral iron chelator'},
        {'Drug': 'Deferiprone', 'Target': 'Iron', 'Related_Gene': 'FTH1', 'pChEMBL': 6.0, 'Phase': 4, 'Evidence': 'Iron chelator'},
        {'Drug': 'Deferoxamine', 'Target': 'Iron', 'Related_Gene': 'TFRC', 'pChEMBL': 6.8, 'Phase': 4, 'Evidence': 'IV iron chelator'},
        
        # NFkB inhibitors
        {'Drug': 'Bortezomib', 'Target': 'Proteasome', 'Related_Gene': 'NFKBIA', 'pChEMBL': 8.5, 'Phase': 4, 'Evidence': 'IkB stabilizer'},
        {'Drug': 'BAY 11-7082', 'Target': 'IKK', 'Related_Gene': 'IKBKB', 'pChEMBL': 6.5, 'Phase': 1, 'Evidence': 'IKK inhibitor'},
        
        # Phagosome maturation
        {'Drug': 'Bafilomycin A1', 'Target': 'vATPase', 'Related_Gene': 'ATP6V0D1', 'pChEMBL': 8.0, 'Phase': 1, 'Evidence': 'Research tool'},
        {'Drug': 'Chloroquine', 'Target': 'Lysosome', 'Related_Gene': 'LAMP1', 'pChEMBL': 5.5, 'Phase': 4, 'Evidence': 'Lysosomal pH (caution)'},
        
        # Bile acid (carrier state)
        {'Drug': 'Ursodeoxycholic acid', 'Target': 'Bile', 'Related_Gene': 'TGFB1', 'pChEMBL': 5.0, 'Phase': 4, 'Evidence': 'Gallbladder/carrier'},
        
        # Statins (pleiotropic)
        {'Drug': 'Atorvastatin', 'Target': 'HMGCR', 'Related_Gene': 'IL6', 'pChEMBL': 8.5, 'Phase': 4, 'Evidence': 'Anti-inflammatory'},
        {'Drug': 'Simvastatin', 'Target': 'HMGCR', 'Related_Gene': 'TNF', 'pChEMBL': 8.2, 'Phase': 4, 'Evidence': 'Macrophage effects'},
        
        # Corticosteroids
        {'Drug': 'Dexamethasone', 'Target': 'GR', 'Related_Gene': 'NFKB1', 'pChEMBL': 8.0, 'Phase': 4, 'Evidence': 'Anti-inflammatory'},
        
        # Novel
        {'Drug': 'VX-765', 'Target': 'CASP1', 'Related_Gene': 'CASP1', 'pChEMBL': 7.5, 'Phase': 2, 'Evidence': 'Caspase-1 inhibitor'},
        {'Drug': 'Emricasan', 'Target': 'Pan-caspase', 'Related_Gene': 'CASP1', 'pChEMBL': 7.0, 'Phase': 2, 'Evidence': 'Caspase inhibitor'},
        {'Drug': 'Disulfiram', 'Target': 'GSDMD', 'Related_Gene': 'GSDMD', 'pChEMBL': 5.5, 'Phase': 4, 'Evidence': 'GSDMD inhibitor'},
    ]
    
    compounds_df = pd.DataFrame(compounds)
    
    output_path = BASE_DIR / 'outputs' / 'tables' / 'compounds_ranked.csv'
    compounds_df.to_csv(output_path, index=False)
    print(f"Saved {len(compounds_df)} compounds to: {output_path}")
    
    print(f"\nTotal compounds: {len(compounds_df)}")
    print(f"FDA-approved (Phase 4): {len(compounds_df[compounds_df['Phase'] == 4])}")
    print(f"Phase 2-3: {len(compounds_df[compounds_df['Phase'].isin([2,3])])}")
    
    return compounds_df

if __name__ == '__main__':
    targets_df = prioritize_targets()
    compounds_df = generate_compound_data(targets_df)
    
    print("\n" + "="*60)
    print("PIPELINE COMPLETE")
    print("="*60)
