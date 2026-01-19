"""
ChEMBL Compound Mining Script
Queries ChEMBL API for compounds targeting HDT genes.

Author: Dr. Siddalingaiah H S
"""

import pandas as pd
import time
from pathlib import Path

# Check if chembl client is installed
try:
    from chembl_webresource_client.new_client import new_client
    CHEMBL_AVAILABLE = True
except ImportError:
    CHEMBL_AVAILABLE = False
    print("WARNING: chembl_webresource_client not installed.")
    print("Install with: pip install chembl_webresource_client")

BASE_DIR = Path(__file__).parent.parent


def query_target_by_gene(gene_symbol: str) -> dict:
    """
    Query ChEMBL for a human protein target by gene symbol.
    
    Returns:
        dict with target_chembl_id and metadata, or None
    """
    if not CHEMBL_AVAILABLE:
        return None
    
    target = new_client.target
    
    try:
        results = target.filter(
            target_synonym__iexact=gene_symbol,
            target_type='SINGLE PROTEIN',
            organism='Homo sapiens'
        ).only(['target_chembl_id', 'pref_name', 'target_type'])
        
        results_list = list(results)
        
        if results_list:
            return results_list[0]
        
        # Try alternative search by target synonyms
        results = target.filter(
            target_synonym__icontains=gene_symbol,
            target_type='SINGLE PROTEIN',
            organism='Homo sapiens'
        ).only(['target_chembl_id', 'pref_name', 'target_type'])
        
        results_list = list(results)
        return results_list[0] if results_list else None
        
    except Exception as e:
        print(f"  Error querying {gene_symbol}: {e}")
        return None


def query_activities_for_target(target_chembl_id: str, min_pchembl: float = 6.0) -> list:
    """
    Query ChEMBL for bioactivity data for a target.
    
    Args:
        target_chembl_id: ChEMBL target ID (e.g., 'CHEMBL203')
        min_pchembl: Minimum pChEMBL value (default 6.0 = 1 μM)
    
    Returns:
        List of activity records with compound info
    """
    if not CHEMBL_AVAILABLE:
        return []
    
    activity = new_client.activity
    
    try:
        results = activity.filter(
            target_chembl_id=target_chembl_id,
            pchembl_value__gte=min_pchembl,
            assay_type__in=['B', 'F']  # Binding and Functional assays
        ).only([
            'molecule_chembl_id',
            'molecule_pref_name',
            'pchembl_value',
            'standard_type',
            'standard_value',
            'standard_units',
        ])
        
        return list(results)[:100]  # Limit to top 100
        
    except Exception as e:
        print(f"  Error querying activities: {e}")
        return []


def get_molecule_info(molecule_chembl_id: str) -> dict:
    """Get detailed molecule info including clinical phase."""
    if not CHEMBL_AVAILABLE:
        return {}
    
    molecule = new_client.molecule
    
    try:
        result = molecule.filter(
            molecule_chembl_id=molecule_chembl_id
        ).only([
            'molecule_chembl_id',
            'pref_name',
            'max_phase',
            'molecule_type',
            'first_approval',
        ])
        
        results_list = list(result)
        return results_list[0] if results_list else {}
        
    except Exception as e:
        return {}


def mine_compounds_for_gene_list(gene_list: list, output_path: Path = None):
    """
    Mine ChEMBL for compounds targeting a list of genes.
    
    Args:
        gene_list: List of gene symbols
        output_path: Path to save results CSV
    
    Returns:
        DataFrame with compound bioactivity data
    """
    if not CHEMBL_AVAILABLE:
        print("ERROR: ChEMBL client not available. Cannot mine compounds.")
        return pd.DataFrame()
    
    print("=" * 70)
    print("CHEMBL COMPOUND MINING")
    print("=" * 70)
    
    all_compounds = []
    
    for i, gene in enumerate(gene_list):
        print(f"\n[{i+1}/{len(gene_list)}] Processing {gene}...")
        
        # Find target
        target_info = query_target_by_gene(gene)
        
        if not target_info:
            print(f"  No ChEMBL target found for {gene}")
            continue
        
        target_id = target_info['target_chembl_id']
        print(f"  Found target: {target_id} ({target_info.get('pref_name', 'N/A')})")
        
        # Query activities
        activities = query_activities_for_target(target_id)
        print(f"  Found {len(activities)} activities with pChEMBL >= 6.0")
        
        # Process unique compounds
        seen_molecules = set()
        for act in activities:
            mol_id = act.get('molecule_chembl_id')
            if mol_id and mol_id not in seen_molecules:
                seen_molecules.add(mol_id)
                
                # Get molecule details
                mol_info = get_molecule_info(mol_id)
                
                compound_entry = {
                    'Gene': gene,
                    'Target_ChEMBL_ID': target_id,
                    'Target_Name': target_info.get('pref_name', ''),
                    'Molecule_ChEMBL_ID': mol_id,
                    'Drug_Name': act.get('molecule_pref_name') or mol_info.get('pref_name', ''),
                    'pChEMBL': act.get('pchembl_value'),
                    'Assay_Type': act.get('standard_type', ''),
                    'Max_Phase': mol_info.get('max_phase', 0),
                    'First_Approval': mol_info.get('first_approval'),
                    'Source': 'ChEMBL_API',
                }
                all_compounds.append(compound_entry)
        
        # Rate limiting
        time.sleep(0.5)
    
    # Create DataFrame
    df = pd.DataFrame(all_compounds)
    
    if len(df) > 0:
        # Sort by pChEMBL
        df = df.sort_values('pChEMBL', ascending=False)
        
        # Summary
        print("\n" + "=" * 70)
        print("SUMMARY")
        print("=" * 70)
        print(f"Total compounds found: {len(df)}")
        print(f"Unique drugs: {df['Drug_Name'].nunique()}")
        print(f"FDA approved (Phase 4): {len(df[df['Max_Phase'] == 4])}")
        print(f"Phase 3: {len(df[df['Max_Phase'] == 3])}")
        print(f"Phase 2: {len(df[df['Max_Phase'] == 2])}")
        
        if output_path:
            df.to_csv(output_path, index=False)
            print(f"\nSaved to: {output_path}")
    
    return df


def main():
    """Main entry point for compound mining."""
    
    # Load prioritized targets
    gene_sig_path = BASE_DIR / 'outputs' / 'tables' / 'targets_ranked_authentic.csv'
    
    if not gene_sig_path.exists():
        # Fall back to verified signature if ranked not yet created
        gene_sig_path = BASE_DIR / 'data' / 'gene_signature_verified.csv'
        genes_df = pd.read_csv(gene_sig_path, comment='#')
    else:
        genes_df = pd.read_csv(gene_sig_path)
    
    # Get top 5 druggable targets for compound mining
    if 'Druggability' in genes_df.columns:
        high_drug = genes_df[genes_df['Druggability'].isin(['High', 'Moderate'])]
        gene_list = high_drug['Symbol'].head(5).tolist()
    else:
        gene_list = genes_df['Symbol'].head(5).tolist()
    
    print(f"Mining compounds for {len(gene_list)} genes: {gene_list}")
    
    output_path = BASE_DIR / 'outputs' / 'tables' / 'compounds_from_chembl.csv'
    
    compounds_df = mine_compounds_for_gene_list(gene_list, output_path)
    
    return compounds_df


if __name__ == '__main__':
    main()
