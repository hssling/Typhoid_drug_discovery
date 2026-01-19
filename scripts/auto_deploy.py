"""
Typhoid HDT v4.1: Automated Global Deployment
Automates Hugging Face Spaces creation and Kaggle Dataset upload.
"""

import os
import subprocess
import sys
import shutil
import json
from pathlib import Path
from huggingface_hub import HfApi, create_repo, upload_folder

BASE_DIR = Path(__file__).parent.parent

def deploy_hf():
    token = os.getenv("HF_TOKEN")
    if not token:
        print("❌ HF_TOKEN not found in environment variables.")
        return False
        
    print("🚀 Deploying to Hugging Face Spaces...")
    api = HfApi()
    repo_id = "hssling/typhoid_drug_discovery_model"
    
    try:
        # Check if repo exists
        try:
            api.repo_info(repo_id=repo_id, repo_type="space", token=token)
            print(f"  Repo {repo_id} already exists. Skipping creation.")
        except:
            print(f"  Creating repo {repo_id}...")
            api.create_repo(
                repo_id=repo_id, 
                token=token, 
                repo_type="space", 
                space_sdk="docker", 
                exist_ok=True
            )
        
        # Prepare README for HF (must be named README.md at root)
        temp_readme = BASE_DIR / 'README_HF_TEMP.md'
        shutil.copy(BASE_DIR / 'HF_README.md', temp_readme)
        
        # Upload project files
        print("Uploading project files...")
        api.upload_folder(
            folder_path=str(BASE_DIR),
            repo_id=repo_id,
            repo_type="space",
            token=token,
            ignore_patterns=[".git*", "__pycache__*", "venv*", "*.pdb", ".gemini*", "README.md"], # Ignore original README
            path_in_repo=""
        )
        
        # Upload the HF-specific README as THE README.md in the repo
        api.upload_file(
            path_or_fileobj=str(temp_readme),
            path_in_repo="README.md",
            repo_id=repo_id,
            repo_type="space",
            token=token
        )
        
        # Clean up
        if temp_readme.exists(): os.remove(temp_readme)
        
        print(f"✅ Successfully deployed to: https://huggingface.co/spaces/{repo_id}")
        return True
    except Exception as e:
        print(f"❌ HF Deployment Failed: {e}")
        return False

def deploy_kaggle():
    user = os.getenv("KAGGLE_USERNAME")
    key = os.getenv("KAGGLE_KEY")
    
    if not user or not key:
        print("❌ KAGGLE_USERNAME or KAGGLE_KEY not found.")
        return False
        
    print("📊 Deploying to Kaggle Datasets...")
    
    # Kaggle expects the kaggle.json in ~/.kaggle/ on Linux or %USERPROFILE%\.kaggle\ on Windows
    # We will try to run the CLI directly if possible
    
    try:
        # Create a temp folder for upload
        upload_dir = BASE_DIR / 'kaggle_upload'
        upload_dir.mkdir(exist_ok=True)
        
        # Copy essential tables
        shutil.copy(BASE_DIR / 'outputs' / 'tables' / 'targets_ranked_v5_global.csv', upload_dir / 'global_priorities.csv')
        shutil.copy(BASE_DIR / 'data' / 'gene_signature_verified.csv', upload_dir / 'gene_signature.csv')
        shutil.copy(BASE_DIR / 'kaggle_metadata.json', upload_dir / 'dataset-metadata.json')
        
        # Run Kaggle command
        # Use python -m kaggle.cli to ensure the command is recognized in the environment
        cmd = [sys.executable, "-m", "kaggle.cli", "datasets", "create", "-p", str(upload_dir)]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Successfully deployed to Kaggle!")
            return True
        else:
            # Try update instead
            cmd_upd = [sys.executable, "-m", "kaggle.cli", "datasets", "version", "-p", str(upload_dir), "-m", "v4.1 update"]
            result = subprocess.run(cmd_upd, capture_output=True, text=True)
            if result.returncode == 0:
                 print(f"✅ Successfully updated Kaggle dataset version!")
                 return True
            print(f"❌ Kaggle Deployment Failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Kaggle Deployment Error: {e}")
        return False

def main():
    print("="*60)
    print("GLOBAL DEPLOYMENT AUTOMATION v4.1")
    print("="*60)
    
    hf_success = deploy_hf()
    print("-" * 30)
    kg_success = deploy_kaggle()
    
    print("\n" + "="*60)
    print("DEPLOYMENT SUMMARY")
    print(f"Hugging Face: {'✅ SUCCESS' if hf_success else '❌ FAILED (Check Credentials)'}")
    print(f"Kaggle:       {'✅ SUCCESS' if kg_success else '❌ FAILED (Check Credentials)'}")
    print("="*60)

if __name__ == "__main__":
    import shutil
    main()
