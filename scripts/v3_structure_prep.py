"""
HDT v3.0: Structural Bioinformatics Layer
Automates protein structure acquisition from RCSB PDB and AlphaFold DB.
"""

import os
import requests
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
STRUCTURE_DIR = BASE_DIR / 'data' / 'structures'
STRUCTURE_DIR.mkdir(parents=True, exist_ok=True)

# Recommended PDB IDs for top targets (manually curated for quality/human)
TARGET_PDB_MAPPING = {
    'MTOR': '4IPH',
    'IL1B': '1ITB',
    'IL6': '1ALU',
    'TNF': '1TNF',
    'IFNg': '1HIG',
    'NLRP3': '7PZW'  # Human NLRP3 decamer (Cryo-EM)
}

def download_pdb(pdb_id):
    """Download a PDB file from RCSB."""
    print(f"Downloading PDB: {pdb_id}...")
    url = f"https://files.rcsb.org/download/{pdb_id}.pdb"
    output_path = STRUCTURE_DIR / f"{pdb_id}.pdb"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(output_path, 'wb') as f:
            f.write(response.content)
        print(f"Saved to {output_path.name}")
        return output_path
    except Exception as e:
        print(f"Error downloading {pdb_id}: {e}")
        return None

def download_alphafold(af_id):
    """Download an AlphaFold structure (PDB format)."""
    print(f"Downloading AlphaFold: {af_id}...")
    # URL format: https://alphafold.ebi.ac.uk/files/AF-Q96P20-F1-model_v4.pdb
    url = f"https://alphafold.ebi.ac.uk/files/{af_id}-model_v4.pdb"
    output_path = STRUCTURE_DIR / f"{af_id}.pdb"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(output_path, 'wb') as f:
            f.write(response.content)
        print(f"Saved to {output_path.name}")
        return output_path
    except Exception as e:
        print(f"Error downloading {af_id}: {e}")
        return None

def main():
    print("="*50)
    print("PHASE 2: STRUCTURAL BIOINFORMATICS (STRUCTURE ACQUISITION)")
    print("="*50)
    
    # Load v3.0 ranked targets to identify top hits
    ranked_path = BASE_DIR / 'outputs' / 'tables' / 'targets_ranked_v3.csv'
    if not ranked_path.exists():
        print("Ranked targets (v3.0) not found. Run run_pipeline_v3.py first.")
        return
        
    targets_df = pd.read_csv(ranked_path)
    top_targets = targets_df['Symbol'].head(6).tolist()
    
    log_data = []
    
    for gene in top_targets:
        struct_id = TARGET_PDB_MAPPING.get(gene)
        if not struct_id:
            print(f"No predefined structure mapping for {gene}. Skipping...")
            continue
            
        if struct_id.startswith('AF-'):
            path = download_alphafold(struct_id)
            source = 'AlphaFold'
        else:
            path = download_pdb(struct_id)
            source = 'RCSB_PDB'
            
        if path:
            log_data.append({
                'Gene': gene,
                'Structure_ID': struct_id,
                'Source': source,
                'File_Path': str(path.relative_to(BASE_DIR))
            })
            
    # Save acquisition log
    log_df = pd.DataFrame(log_data)
    log_path = STRUCTURE_DIR / 'structure_log.csv'
    log_df.to_csv(log_path, index=False)
    
    print("\n" + "="*50)
    print(f"Acquisition complete. {len(log_df)} structures saved to {STRUCTURE_DIR.name}/")
    print(f"Log saved to {log_path.name}")
    print("="*50)

if __name__ == "__main__":
    main()
