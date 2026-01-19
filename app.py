"""
Hugging Face Spaces Entry Point: Typhoid HDT Explorer v4.0.1
Unified application file for cloud hosting.
"""

import os
import shutil
from pathlib import Path
import streamlit as st

# Setup: Ensure scripts/v4_dashboard_global.py is the main app
# In HF Spaces, the main file should be in the root as 'app.py'

# 1. Define the main logic (mirroring scripts/v4_dashboard_global.py)
# We will import the main logic or just recreate the entry point for robustness

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Path handling for HF Environment
BASE_DIR = Path(__file__).parent
TABLE_DIR = BASE_DIR / 'outputs' / 'tables'

st.set_page_config(page_title="Enteric HDT Explorer v4.0", layout="wide", page_icon="🌍")

@st.cache_data
def load_data():
    path = TABLE_DIR / 'targets_ranked_v5_global.csv'
    if path.exists():
        return pd.read_csv(path)
    return None

@st.cache_data
def load_drugs():
    path = TABLE_DIR / 'v4_ai_predicted_results.csv'
    if path.exists():
        return pd.read_csv(path)
    return None

df_targets = load_data()
df_drugs = load_drugs()

# HEADER
st.title("🌍 Global Enteric HDT Discovery Portal")
st.markdown("### Powered by AI, Multi-Omics, and Causal Inference")

st.sidebar.markdown("# Discovery Suite")
menu = st.sidebar.selectbox("Navigate:", ["📊 Leaderboard", "🤖 AI Predictions", "🧬 Target Profile", "📄 About & Ethics"])

if df_targets is not None:
    if menu == "📊 Leaderboard":
        st.subheader("Global HDT Priority Rankings")
        st.dataframe(df_targets[['Global_Rank', 'Symbol', 'Global_Impact_Score', 'Scope', 'Pathway', 'Causal_Evidence']], use_container_width=True)
        
    elif menu == "🤖 AI Predictions":
        st.subheader("AI-Predicted Affinity for Prioritized Hits")
        if df_drugs is not None:
            st.dataframe(df_drugs.sort_values('AI_Predicted_pChEMBL', ascending=False).head(20)[['Drug_Name', 'Gene', 'pChEMBL', 'AI_Predicted_pChEMBL', 'Max_Phase']], use_container_width=True)
            
    elif menu == "🧬 Target Profile":
        gene = st.selectbox("Select Target:", df_targets['Symbol'].tolist())
        target = df_targets[df_targets['Symbol'] == gene].iloc[0]
        st.write(f"**Target:** {gene} | **Global Score:** {target['Global_Impact_Score']}")
        
    elif menu == "📄 About & Ethics":
        st.subheader("Scientific Integrity & Methodology")
        st.markdown("This portal provides authentic, evidence-based host-directed therapy candidates for Typhoid and Paratyphoid fever. All data is traced to verified literature (Thompson et al. 2009, Dunstan et al. 2014).")
        st.info("Diamond Open Access Strategy: This work is submitted to the Journal of Infection in Developing Countries (JIDC).")
else:
    st.error("Data files not found. Ensure outputs/tables/ are populated in the Space.")
