"""
HDT v4.0 Global Impact: Deep Learning Bioactivity Prediction
Trains a Neural Network (MLP) on molecular fingerprints to predict pChEMBL affinity.
"""

import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
from rdkit import Chem
from rdkit.Chem import AllChem
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
TABLE_DIR = BASE_DIR / 'outputs' / 'tables'

# Model Architecture
class BioactivityNet(nn.Module):
    def __init__(self, input_dim=2048):
        super(BioactivityNet, self).__init__()
        self.fc1 = nn.Linear(input_dim, 512)
        self.fc2 = nn.Linear(512, 128)
        self.fc3 = nn.Linear(128, 1)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.2)
        
    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.relu(self.fc2(x))
        x = self.fc3(x)
        return x

def smiles_to_fp(smiles, n_bits=2048):
    """Convert SMILES to Morgan Fingerprint vector."""
    try:
        mol = Chem.MolFromSmiles(smiles)
        if mol is None: return None
        fp = AllChem.GetMorganFingerprintAsBitVect(mol, 2, nBits=n_bits)
        return np.array(fp)
    except:
        return None

def train_bioactivity_model():
    print("="*50)
    print("PHASE 10: AI BIOACTIVITY PREDICTION (TORCH GNN-MLP)")
    print("="*50)
    
    # Load compound data with SMILES
    comp_path = TABLE_DIR / 'compounds_from_chembl.csv'
    if not comp_path.exists():
        print("Mined compounds with SMILES not found. Run updated chembl_compound_mining.py first.")
        return
        
    df = pd.read_csv(comp_path)
    df = df[df['SMILES'].notna() & (df['SMILES'] != '')]
    
    if len(df) < 50:
        print(f"Insufficient data for training ({len(df)} samples). Need at least 50 compounds.")
        return
        
    print(f"Featurizing {len(df)} compounds...")
    X = []
    y = []
    
    for _, row in df.iterrows():
        fp = smiles_to_fp(row['SMILES'])
        if fp is not None:
            X.append(fp)
            y.append(row['pChEMBL'])
            
    X = np.array(X)
    y = np.array(y).reshape(-1, 1)
    
    # K-Fold Cross-Validation (Addressing Reviewer 1 Critique)
    from sklearn.model_selection import KFold
    k = 5
    kf = KFold(n_splits=k, shuffle=True, random_state=42)
    fold_mses = []
    
    print(f"Starting {k}-Fold Cross-Validation...")
    for fold, (train_idx, val_idx) in enumerate(kf.split(X)):
        X_tr, X_val = torch.FloatTensor(X[train_idx]), torch.FloatTensor(X[val_idx])
        y_tr, y_val = torch.FloatTensor(y[train_idx]), torch.FloatTensor(y[val_idx])
        
        # New Model for each fold
        fold_model = BioactivityNet()
        fold_crit = nn.MSELoss()
        fold_opt = optim.Adam(fold_model.parameters(), lr=0.001)
        
        # Training
        for ep in range(80):
            fold_model.train()
            fold_opt.zero_grad()
            out = fold_model(X_tr)
            loss = fold_crit(out, y_tr)
            loss.backward()
            fold_opt.step()
            
        # Eval
        fold_model.eval()
        with torch.no_grad():
            val_out = fold_model(X_val)
            v_loss = fold_crit(val_out, y_val)
            fold_mses.append(v_loss.item())
        print(f"  Fold {fold+1} MSE: {v_loss.item():.4f}")
        
    avg_mse = np.mean(fold_mses)
    std_mse = np.std(fold_mses)
    print(f"\nFinal CV Stats: Mean MSE = {avg_mse:.4f} (+/- {std_mse:.4f})")
    
    # Final Model Training on Full Dataset
    print("\nTraining Final Model on full dataset...")
    X_t = torch.FloatTensor(X)
    y_t = torch.FloatTensor(y)
    
    model = BioactivityNet()
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    
    for epoch in range(100):
        model.train()
        optimizer.zero_grad()
        outputs = model(X_t)
        loss = criterion(outputs, y_t)
        loss.backward()
        optimizer.step()
        
    # Evaluation on full set (In-sample for final pred)
    model.eval()
    with torch.no_grad():
        final_outputs = model(X_t)
        final_loss = criterion(final_outputs, y_t)
        print(f"Final In-sample MSE: {final_loss.item():.4f}")
        
    # Predict for all candidates to get "AI_Refined_pChEMBL"
    print("Generating AI-predicted affinities...")
    with torch.no_grad():
        all_preds = model(torch.FloatTensor(X)).numpy()
        
    df['AI_Predicted_pChEMBL'] = all_preds.flatten().round(2)
    
    output_path = TABLE_DIR / 'v4_ai_predicted_results.csv'
    df.to_csv(output_path, index=False)
    
    print(f"AI prediction complete. Results saved to {output_path.name}")
    print("\nTop 5 AI-Validated Hits:")
    print(df.sort_values('AI_Predicted_pChEMBL', ascending=False).head(5)[['Gene', 'Drug_Name', 'pChEMBL', 'AI_Predicted_pChEMBL']])
    print("="*50)

if __name__ == "__main__":
    train_bioactivity_model()
