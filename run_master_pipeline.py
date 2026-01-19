"""
Typhoid HDT v4.0: Unified Master Orchestrator
Executes the entire discovery-to-publication lifecycle in sequence.
"""

import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
SCRIPTS_DIR = BASE_DIR / 'scripts'

PHASES = [
    # 1. Verification & Baseline
    ("scripts/verify_geo_datasets.py", "Verifying authentic GEO datasets..."),
    
    # 2. Omics & Compound Mining
    ("scripts/run_pipeline_authentic.py", "Running v2.0 Authentic Pipeline..."),
    ("scripts/chembl_compound_mining.py", "Mining ChEMBL for SMILES-enabled ligands..."),
    
    # 3. v3.0 Network & Structural Layers
    ("scripts/v3_string_network.py", "Calculating Network Centrality Hubs..."),
    ("scripts/v3_structure_prep.py", "Fetching 3D Protein Structures..."),
    ("scripts/v3_virtual_screening.py", "Calculating Structural Fit Scores..."),
    
    # 4. v4.0 Mastery Layers
    ("scripts/v3_single_cell_analysis.py", "Integrating Single-Cell Specificity..."),
    ("scripts/v3_causal_inference.py", "Performing Causal De-risking (GWAS)..."),
    ("scripts/run_pipeline_v3.py", "Consolidating v3.0 Priority Scores..."),
    
    # 5. v4.0 Global Impact & AI
    ("scripts/v4_gnn_bioactivity.py", "Training PyTorch GNN Bioactivity Model..."),
    ("scripts/v4_pan_enteric_analysis.py", "Running Pan-Enteric Scaling..."),
    
    # 6. Publication Suite
    ("scripts/generate_figures_v3.py", "Generating Master Figures..."),
    ("scripts/generate_manuscript_v3.py", "Generating Final Manuscript..."),
    ("scripts/generate_v4_submission_package.py", "Generating World-Class Submission Package..."),
    # ("scripts/auto_deploy.py", "Deploying to Hugging Face & Kaggle (Requires Tokens)..."),
]

def run_phase(script_path, description):
    print(f"\n>>> {description}")
    path = BASE_DIR / script_path
    if not path.exists():
        print(f"!!! Error: {script_path} not found. Skipping...")
        return False
        
    try:
        result = subprocess.run([sys.executable, str(path)], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Phase Complete.")
            return True
        else:
            print(f"❌ Phase Failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Execution Error: {e}")
        return False

def main():
    print("="*80)
    print("TYPHOID HDT DISCOVERY SUITE v4.0: UNIFIED MASTER ORCHESTRATOR")
    print("="*80)
    print("Executing full discovery lifecycle (Phase 1 to 14)...")
    
    success_count = 0
    for script, desc in PHASES:
        if run_phase(script, desc):
            success_count += 1
            
    print("\n" + "="*80)
    print("ORCHESTRATION SUMMARY")
    print("="*80)
    print(f"Total Phases Executed: {len(PHASES)}")
    print(f"Successful: {success_count}")
    print(f"Failed: {len(PHASES) - success_count}")
    print("\nNext Steps:")
    print("1. Run 'streamlit run scripts/v4_dashboard_global.py' to explore results.")
    print("2. Review 'manuscripts/' for the final submission-ready paper.")
    print("3. Check 'docs/' for validation and clinical strategy protocols.")
    print("="*80)

if __name__ == "__main__":
    main()
